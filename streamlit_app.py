import pandas as pd 
import streamlit as st
import datetime
import plotly.express as px 
import plotly.graph_objects as go

print("Hello Learners")


df = pd.read_csv('adidas.csv.csv')

st.dataframe(df)
