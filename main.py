import pandas as pd
import streamlit as st
import plotly.express as px
import geopandas as gpd
import json

df = pd.read_csv('./data/fcast_delitos_comunas.csv')

df['ds'] = pd.to_datetime(df['ds'])




# Filtro de región
region = st.sidebar.selectbox('Selecciona una región', ['Región Metropolitana de Santiago',
                                                        'Región de Valparaíso',
                                                        ]
                              )
# Filtro de fecha
fecha_unica = df['ds'].unique()
fecha = st.sidebar.selectbox('Selecciona una fecha', fecha_unica)

dict_regiones = {
    'Región Metropolitana de Santiago': 13,
    'Región de Valparaíso': 5,
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
st.plotly_chart(map_fig)
