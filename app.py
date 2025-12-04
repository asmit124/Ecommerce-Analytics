import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="E-Commerce Analytics Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS (DARK MODE) ---
st.markdown("""
    <style>
    /* Main Background - Dark Blue/Black */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Metric Cards Styling - Dark Mode */
    div[data-testid="metric-container"] {
        background-color: #262730;
        border: 1px solid #464B5C;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        color: #FFFFFF;
    }
    div[data-testid="metric-container"] label {
        color: #A3A8B8; /* Subtitle color */
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #0E1117;
        color: #FAFAFA;
        border-radius: 5px 5px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #262730;
        border-bottom: 2px solid #4e73df;
        color: #4e73df;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- HELPER: GENERATE MOCK DATA ---
def generate_mock_data():
    # Set seed for reproducibility (so graphs don't change every time)
    np.random.seed(42)
    
    # UPDATED: Generate data for 2023 AND 2024 to test year filter
    dates = pd.date_range(start="2023-01-01", end="2024-12-31", freq="D")
    selected_dates = np.random.choice(dates, 800) # Increased count
    products = ['Wireless Headphones', 'Gaming Mouse', 'Mechanical Keyboard', '4K Monitor', 'Laptop Stand']
    prices = {'Wireless Headphones': 120, 'Gaming Mouse': 60, 'Mechanical Keyboard': 150, '4K Monitor': 350, 'Laptop Stand': 45}
    
    data = []
    for date in selected_dates:
        prod = np.random.choice(products)
        qty = np.random.randint(1, 4)
        data.append({
            'OrderDate': date,
            'CustomerID': f"CUST-{np.random.randint(1000, 1050)}",
            'ProductID': prod,
            'Quantity': qty,
            'TotalSales': prices[prod] * qty
        })
    return pd.DataFrame(data)

# --- HELPER: CLEAN DATA ---
def clean_data(df):
    df = df.drop_duplicates()
    if 'OrderDate' in df.columns:
        df['OrderDate'] = pd.to_datetime(df['OrderDate'], dayfirst=True, errors='coerce')
    
    numeric_cols = ['TotalSales', 'Quantity']
    for col in numeric_cols:
        if col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.replace(r'[$,]', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    df = df.dropna(subset=['OrderDate', 'TotalSales'])
    return df

# --- HELPER: LOAD DATA ---
@st.cache_data
def load_data(file):
    try:
        df = pd.read_csv(file)
        df = clean_data(df) 
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.title("Data Controls")
    
    data_source = st.radio("Select Data Source", ["Upload CSV", "Use Demo Data"])
    
    df = None
    if data_source == "Upload CSV":
        uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
        if uploaded_file:
            df = load_data(uploaded_file)
    else:
        if st.button("Generate Sample Data", type="primary"):
            df = generate_mock_data()
            df = clean_data(df)
            st.success("Demo data generated!")

    st.markdown("---")
    st.markdown("### 🛠 Filter Settings")
    
    # Placeholders for filters
    year_filter_container = st.container()
    date_filter_container = st.container()

# --- MAIN APP LOGIC ---
if df is not None:
    # 1. Extract Unique Years
    df['Year'] = df['OrderDate'].dt.year
    available_years = sorted(df['Year'].unique(), reverse=True)
    
    # 2. Year Filter (Added)
    with year_filter_container:
        selected_year = st.selectbox("Select Year", available_years)
    
    # Filter data by Year first
    df_year = df[df['Year'] == selected_year]
    
    # 3. Date Range Filter (Constrained to selected year)
    min_date = df_year['OrderDate'].min()
    max_date = df_year['OrderDate'].max()
    
    with date_filter_container:
        # Handle case where year filtering might result in empty data (rare)
        if pd.isnull(min_date) or pd.isnull(max_date):
             st.warning("No data for this year.")
             filtered_df = df_year
             start_date, end_date = None, None
        else:
            date_range = st.date_input(
                "Refine Date Range",
                value=[min_date, max_date],
                min_value=min_date,
                max_value=max_date
            )
            
            # Handle user input (they might pick 1 date or 2)
            if len(date_range) == 2:
                start_date, end_date = date_range
                mask = (df_year['OrderDate'] >= pd.to_datetime(start_date)) & (df_year['OrderDate'] <= pd.to_datetime(end_date))
                filtered_df = df_year.loc[mask]
            else:
                start_date, end_date = date_range[0], date_range[0]
                filtered_df = df_year

    st.title("📊 E-Commerce Analytics Dashboard")
    if start_date and end_date:
        st.markdown(f"Overview for: **{selected_year}** ({start_date} to {end_date})")
    else:
        st.markdown(f"Overview for: **{selected_year}**")
        
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["📈 Executive Overview", "👥 Customer Segmentation (RFM)", "📋 Raw Data"])

    # --- TAB 1: EXECUTIVE OVERVIEW ---
    with tab1:
        total_revenue = filtered_df['TotalSales'].sum()
        avg_order_value = filtered_df['TotalSales'].mean()
        total_orders = len(filtered_df)
        unique_customers = filtered_df['CustomerID'].nunique()
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Revenue", f"${total_revenue:,.0f}")
        c2.metric("Avg Order Value", f"${avg_order_value:.2f}")
        c3.metric("Total Orders", f"{total_orders}")
        c4.metric("Active Customers", f"{unique_customers}")
        
        st.markdown("###") 

        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            st.subheader("Revenue Trend")
            sales_over_time = filtered_df.set_index('OrderDate').resample('W')['TotalSales'].sum().reset_index()
            
            # Area Chart matching the screenshot style
            fig_trend = px.area(sales_over_time, x='OrderDate', y='TotalSales', 
                                title=None,
                                color_discrete_sequence=['#4e73df']) # Blue color
            
            # FORCE DARK TEMPLATE
            fig_trend.update_layout(
                xaxis_title="", 
                yaxis_title="Sales ($)", 
                template="plotly_dark",  # <-- Key change for dark mode
                margin=dict(l=0, r=0, t=10, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_trend, use_container_width=True)

        with col_right:
            st.subheader("Top Products")
            top_products = filtered_df.groupby('ProductID')['TotalSales'].sum().nlargest(5).reset_index()
            
            # Bar Chart matching the screenshot style
            fig_bar = px.bar(top_products, x='ProductID', y='TotalSales', 
                             color='TotalSales', 
                             color_continuous_scale='Blues') # Blue gradient
            
            # FORCE DARK TEMPLATE
            fig_bar.update_layout(
                xaxis_title=None, 
                yaxis_title=None, 
                showlegend=False, 
                template="plotly_dark", # <-- Key change for dark mode
                margin=dict(l=0, r=0, t=10, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    # --- TAB 2: RFM SEGMENTATION ---
    with tab2:
        if not filtered_df.empty:
            snapshot_date = filtered_df['OrderDate'].max() + timedelta(days=1)
            rfm = filtered_df.groupby('CustomerID').agg({
                'OrderDate': lambda x: (snapshot_date - x.max()).days,
                'CustomerID': 'count',
                'TotalSales': 'sum'
            }).rename(columns={'OrderDate': 'Recency', 'CustomerID': 'Frequency', 'TotalSales': 'Monetary'})

            rfm['R_Score'] = pd.qcut(rfm['Recency'], 4, labels=['4','3','2','1'])
            try:
                rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=['1','2','3','4'])
                rfm['M_Score'] = pd.qcut(rfm['Monetary'], 4, labels=['1','2','3','4'])
            except:
                rfm['F_Score'] = '1'
                rfm['M_Score'] = '1'

            rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

            def segment_customer(row):
                if row['RFM_Score'] in ['444', '434', '443', '344']: return 'Champions'
                elif row['R_Score'] == '4': return 'New Users'
                elif row['R_Score'] == '1': return 'At Risk'
                else: return 'Regular'

            rfm['Segment'] = rfm.apply(segment_customer, axis=1)

            r_col1, r_col2 = st.columns([1, 2])
            
            with r_col1:
                st.markdown("#### Distribution")
                segment_counts = rfm['Segment'].value_counts()
                fig_pie = px.pie(values=segment_counts.values, names=segment_counts.index, 
                                   hole=0.5, color_discrete_sequence=px.colors.qualitative.Pastel)
                fig_pie.update_layout(showlegend=True, margin=dict(l=0, r=0, t=0, b=0), template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_pie, use_container_width=True)

            with r_col2:
                st.markdown("#### Value vs Frequency Matrix")
                fig_bubble = px.scatter(rfm, x='Frequency', y='Monetary', 
                                        color='Segment', size='Monetary', 
                                        hover_name=rfm.index,
                                        color_discrete_sequence=px.colors.qualitative.Pastel)
                fig_bubble.update_layout(template="plotly_dark", xaxis_title="Order Frequency", yaxis_title="Total Spend", paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_bubble, use_container_width=True)
                
            with st.expander("View Customer Details"):
                st.dataframe(
                    rfm,
                    column_config={
                        "Recency": st.column_config.NumberColumn("Recency", help="Days since last order"),
                        "Frequency": st.column_config.NumberColumn("Frequency"),
                        "Monetary": st.column_config.ProgressColumn("Monetary", format="$%f", min_value=0, max_value=float(rfm['Monetary'].max())),
                    },
                    use_container_width=True
                )

    # --- TAB 3: DATA ---
    with tab3:
        st.dataframe(filtered_df, use_container_width=True)

else:
    st.container()
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h1 style='text-align: center; color: white;'>👋 Welcome to Sales Analyzer</h1>", unsafe_allow_html=True)
        st.button("Generate Sample Data", type="primary")
