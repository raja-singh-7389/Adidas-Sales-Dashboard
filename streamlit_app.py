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

