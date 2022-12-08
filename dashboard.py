import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import cv2 

# Setting Page Configurations
st.set_page_config(
    page_title="Project IV <Div>Tech Dashboard",
    page_icon='📊',
    layout="wide",
    initial_sidebar_state="auto",
)

# Loading dataset
df = pd.read_csv('Life_Expectancy_00_15.csv', sep=';')

# Creating a cointainer
placeholder = st.empty()

with placeholder.container():
    # Title 
    st.title('Project IV <Div>Tech by Ada & Suzano 📊🌎')
    st.title(' ')
 
    # Head 
    head_1,head_2, head_3, head_4 = st.columns(4)
    with head_1:
        st.write('#### Dataset: Life Expectancy (2000-2015)')

    # Columns 
    col_1,col_2,col_3 = st.columns(3)

    # Filters (Year and Continent)
    with col_3:
        year_filter = st.selectbox('Choose a year',
                                        df['Year'].unique()) 
        # Aplicação do filtro 'Year'
        df_filtered = df[df['Year'] == year_filter]

        # Aplicação do filtro 'Continent'
        continent_filter = st.selectbox('Choose a continent',
                                        df_filtered['Continent'].unique())

        # Aplicação do filtro 'Continent'
        df_filtered = df_filtered[df_filtered['Continent'] == continent_filter]  

    # KPI Total Number of Countries
    head_3.metric(
        label=f'Total Number of Countries 🌎',
        value=len(df['Country'].unique()),
    )
    
    # KPI Number of Continent Countries 
    head_4.metric(
        label=f'Number of {continent_filter} Countries 📊',
        value=len(df_filtered['Country'].unique()),
    )
    
    # KPI Continent Life Expectancy
    col_3.metric(
        label=f'Mean {continent_filter} Life Expectancy in {year_filter}',
        value=int(df_filtered.groupby('Continent')['Life Expectancy'].mean()),
    )

    # KPI Continent Population
    col_3.metric(
        label=f'{continent_filter} Population',
        value=df_filtered.groupby('Continent')['Population'].sum())

    with col_1:      
        # Continent Most Populous Countries
        gp_countries_population = df_filtered\
            .groupby('Country')\
            ['Population']\
            .sum().to_frame()\
            .sort_values(by='Population', ascending = False)[0:10]

        fig = px.bar(gp_countries_population, x=gp_countries_population.index, y='Population')
        fig.update_layout(title_text=f'{continent_filter} Most Populous Countries', title_x=0.5) 
        st.plotly_chart(fig, use_container_width=True, sharing="streamlit", theme=None)

    with col_2:
        # Continent Countries with Largest Mean Life Expectancy
        gp_countries_expectancy = df_filtered\
            .groupby('Country')\
            ['Life Expectancy']\
            .mean().to_frame()\
            .sort_values(by='Life Expectancy', ascending = False)[0:10]

        fig = px.bar(gp_countries_expectancy, x=gp_countries_expectancy.index, y='Life Expectancy')
        fig.update_layout(title_text=f'{continent_filter} Countries with Largest Mean Life Expectancy', title_x=0.5) 
        st.plotly_chart(fig, use_container_width=True, sharing="streamlit", theme=None)

    with col_2:
        # Continent Countries with Largest Mean Life Expectancy
        gp_countries_expectancy = df_filtered\
            .groupby('Country')\
            ['Life Expectancy']\
            .mean().to_frame()\
            .sort_values(by='Life Expectancy', ascending = False)[0:10]

        fig = px.bar(gp_countries_expectancy, x=gp_countries_expectancy.index, y='Life Expectancy')
        fig.update_layout(title_text=f'{continent_filter} Countries with Largest Mean Life Expectancy', title_x=0.5) 
        st.plotly_chart(fig, use_container_width=True, sharing="streamlit", theme=None)

