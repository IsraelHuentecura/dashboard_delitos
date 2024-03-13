import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv('./data/fcast_delitos_comunas.csv')

df['ds'] = pd.to_datetime(df['ds'])
# Filtro por comuna
comuna = st.sidebar.selectbox('Selecciona una comuna', df['comuna'].unique())
df_filter = df[df['comuna'] == comuna]
# Hacer un gráfico de series de tiempo yhat y tasa_dmcs vs el tiempo
fig = px.line(df_filter, x='ds', y=['yhat', 'tasa_dmcs'], title='Delitos en la comuna de Santiago')
st.plotly_chart(fig)