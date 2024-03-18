import pandas as pd
import streamlit as st
import plotly.express as px
import geopandas as gpd
import json

df = pd.read_csv('./data/fcast_delitos_comunas.csv')

df['ds'] = pd.to_datetime(df['ds'])


st.set_page_config(layout = 'wide')



# Filtro de región
region = st.sidebar.selectbox('Selecciona una región', ['Región Metropolitana de Santiago',
                                                        'Región de Valparaíso',
                                                        'Región de Coquimbo',
                                                        'Región de O’Higgins',
                                                        'Región del Maule',
                                                        'Región de Ñuble',
                                                        'Región del Biobío',
                                                        'Región de La Araucanía',
                                                        'Región de Los Ríos',
                                                        'Región de Los Lagos',
                                                        'Región de Aysén del General Carlos Ibáñez del Campo',
                                                        'Región de Magallanes y de la Antártica Chilena',
                                                        'Región de Arica y Parinacota',
                                                        'Región de Tarapacá',
                                                        'Región de Antofagasta',
                                                        'Región de Atacama'
                                                        
                                                        ]
                              )
# Filtro de fecha
fecha_unica = df['ds'].unique()
fecha = st.sidebar.selectbox('Selecciona una fecha', fecha_unica)

dict_regiones = {
    'Región Metropolitana de Santiago': 13,
    'Región de Valparaíso': 5,
    'Región de Coquimbo': 4,
    'Región de O’Higgins': 6,
    'Región del Maule': 7,
    'Región de Ñuble': 16,
    'Región del Biobío': 8,
    'Región de La Araucanía': 9,
    'Región de Los Ríos': 14,
    'Región de Los Lagos': 10,
    'Región de Aysén del General Carlos Ibáñez del Campo': 11,
    'Región de Magallanes y de la Antártica Chilena': 12,
    'Región de Arica y Parinacota': 15,
    'Región de Tarapacá': 1,
    'Región de Antofagasta': 2,
    'Región de Atacama': 3,
    
}

# Tu objeto GeoJSON desde el path
path_json = f'chile-geojson-master/{dict_regiones[region]}.geojson'

# Convierte la cadena de texto a un objeto de Python
geojson_obj = json.loads(open(path_json).read())

# Convierte el objeto GeoJSON a un GeoDataFrame
gdf = gpd.GeoDataFrame.from_features(geojson_obj)

# Hacer un join con el dataframe y el geojson en base a la comuna y la fecha
gdf = gdf.merge(df, left_on='Comuna', right_on='comuna', how='inner')
gdf = gdf[gdf['ds'] == fecha]

# Determinar centroide de la región
gdf['centroid'] = gdf['geometry'].centroid
gdf['lon'] = gdf['centroid'].x
gdf['lat'] = gdf['centroid'].y


# Crea el gráfico con Plotly y como mapa de calor la variable tasa_dmcs
map_fig = px.choropleth_mapbox(gdf, geojson=gdf.geometry, 
                           locations=gdf.index, 
                            color='tasa_dmcs',
                           title='Región Metropolitana de Santiago por Comunas',
                           mapbox_style="carto-positron",
                           center={"lat": gdf['lat'].mean(), "lon": gdf['lon'].mean()},
                           zoom=7,
                           hover_data=['Comuna'])

# Hacer que el grafico más ancho
map_fig.update_layout(width=1000, height=600)
st.plotly_chart(map_fig)
