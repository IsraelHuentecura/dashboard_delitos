import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout = 'wide')


df = pd.read_csv('./data/fcast_delitos_comunas.csv')

df['ds'] = pd.to_datetime(df['ds'])
# Filtro por comuna
comuna = st.sidebar.selectbox('Selecciona una comuna', df['comuna'].unique())
df_filter = df[df['comuna'] == comuna]

# Hacer un smooth de la serie de tiempo
df_filter['yhat'] = df_filter['yhat'].rolling(window=12).mean()
df_filter['tasa_dmcs'] = df_filter['tasa_dmcs'].rolling(window=12).mean()

# Hacer un gráfico de series de tiempo yhat y tasa_dmcs vs el tiempo
fig = px.line(df_filter, x='ds', y=['yhat', 'tasa_dmcs'], title=f'Predicción de delitos de mayor connotación social en {comuna}')

#Hacer el grafico más ancho
fig.update_layout(width=1000, height=600)

# Poner de nombre fecha en el eje X
fig.update_xaxes(title_text='Fecha')
# Poner de nombre Delitos de mayor connotación social en el eje Y
fig.update_yaxes(title_text='Delitos de mayor connotación social (miles)')
# En la leyenda de yhat poner 'Predicción'
fig.for_each_trace(lambda t: t.update(name=t.name.replace("yhat", "Predicción")))
# En la leyenda de tasa_dmcs poner 'Tasa de delitos'
fig.for_each_trace(lambda t: t.update(name=t.name.replace("tasa_dmcs", "Tasa de delitos")))
# Mostrar el gráfico
st.plotly_chart(fig)