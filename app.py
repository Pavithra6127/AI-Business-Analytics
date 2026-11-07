
import pandas as pd
import streamlit as st
import plotly.express as px

# Page settings
st.set_page_config(
    page_title="Business Analytics Dashboard",
    layout="wide"
)

# Load dataset
data = pd.read_csv(
    "Superstore.xlsx.csv",
    encoding="latin1",
    usecols=range(21)
)

# Clean numerical data
for column in ["Sales", "Quantity", "Discount", "Profit"]:
    data[column] = pd.to_numeric(data[column], errors="coerce")

data = data.dropna(subset=["Sales", "Profit"])

# Dashboard title
st.title("AI-Powered Business Analytics Dashboard")
st.write("Analyze sales, profit and business performance.")

# Sidebar filters
st.sidebar.header("Filter Data")

regions = ["All"] + sorted(data["Region"].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("Select Region", regions)

categories = ["All"] + sorted(data["Category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Select Category", categories)

# Apply filters
filtered_data = data.copy()

if selected_region != "All":
    filtered_data = filtered_data[
        filtered_data["Region"] == selected_region
    ]

if selected_category != "All":
    filtered_data = filtered_data[
        filtered_data["Category"] == selected_category
    ]

# Key Performance Indicators
st.subheader("Business Performance")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"${filtered_data['Sales'].sum():,.2f}")
col2.metric("Total Profit", f"${filtered_data['Profit'].sum():,.2f}")
col3.metric("Total Orders", filtered_data["Order ID"].nunique())
col4.metric("Total Quantity", int(filtered_data["Quantity"].sum()))

# Sales by Category
st.subheader("Sales by Category")

category_sales = (
    filtered_data.groupby("Category", as_index=False)["Sales"].sum()
)

fig1 = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    color="Category",
    title="Category-wise Sales"
)

st.plotly_chart(fig1, use_container_width=True)

# Profit by Region
st.subheader("Profit by Region")

region_profit = (
    filtered_data.groupby("Region", as_index=False)["Profit"].sum()
)

fig2 = px.pie(
    region_profit,
    names="Region",
    values="Profit",
    title="Region-wise Profit"
)

st.plotly_chart(fig2, use_container_width=True)

# Display dataset
st.subheader("Sales Data")
st.dataframe(filtered_data, use_container_width=True)
