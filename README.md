📊 E-Commerce Sales Analytics Dashboard
🔗 Live Demo:https://ecommerce-analytics1-d9prowngtyeqblir3f4pfs.streamlit.app/

A powerful, interactive analytics dashboard built with Python and Streamlit. This tool transforms raw e-commerce sales data into actionable insights, featuring automated data cleaning, executive KPIs, and advanced Customer Segmentation (RFM Analysis).

🚀 Features

Zero-Config Demo Mode: Visualize the dashboard immediately with one-click sample data generation.

Automated Data Cleaning: Automatically handles duplicates, fixes date formats, and sanitizes currency strings (e.g., $1,200.00 → 1200.00).

Executive Overview: Real-time KPIs for Total Revenue, Average Order Value, and Active Customers.

Interactive Visualizations:

Revenue Trends (Area Charts)

Top Selling Products (Bar Charts)

Sales Seasonality

Advanced Customer Segmentation: automatically classifies customers using RFM Analysis (Recency, Frequency, Monetary) into segments like:

🏆 Champions (High value, frequent buyers)

🌟 Loyal (Regular buyers)

📉 At Risk (Haven't purchased recently)

Date Range Filtering: Dynamically slice data by specific time periods.

🛠️ Installation & Local Setup

Clone the repository

git clone [https://github.com/asmit124/Ecommerce-Analytics_1](https://github.com/asmit124/Ecommerce-Analytics_1)
cd ecommerce-dashboard


Install dependencies
Make sure you have Python installed, then run:

pip install -r requirements.txt


Run the application

streamlit run dashboard.py


View in Browser
The app will automatically open at http://localhost:8501.

📂 Expected CSV Format

If you choose to upload your own data, ensure your CSV contains the following columns (headers are case-insensitive in the cleaning logic, but preferred as below):

Column Name

Description

Example

OrderDate

Date of purchase

2023-01-15 or 15-01-2023

TotalSales

Revenue from the order

150.00 or $150

CustomerID

Unique ID for the customer

CUST-001

ProductID

Name or ID of the product

Wireless Mouse

Quantity

(Optional) Number of items

2

📦 Deployment

Method 1: Streamlit Cloud (Easiest)

Push this code to a GitHub repository.

Log in to Streamlit Cloud.

Click "New App" and select your repository.

Click Deploy.

Method 2: Hugging Face Spaces

Create a new Space on Hugging Face.

Select Streamlit as the SDK.

Upload dashboard.py (rename to app.py) and requirements.txt.

🧰 Tech Stack

Frontend/Backend: Streamlit

Data Processing: Pandas & NumPy

Visualization: Plotly Express

📄 License

This project is open-source and available under the MIT License.
