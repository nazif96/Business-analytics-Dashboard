import streamlit as st 
import pandas as pd
import numpy as np
from numerize import numerize
import plotly.express as px
import plotly.subplots as sp
import os 

st.set_page_config(page_title="Business Analytics Dashbord", page_icon="🌍", layout="wide")
st.subheader("📉 Business Analytics Dashbord") 

# chargement CSS style
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# chargement des données
df = pd.read_csv("customers.csv")

# Sidebar
st.sidebar.header("veuillez filtrer")
departement = st.sidebar.multiselect(
    "Filtrer Departement",
    options= df['Department'].unique(),
    default= df['Department'].unique(),
)

pays = st.sidebar.multiselect(
    "Filtrer Country",
    options= df['Country'].unique(),
    default= df['Country'].unique(),
)

businessunit = st.sidebar.multiselect(
    "Filtrer Business Unit",
    options= df['BusinessUnit'].unique(),
    default= df['BusinessUnit'].unique(),
)


df_selection = df.query("Department == @departement & Country == @pays & BusinessUnit == @businessunit")


# Meilleurs analyses 

def metrics():
    from streamlit_extras.metric_cards import style_metric_cards 
    st.subheader("📊 Meilleurs analyses")
    col1, col2, col3 = st.columns(3)
    
    col1.metrics(label="Total Clients", value= df_selection.Gender.count(), delta="tout les clients")
    
    col2.metrics(label="Total salaire annuel", value= f"{df_selection.AnnualSalary.sum():, .0f}", delta=df.AnnualSalary.median()) 
    
    col3.metrics(label= "Salaire Annuel", value = f"{df_selection.AnnualSalary.max()-df.AnnualSalary.min():, .0f}", delta= "échelle Salariale annuelle") 
    
    style_metric_cards(background_color="#121270", border_left_color="#FFD700", text_color="#f20045", box_shadow="3px")
    