import streamlit as st
from datetime import datetime
import uuid
import pandas as pd

# -------------------------------------------------------------
# 1. CONFIGURACIÓN DE LA PÁGINA
# -------------------------------------------------------------
st.set_page_config(
    page_title="Gestión de Eventos",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Gestión de eventos")
st.write("Bienvenido a tu aplicación web interactiva para administrar eventos.")

# -------------------------------------------------------------
# 2. BASE DE DATOS EN MEMORIA (Session State)
# -------------------------------------------------------------
if "eventos" not in st.session_state:
    # Ejemplo inicial de datos
    st.session_state.eventos = [
        {
            "ID": str(uuid.uuid4())[:8],
            "Nombre": "Conferencia de IA",
            "Fecha": "2026-11-15",
            "Categoría": "Tecnología",
            "Descripción": "Evento de actualización en Inteligencia Artificial"
        }
    ]

# -------------------------------------------------------------
# 3. MENÚ LATERAL (BARRA LATERAL)
# -------------------------------------------------------------
opcion = st.sidebar.selectbox(
    "Selecciona una opción:",
    ["Agregar evento", "Buscar evento", "Reportes / Ver todos"]
)

# -------------------------------------------------------------
# 4. LÓGICA DE CADA OPCIÓN
# -------------------------------------------------------------

# --- OPCIÓN 1: AGREGAR EVENTO ---
if opcion == "Agregar evento":
    st.subheader("➕ Registrar un nuevo evento")
    
    with st.form("form_agregar"):
        nombre = st.text_input("Nombre del evento:")
        fecha = st.date_input("Fecha del evento:", datetime.now())
        categoria = st.selectbox("Categoría:", ["General", "Tecnología", "Educación", "Negocios", "Social"])
        descripcion = st.text_area("Descripción:")
        
        boton_guardar = st.form_submit_button("Guardar Evento")
        
        if boton_guardar:
            if nombre.strip() != "":
                nuevo_evento = {
                    "ID": str(uuid.uuid4())[:8],
                    "Nombre": nombre,
                    "Fecha": str(fecha),
                    "Categoría": categoria,
                    "Descripción": descripcion
                }
                st.session_state.eventos.append(nuevo_evento)
                st.success(f"¡Evento '{nombre}' registrado con éxito!")
            else:
                st.warning("Por favor, ingresa un nombre para el evento.")

# --- OPCIÓN 2: BUSCAR EVENTO ---
elif opcion == "Buscar evento":
    st.subheader("🔍 Buscar eventos registrados")
    
    termino_busqueda = st.text_input("Ingresa el nombre o categoría a buscar:")
    
    if termino_busqueda:
        resultados = [
            e for e in st.session_state.eventos
            if termino_busqueda.lower() in e["Nombre"].lower() or termino_busqueda.lower() in e["Categoría"].lower()
        ]
        
        if resultados:
            st.success(f"Se encontraron {len(resultados)} coincidencia(s):")
            st.dataframe(pd.DataFrame(resultados), use_container_width=True)
        else:
            st.info("No se encontraron eventos con esos términos.")
    else:
        st.write("Escribe en la casilla superior para filtrar eventos.")

# --- OPCIÓN 3: REPORTES / VER TODOS ---
elif opcion == "Reportes / Ver todos":
    st.subheader("📊 Reporte general de eventos")
    
    if len(st.session_state.eventos) > 0:
        df_eventos = pd.DataFrame(st.session_state.eventos)
        
        # Tarjetas con métricas rápido
        col1, col2 = st.columns(2)
        col1.metric("Total de eventos", len(df_eventos))
        col2.metric("Categorías distintas", df_eventos["Categoría"].nunique())
        
        # Tabla completa
        st.dataframe(df_eventos, use_container_width=True)
        
        # Botón para descargar reporte en CSV
        csv = df_eventos.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Reporte en CSV",
            data=csv,
            file_name="reporte_eventos.csv",
            mime="text/csv"
        )
    else:
        st.info("Aún no hay eventos registrados.")
