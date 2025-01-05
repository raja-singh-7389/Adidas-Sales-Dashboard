import pandas as pd 
import streamlit as st
import datetime
import plotly.express as px 
import plotly.graph_objects as go

print("Hello Learners")


df = pd.read_csv('Adidas.csv.csv')

st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html = True)

col1, col2 = st.columns([0.1,0.9])
with col1: 
  st.image('https://www.adidas.com/content/dam/on/demandware.static/-/Sites-adidas-us-catalog/default/dwb8c8a8b4/images/logo.svg')

  html_title = """
        <style>
        .title-test {
        font-weight: bold;
        padding : 5px;
        border-radius: 6px;
        }
        </style>
        <center><h1 class='title-test'>Adidas Interactive sales Dashboard</h1></center>"""

with col2:
 st.markdown(html_title,unsafe_allow_html = True)

col3,col4,col5 = st.columns([0.1,0.45,0.45])

with col3: 
  box_date= str(datetime.datetime.now().strftime("%d %B %Y"))
  st.write (f"Last update by : {box_date}")

with col4:
  fig = px.bar(df, x = "Retailer", y = "TotalSales", labels= {"TotalSales" : "Total Sales {$}"}, title = "Total Sales by Retailer", hover_data=["TotalSales"],template = "gridon",height = 500)

st.plotly_chart(fig,use_container_width=True)

_, view1, dwn1, view2, dwn2 = st.columns([0.15,0.20,0.20,0.20,0.20])

with view1:
  expander = st.expander("Retailer wise Sales")

data = df[["Retailer", "TotalSales"]].groupby(by="Retailer")["TotalSales"].sum()
expander.write(data)

with dwn1:

# Convert 'InvoiceDate' to datetime, handling errors gracefully
  df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors='coerce')

# Create 'Month_Year' column by extracting the month and year from 'InvoiceDate'
  df["Month_Year"] = df["InvoiceDate"].dt.strftime("%b %y")

# Group by 'Month_Year' and sum the 'TotalSales' for each month
result = df.groupby("Month_Year")["TotalSales"].sum().reset_index()

# Download button for CSV export
st.download_button("Get Data", data=result.to_csv(), file_name="sales_by_month.csv", mime="text/csv")

with col5:
  fig1= px.line(result, x ="Month_Year", y = "TotalSales", title= "Total Sales Over time", template="gridon")

st.plotly_chart(fig1, use_container_width=True)

with view2:
  expander = st.expander("MonthlySales")
  data= result
expander.write(data)

with dwn2:
  st.download_button("Get Data", data = result.to_csv(),file_name= "Monthy Sales.csv",mime="text/csv")
  st.divider()

result1 = df.groupby(by="State")[["TotalSales", "UnitsSold"]].sum().reset_index()

# add the units sold as a line chart on a secondary y-axis
import plotly.graph_objects as go

fig3 = go.Figure()

# Add Total Sales bar trace
fig3.add_trace(go.Bar(x=result1["State"], y=result1["TotalSales"], name="Total Sales"))

# Add Units Sold line trace
fig3.add_trace(go.Scatter(x=result1["State"], y=result1["UnitsSold"], mode="lines", name="Units Sold", yaxis="y2"))

# Update layout
fig3.update_layout(
    title="Total Sales and Units Sold by State",
    xaxis=dict(title="State"),
    yaxis=dict(title="Total Sales", showgrid=False),
    yaxis2=dict(title="Units Sold", overlaying="y", side="right"),
    template="gridon",
    legend=dict(x=1, y=1.1)
)


_, col6 = st.columns([0.1, 1])

with col6:
     st.plotly_chart(fig3, use_container_width=True)


# Layout for buttons and data display
_, view3, dwn3 = st.columns([0.5, 0.45, 0.45])

with view3:
    expander = st.expander("View Data for Sales by Units Sold")
    expander.write(result1)

with dwn3:
    st.download_button("Get Data", data=result1.to_csv(), file_name="Sales_by_UnitsSold.csv", mime="text/csv")
    st.divider()

_, col7 = st.columns([0.1, 1])

# Fixing treemap data creation
treemap = df[["Region", "City", "TotalSales"]].groupby(by=["Region", "City"])["TotalSales"].sum().reset_index()

# Format TotalSales values
def format_sales(value):
    if pd.notnull(value) and value >= 0:
        return '{:.2f} Lakh'.format(value / 1_00_000)
    return "N/A"

treemap["TotalSales(Formatted)"] = treemap["TotalSales"].apply(format_sales)

# Create the treemap
fig4 = px.treemap(
    treemap,
    path=["Region", "City"],
    values="TotalSales",
    hover_name="TotalSales(Formatted)",
    hover_data={"TotalSales": True, "TotalSales(Formatted)": False},  # Fix hover data
    color="City",
    height=700,
    width=600,
)

# Update traces
fig4.update_traces(textinfo="label+value")

# Render the treemap in Streamlit
with col7:
    st.subheader(":point_right: Total Sales by Region and City in Treemap")
    st.plotly_chart(fig4, use_container_width=True)


# First Section: Total Sales by Region and City
_, view4, dwn4 = st.columns([0.5, 0.45, 0.45])

with view4:
    # Group and calculate total sales by Region and City
    result2 = df[["Region", "City", "TotalSales"]].groupby(by=["Region", "City"])["TotalSales"].sum().reset_index()
    expander = st.expander("View data for Total Sales by Region and City")
    expander.write(result2)

with dwn4:
    # Provide download button for the grouped data
    st.download_button("Get Data", data=result2.to_csv(index=False), file_name="Sales_by_Region.csv", mime="text/csv")

# Divider between sections
st.divider()

# Second Section: Raw Data
_, view5, dwn5 = st.columns([0.5, 0.45, 0.45])

with view5:
    # Display raw data
    expander = st.expander("View Sales Raw Data")
    expander.write(df)

with dwn5:
    # Provide download button for raw data
    st.download_button("Get Raw Data", data=df.to_csv(index=False), file_name="SalesRawData.csv", mime="text/csv")

# Divider
st.divider()




