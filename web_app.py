import ipywidgets     as widgets
import seaborn        as sns
import plotly.express as px
import streamlit as st

import pandas         as pd
import numpy          as np

from matplotlib       import pyplot    as plt

from ipywidgets       import fixed,interact, interactive, fixed, interact_manual
from geopy.geocoders  import Nominatim
from tabulate         import tabulate
from matplotlib       import gridspec
from pathlib          import Path
from folium.plugins   import MarkerCluster
from streamlit_folium import folium_static
from datetime         import datetime

import geopandas
import folium

st.set_page_config(layout='wide')
f_data = st.sidebar.checkbox('Show Portfolio Page')

@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)

    return data

@st.cache(allow_output_mutation = True)
def get_geofile(url):
    geofile = geopandas.read_file(url)

    return geofile

def set_feature(data):
    data['price_m2'] = data['price']/data['sqft_lot']

    return data

if f_data:
    def overview_data(data):
        # ==============
        # Data Overview
        # ==============
        st.title('HOUSES CO')
        st.title('Data Overview')
        
        f_zipcode = st.sidebar.multiselect('Enter zipcode', data['zipcode'].unique())
        f_attributes = st.sidebar.multiselect('Enter columns', data.columns)

        # Filter overview table
        if   (f_zipcode != []) & (f_attributes != []):
            ov_data = data.loc[data['zipcode'].isin(f_zipcode), f_attributes]
        elif (f_zipcode != []) & (f_attributes == []):
            ov_data = data.loc[data['zipcode'].isin(f_zipcode), :]
        elif (f_zipcode == []) & (f_attributes != []):
            ov_data = data.loc[:, f_attributes]
        else:
            ov_data = data.copy()
        st.dataframe(ov_data)
        
        c1, c2 = st.columns((1, 1))
            # Average metrics
            
        if (f_zipcode != []):
            avg_data = data.loc[data['zipcode'].isin(f_zipcode), :]
        else:
            avg_data = data.copy()
            
        avg_data['price_m2'] = data['price_m2']
        df1 = avg_data[['id', 'zipcode']].groupby('zipcode').count().reset_index()
        df2 = avg_data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
        df3 = avg_data[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
        df4 = avg_data[['price_m2', 'zipcode']].groupby('zipcode').count().reset_index()
            
        m1 = pd.merge(df1, df2, on='zipcode', how='inner')
        m2 = pd.merge(m1,  df3, on='zipcode', how='inner')
        df = pd.merge(m2,  df4, on='zipcode', how='inner')
        df.columns = ['zipcode', 'total_houses', 'price', 'sqft_living', 'price/m2']
        
        c1.header('Average Values')
        c1.dataframe(df, height=600)
        
            # Statistic Descriptive
        if (f_attributes != []):
            num_attributes = data[f_attributes].select_dtypes(include=['int64', 'float64'])
        else:
            num_attributes = data.select_dtypes(include=['int64', 'float64'])
            
        media   = pd.DataFrame(num_attributes.apply(np.mean))
        mediana = pd.DataFrame(num_attributes.apply(np.median))
        std     = pd.DataFrame(num_attributes.apply(np.std))
        max_    = pd.DataFrame(num_attributes.apply(np.max))
        min_    = pd.DataFrame(num_attributes.apply(np.min))
        df1     = pd.concat([max_, min_, media, mediana, std], axis=1).reset_index()
        df1.columns = ['attributes', 'max', 'min', 'mean', 'median', 'std']
        
        c2.header('Descriptive Analysis')
        c2.dataframe(df1, height=600)
        
        return None
    
    def portfolio_density(data, geofile):
        # =======================
        # Densidade de Portfólio
        # =======================
        st.title('Region Overview')
        
        c1, c2 = st.columns((1, 1))
        
        c1.header('Portfolio Density')
        
        df = data
        
        # Base Map - Folium
        density_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()], default_zoom_start=15)
        marker_cluster = MarkerCluster().add_to(density_map)
        
        for name, row in df.iterrows():
            folium.Marker([row['lat'], row['long']], popup='Sold R${0} on: {1}. Features: {2} sqft, {3} bedrooms, {4} bathrooms, year built: {5}'
                      .format(row['price'],
                              row['date'],
                              row['sqft_living'],
                              row['bedrooms'],
                              row['bathrooms'],
                              row['yr_built'])).add_to(marker_cluster)
        with c1:
            folium_static(density_map)
            
        # Region Price Map
        c2.header('Price Density')
        df = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
        df.columns = ['ZIP', 'PRICE']

        geofile = geofile[geofile['ZIP'].isin(df['ZIP'].tolist())]
        region_price_map = folium.Map(location=[data['lat'].mean(),
                                            data['long'].mean()],
                                  default_zoom_start=15)
        region_price_map.choropleth(data=df,
                                geo_data=geofile,
                                columns=['ZIP', 'PRICE'],
                                key_on='feature.properties.ZIP',
                                fill_color='YlOrRd',
                                fill_opacity=0.7,
                                line_opacity=0.2,
                                legend_name='AVG PRICE')
        with c2:
            folium_static(region_price_map)
            
        return None
    
    def commercial_distribution(data):
        # ==================================================
        # Distribuição dos imóveis por categorias comerciais
        # ==================================================
        st.sidebar.title('Coomercial Options')
        
        st.title('Commercial Attributes')
        
        # Average Price per Year
        data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')

        min_year_built = int(data['yr_built'].min())
        max_year_built = int(data['yr_built'].max())
        st.sidebar.subheader('Select Max Year Built')
        f_year_built = st.sidebar.slider('Year Built', min_year_built,
                                     max_year_built,
                                     max_year_built)
        st.header('Average Price per Year Built')
        
        df = data.loc[data['yr_built'] < f_year_built]
        df = df[['yr_built', 'price']].groupby('yr_built').mean().reset_index()

        fig = px.line(df, x='yr_built', y='price')
        st.plotly_chart(fig, use_container_width=True)
        
        # Average Price per Day
        st.header('Average Price per Day')
        st.sidebar.subheader('Select Max Date')

        min_date = datetime.strptime(data['date'].min(), '%Y-%m-%d')
        max_date = datetime.strptime(data['date'].max(), '%Y-%m-%d')

        f_date = st.sidebar.slider('Date', min_date, max_date, max_date)
    
        data['date'] = pd.to_datetime(data['date'])
        df = data.loc[data['date'] < f_date]
        df = df[['date', 'price']].groupby('date').mean().reset_index()

        fig = px.line(df, x='date', y='price')
        st.plotly_chart(fig, use_container_width=True)
        
        # Histograma
        st.header('Price Distribution')
        st.sidebar.subheader('Select Max Price')

        min_price = int(data['price'].min())
        max_price = int(data['price'].max())
        avg_price = int(data['price'].mean())
        f_price = st.sidebar.slider('Price', min_price, max_price, max_price)
        df = data.loc[data['price'] < f_price]

        fig = px.histogram(df, x='price', nbins=50)
        st.plotly_chart(fig, use_container_width=True)
        
        return None
    
    def attributes_distribution(data):
        # ===============================================
        # Distribuição dos imoveis por categorias físicas
        # ===============================================
        st.sidebar.title('Attributes Options')
        
        st.title('House Attributes')

        f_bedrooms  = st.sidebar.selectbox('Max number of bedrooms',  sorted(set(data['bedrooms'].unique())))
        f_bathrooms = st.sidebar.selectbox('Max number of bathrooms', sorted(set(data['bathrooms'].unique())))
        
        c1, c2 = st.columns(2)
        
        # House per bedroms
        c1.header('Houses per bedrooms')
        df = data[data['bedrooms'] < f_bedrooms]
        fig = px.histogram(df, x='bedrooms', nbins=19)
        c1.plotly_chart(fig, use_container_width=True)
        
        # House per bathrooms
        c2.header('Houses per bathrooms')
        df = data[data['bathrooms'] < f_bathrooms]
        fig = px.histogram(df, x='bathrooms', nbins=19)
        c2.plotly_chart(fig, use_container_width=True)
        
        # filters
        f_floors = st.sidebar.selectbox('Max number of floor', sorted(set(data['floors'].unique())))
        f_waterview = st.sidebar.checkbox('Water View')
        
        c1, c2 = st.columns(2)
        
        # House per floors
        c1.header('House per floors')
        df = data[data['floors'] < f_floors]
        fig = px.histogram(df, x='floors', nbins=19)
        c1.plotly_chart(fig, use_container_width=True)
        
        # House per water view
        c2.header('Water View')
        if f_waterview:
            df = data[data['waterfront'] == 1]
        else:
            df = data.copy()
            
        fig = px.histogram(df, x='waterfront', nbins=10)
        
        c2.plotly_chart(fig, use_container_width=True)
        
        return None
            
