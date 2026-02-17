import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

# Configuración de página
st.set_page_config(page_title="Dashboard vehículos US", layout="wide")

# Encabezado principal
st.title('📊 Análisis del mercado automotriz')

# Carga y limpieza consolidada
@st.cache_data 
def load_and_clean_data():
    df_vehicles = pd.read_csv('vehicles_us.csv')

    # 1. Tracción (is_4wd)
    df_vehicles['is_4wd'] = df_vehicles['is_4wd'].fillna(0).astype(int)

    # 2. Año del modelo
    df_vehicles['model_year'] = df_vehicles['model_year'].fillna(
        df_vehicles.groupby('model')['model_year'].transform('median')
    )
    df_vehicles.dropna(subset=['model_year'], inplace=True)
    df_vehicles['model_year'] = df_vehicles['model_year'].astype(int)

    # 3. Cilindros
    df_vehicles['cylinders'] = df_vehicles['cylinders'].fillna(
        df_vehicles.groupby('model')['cylinders'].transform(
            lambda x: x.mode()[0] if not x.mode().empty else np.nan
        )
    )
    # Llenar nulos restantes de cilindros si el modelo no tiene moda
    df_vehicles['cylinders'] = df_vehicles['cylinders'].fillna(df_vehicles['cylinders'].median())

    # 4. Odómetro (Kilometraje)
    df_vehicles['odometer'] = df_vehicles['odometer'].fillna(
        df_vehicles.groupby('model_year')['odometer'].transform('median')
    )
    df_vehicles['odometer'] = df_vehicles['odometer'].fillna(df_vehicles['odometer'].median())

    # 5. Color
    df_vehicles['paint_color'] = df_vehicles['paint_color'].fillna('unknown')

    # 6. Conversión final de tipos
    df_vehicles['cylinders'] = df_vehicles['cylinders'].astype(int)
    df_vehicles['odometer'] = df_vehicles['odometer'].astype(int)
    
    return df_vehicles

# Ejecutar limpieza
df = load_and_clean_data()

# Histograma visilble
st.subheader('Distribución general de precios')
fig_precios = px.histogram(df, x="price", 
                           nbins=50, 
                           color_discrete_sequence=['#636EFA'],
                           labels={'price': 'Precio de venta ($)'})

fig_precios.update_layout(yaxis_title="Cantidad de vehículos", 
                          xaxis_title="Precio ($)")
st.plotly_chart(fig_precios, use_container_width=True)

st.divider()

# Herramientas de análisis
st.header('Herramientas de análisis específico')

col_filters, col_charts = st.columns([1, 2])

with col_filters:
    st.write("### 🛠️ Personalizar vista")
    
    # Filtro de Precio
    min_p, max_p = int(df['price'].min()), int(df['price'].max())
    rango_precio = st.slider("Rango de precio ($)", min_p, max_p, (min_p, max_p))
    
    # Filtros extra solicitados
    condiciones = st.multiselect("Condición del vehículo", options=df['condition'].unique(), default=df['condition'].unique())
    
    # Checkboxes
    show_scatter = st.checkbox('Mostrar Precio vs Odómetro')
    show_type = st.checkbox('Mostrar Distribución por Tipo')

# Aplicar filtrado dinámico
df_filtered = df[
    (df['price'] >= rango_precio[0]) & 
    (df['price'] <= rango_precio[1]) &
    (df['condition'].isin(condiciones))
]

with col_charts:
    # Gráfico de dispersión
    if show_scatter:
        st.write("### Precio vs. kilometraje (datos filtrados)")
        fig_scat = px.scatter(df_filtered, x="odometer", y="price", 
                              color="condition",
                              hover_data=['model_year', 'model'],
                              labels={'odometer': 'Kilometraje (millas)', 'price': 'Precio ($)', 'condition': 'Estado'},
                              opacity=0.5)
        st.plotly_chart(fig_scat, use_container_width=True)
    
    # Gráfico por tipo
    if show_type:
        st.write("### Cantidad de vehículos por tipo")
        fig_type = px.histogram(df_filtered, x="type", color="type",
                               labels={'type': 'Tipo de Vehículo', 'count': 'Cantidad'})
        fig_type.update_layout(xaxis_title="Tipo de Carrocería", yaxis_title="Frecuencia")
        st.plotly_chart(fig_type, use_container_width=True)

    if not show_scatter and not show_type:
        st.info("Usa los filtros y casillas de la izquierda para profundizar en el análisis.")