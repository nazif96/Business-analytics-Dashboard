import streamlit as st 
import pandas as pd
import numpy as np
from numerize import numerize
import plotly.express as px
import plotly.subplots as sp

st.set_page_config(page_title="Business Analytics Dashbord", page_icon="🌍", layout="wide")
st.subheader("📉 Business Analytics Dashbord") 

# chargement CSS style
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# chargement des données
df = pd.read_csv("Données/customers.csv")  # chargement des données
print(df) 