######################################################################################################		
######################################################################################################		
######################################################################################################

else:
    
    def sell_attributes(data):
        
        st.title('HOUSES CO')
        st.title('Purchase/ Sell Table')
        
        st.sidebar.title('Table Filter')
        
        f_zipcode = st.sidebar.multiselect('Enter zipcode', data['zipcode'].unique())
        
        if (f_zipcode != []):
            data = data.loc[data['zipcode'].isin(f_zipcode)]
        else:
            data = data.copy()
               
        df = data[['zipcode', 'price']].groupby('zipcode').median().reset_index()
        
        df.columns = ['zipcode', 'price_median']

        data = pd.merge(data, df, on = 'zipcode', how = 'inner')
        
        data['status'] = data['condition'].apply(lambda x: 'Buy' if x>2 else 'Not Buy')
        
        data['date'] = pd.to_datetime(data['date'])
        
        data['season'] = data['date'].apply(lambda x: 'Spring' 
                                    if ((x >= pd.to_datetime('2014-03-20')) & (x < pd.to_datetime('2014-06-21')))
                                    |  ((x >= pd.to_datetime('2015-03-20')) & (x < pd.to_datetime('2015-06-21')))
                                    else 'Summer'
                                    if (x >= pd.to_datetime('2014-06-21')) & (x < pd.to_datetime('2014-09-22'))
                                    else 'Fall'
                                    if (x >= pd.to_datetime('2014-09-22')) & (x < pd.to_datetime('2014-12-21'))
                                    else 'Winter')   
        
        data['sell_price'] = data[['price', 'price_median', 'status']].apply(lambda x: 
                                   x['price']*1.3 if (x['price'] <  x['price_median']) & (x['status'] == 'Buy')
                              else x['price']*1.1 if (x['price'] >= x['price_median']) & (x['status'] == 'Buy') 
                              else 0, axis = 1)

        data['profit'] = data[['sell_price', 'price']].apply(lambda x: 
                                            (x['sell_price'] - x['price']) if x['sell_price'] != 0
                                       else 0, axis = 1)
        
        purchase_sell_rec = data.loc[data['status'] == 'Buy'][['id', 'zipcode', 'price_median', 'price', 'sell_price', 'profit', 'season']]
        
        st.dataframe(purchase_sell_rec)
        
        return None

    def update_map(data): 
        #filter data
        st.title('Map Recomendations')
        
        st.sidebar.title('Map Filter')
        
        min_price = int(data['price'].min())
        max_price = int(data['price'].max())
        avg_price = int(data['price'].mean())
        price_limit = st.sidebar.slider('Price', min_price, max_price, max_price)
        
        value = int(data['sqft_living'].mean())
        min_ = int(data['sqft_living'].min())
        max_ = int(data['sqft_living'].max())
        living_limit = st.sidebar.slider('Minimum Living Room Size', min_, max_, min_)
    
        value = int(data['bathrooms'].mean())
        min_ = int(data['bathrooms'].min())
        max_ = int(data['bathrooms'].max())
        bathroom_limit = st.sidebar.slider('Minimum Bathrooms Values', min_, max_, min_)
       
        value = int(data['yr_built'].mean())
        min_ =  int(data['yr_built'].min())
        max_ =  int(data['yr_built'].max())
        yrbuilt_limit  = st.sidebar.slider('Built Since Year', min_, max_, min_)#value)
       
        waterfront_limit = st.sidebar.checkbox('Only waterfront', value=False, disabled=False)

        data['status'] = data['condition'].apply(lambda x: 'Buy' if x>2 else 'Not Buy')
        
        if(waterfront_limit):
            houses = data[(data['price'] < price_limit) &
                       (data['sqft_living'] > living_limit) &
                       (data['bathrooms'] >= bathroom_limit) &
                       (data['yr_built'] >= yrbuilt_limit) &
                       (data['waterfront'] == waterfront_limit)][['id', 'lat', 'long', 'price', 'status']].copy()
        elif(waterfront_limit == False):
            houses = data[(data['price'] < price_limit) &
                       (data['sqft_living'] > living_limit) &
                       (data['bathrooms'] >= bathroom_limit) &
                       (data['yr_built'] >= yrbuilt_limit)][['id', 'lat', 'long', 'price', 'status']].copy()
        
        #plot map
        fig = px.scatter_mapbox(houses,
                               lat = 'lat',
                               lon = 'long',
                               color = 'status',
                               size = 'price',
                               color_continuous_scale = px.colors.cyclical.IceFire,
                               size_max = 15,
                               zoom = 9)
        
        fig.update_layout(mapbox_style = 'open-street-map')
        fig.update_layout(height = 600, margin = {'r':0, 'l':0, 't':0 , 'b':0})
        st.plotly_chart(fig)


if __name__ == "__main__":
    
    path = 'data/raw/kc_house_data.csv'
        
    data = get_data(path)
        
    if f_data:
        
        url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'
        
        geofile = get_geofile( url )
        
        data = set_feature(data)
        
        overview_data(data)
        
        portfolio_density(data, geofile)
    
        commercial_distribution(data)
    
        attributes_distribution(data)
        
    else:
        
        sell_attributes(data)
        
        update_map(data)