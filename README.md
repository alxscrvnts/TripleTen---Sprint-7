# SPRINT 7 - Análisis de Mercado de Vehículos 

Este proyecto consiste en una aplicación web interactiva desarrollada con **Streamlit** y **Plotly**, diseñada para explorar y visualizar datos de anuncios de venta de vehículos en los Estados Unidos. La Fase 1 se enfoca en la limpieza de datos, análisis exploratorio (EDA) y la creación de un dashboard funcional.

---

## 🛠️ Funcionalidades del dashboard

La aplicación permite a los usuarios interactuar con los datos mediante:
- **Histograma de precios:** Una visualización fija para entender la distribución del valor de mercado.
- **Filtros dinámicos:** Slider de precios y selector multivariable para filtrar por condición del vehículo.
- **Visualización bajo demanda:** Casillas de verificación (checkboxes) para desplegar:
    - Gráfico de dispersión (Precio vs. Odómetro) para analizar el impacto del kilometraje.
    - Gráfico de barras para comparar tipos de carrocería disponibles.

---

## Proceso de Limpieza (Consolidado)

Para asegurar la integridad del análisis, se aplicó un bloque de limpieza que resuelve:
1. **Tracción:** Conversión de valores nulos en `is_4wd` a un formato binario (0/1).
2. **Años del Modelo:** Imputación de nulos utilizando la mediana según el modelo del vehículo.
3. **Cilindros:** Llenado de datos faltantes basado en la moda del modelo.
4. **Odómetro:** Imputación de kilometraje basada en la mediana del año del modelo y la mediana global.
5. **Colores:** Clasificación de nulos como `unknown`.

---

## Cómo ejecutar la aplicación localmente

1. **Clonar el repositorio:**
   ```bash
   git clone <https://github.com/alxscrvnts/TripleTen---Sprint-7>
   cd "TripleTen - Sprint 7"
