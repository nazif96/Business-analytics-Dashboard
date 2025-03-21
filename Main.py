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
    
    
# ceer les div pour les graphiques

div1, div2 = st.columns(2) 
# 📊 pie chart 
def pie_chart():
    with div1: 
        theme_plotly = None  
        fig = px.pie(df_selection, values='AnnualSalary', names='Department', title='Répartition des salaires par département')
        fig.update_layout(legende_title ='Country', legend_y=0.9)
        fig.update_traces(textinfo ='percent+label', textposition= 'inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
# 📊 bar chart (Barres )
def bar_chart():
    theme_plotly = None 
    with div2:
        theme_plotly = None
        fig = px.bar(df_selection, x='Department', y='AnnualSalary', text_auto= '.2s', title=' ')
        fig.update_traces(textfont_size= 16, textangle=0, textposition='outside', cliponaxis=False)
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")
        
# 📊 scatter plot (Nuage de points)


#mysql table 
def table():
    with st.expander("Tabular"):
        #st.dataframe(df_selection)
        shwdata = st.multiselect('Filtrer:', df.columns, default= ['EEID', 'FullName', 'JobTitle', 'Department', 'BusinessUnit', 'Gender','Ethnicity', 'Age', 'HireDate', 'AnnualSalary', 'Bonus', 'Country', 'City', 'id']) 
        st.dataframe(df_selection[shwdata], use_container_width=True)


# option menu         
from streamlit_option_menu import option_menu
with st.sidebar:
    selected= option_menu(
        menu_title= "Main Menu",
        options= ["Home", "Table"],
        icons= ["Home", "book"],
        menu_icon= "cast", # option
        default_index= 0, 
        orientation= "vertical",
    
        
    )


if selected == "Home":
    pie_chart()
    bar_chart()
    metrics()
    
if selected == "Table":
    metrics()
    table()
    st.dataframe(df_selection.describe().T, use_container_width=True)  