import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px

# Setting Page Configurations
st.set_page_config(
    page_title="Project IV <Div>Tech Dashboard",
    page_icon='📊',
    layout="wide",
    initial_sidebar_state="auto",
)

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://img.freepik.com/vetores-gratis/copie-o-fundo-branco-ondulado-do-espaco_23-2148845471.jpg?w=2000");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()


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
        continent_filter = st.selectbox('Choose a continent', np.append('Global', df_filtered['Continent'].unique()))

        # Aplicação do filtro 'Continent'
        if (continent_filter != 'Global'):
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
    
    # KPI Life Expectancy
    if (continent_filter != 'Global'):
        col_3.metric(
            label=f'Mean {continent_filter} Life Expectancy in {year_filter}',
            value=int(df_filtered.groupby('Continent')['Life Expectancy'].mean()),
        )
        # KPI Global Population
        col_3.metric(
            label=f'{continent_filter} Population',
            value=df_filtered.groupby('Continent')['Population'].sum())

    else:
        col_3.metric(
            label=f'Mean {continent_filter} Life Expectancy in {year_filter}',
            value=int(df.groupby('Continent')['Life Expectancy'].mean().values.mean()),
        )
        col_3.metric(
            label=f'{continent_filter} Population',
            value=int(df.groupby('Continent')['Population'].mean().values.mean()),
        )
  

    with col_1:
        fig = px.scatter(df_filtered, y = 'Life Expectancy', x='Health expenditure', color='Continent', template='seaborn')
        fig.update_layout(xaxis_title='Health Expenditure', yaxis_title='Life Expectancy')
        fig.update_layout(title_text=f'{continent_filter} Correlation Heath Expenditure x Life Expectancy', title_x=0.5) 
        st.plotly_chart(fig, use_container_width=True, sharing="streamlit", theme=None)

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
    

    if (continent_filter == 'Global'):
        with col_2:
            # Forest Area Distribution by Continent
            df_filtered_continent = df.groupby(['Continent', 'Year'])['Forest area'].sum()\
                .to_frame().sort_values(by='Forest area', ascending=False).reset_index()

            fig = px.line(df_filtered_continent, x='Year', y='Forest area', color='Continent', markers=True)
            fig.update_layout(title_text=f'Forest Area by Continent From 2000 to 2015', title_x=0.5) 
            st.plotly_chart(fig, use_container_width=True, sharing="streamlit", theme=None)
    else:
        with col_2:
            # Forest Area Distribution by Country
            df_filtered_country = df[df['Continent'] == continent_filter].sort_values(by='Forest area', ascending=False).reset_index()

            grouped_continent = df.groupby(['Continent','Year'])['Forest area'].mean().reset_index()
            fig = px.line(df_filtered_country.iloc[0:75], x='Year', y='Forest area', color='Country', markers=True)
            fig.update_layout(title_text=f'Largest Forest Area by {continent_filter} Countries From 2000 to 2015', title_x=0.5) 
            st.plotly_chart(fig, use_container_width=True, sharing="streamlit", theme=None)

        

    with col_2:
        if (continent_filter=='Global'):
            # Filtering dataframe
            df_2000 = df[df.loc[:,'Year']==2000].copy()
            df_2015 = df[df.loc[:,'Year']==2015].copy()

            # Calculating population difference
            df_2015['pop_difference'] = df_2015['Population'].values-df_2000['Population'].values

            # Plotting top 10 countries with largest difference population between 2000 and 2015
            df_2015=df_2015.groupby('Country')['pop_difference'].sum().to_frame().sort_values(by='pop_difference', ascending=False)[0:10]

            fig = px.bar(df_2015, x=df_2015.index, y='pop_difference')
            fig.update_layout(title_text=f'Countries with Largest Difference Population (2000 to 2015)', title_x=0.5) 
            fig.update_yaxes(title_text='Population Difference')
            st.plotly_chart(fig, use_container_width=True, sharing="streamlit", theme=None)
        else: 
            df_filtered_country = df[df['Continent'] == continent_filter]
            # Filtering dataframe
            df_2000 = df_filtered_country[df_filtered_country.loc[:,'Year']==2000].copy()
            df_2015 = df_filtered_country[df_filtered_country.loc[:,'Year']==2015].copy()

            # Calculating population difference
            df_2015['pop_difference'] = df_2015['Population'].values-df_2000['Population'].values

            # Plotting top 10 countries with largest difference population between 2000 and 2015
            df_2015=df_2015.groupby('Country')['pop_difference'].sum().to_frame().sort_values(by='pop_difference', ascending=False)[0:10]

            fig = px.bar(df_2015, x=df_2015.index, y='pop_difference')
            fig.update_layout(title_text=f'{continent_filter} Countries with Largest Difference Population (2000 to 2015)', title_x=0.5) 
            fig.update_yaxes(title_text='Population Difference')
            st.plotly_chart(fig, use_container_width=True, sharing="streamlit", theme=None)


