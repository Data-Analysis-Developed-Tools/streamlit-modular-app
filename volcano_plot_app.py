import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from components.data_loader import prepara_dati

def mostra_volcano_plot():
    st.title("Volcano Plot Interattivo")

    # **Usiamo direttamente i dati elaborati in session_state**
    if "dati_processati" not in st.session_state or st.session_state["dati_processati"] is None:
        st.error("⚠️ Nessun dato disponibile per generare il Volcano Plot.")
        return
    dati_preparati = st.session_state["dati_processati"]

    # **Recuperiamo le soglie impostate**
    fold_change_threshold = st.session_state.get("fold_change_threshold", 0.0)
    p_value_threshold = st.session_state.get("p_value_threshold", 0.05)

    # **Generazione del Volcano Plot**
    try:
        fig = px.scatter(dati_preparati, x='Log2FoldChange', y='-log10(p-value)', 
                         text='Variabile',
                         hover_data=['Variabile'],
                         color=dati_preparati['MediaLog'] if "MediaLog" in dati_preparati.columns else None,
                         size=dati_preparati['MediaLog'] if "MediaLog" in dati_preparati.columns else None,
                         color_continuous_scale='RdYlBu_r', size_max=10)

        # **Linee di soglia Log2FoldChange**
        fig.add_trace(go.Scatter(x=[-fold_change_threshold, -fold_change_threshold], 
                                 y=[0, dati_preparati['-log10(p-value)'].max()], 
                                 mode='lines', line=dict(color='red', dash='dash', width=2)))

        fig.add_trace(go.Scatter(x=[fold_change_threshold, fold_change_threshold], 
                                 y=[0, dati_preparati['-log10(p-value)'].max()], 
                                 mode='lines', line=dict(color='red', dash='dash', width=2)))

        # **Linea di soglia -log10(p-value)**
        fig.add_trace(go.Scatter(x=[dati_preparati['Log2FoldChange'].min(), dati_preparati['Log2FoldChange'].max()], 
                                 y=[p_value_threshold, p_value_threshold], 
                                 mode='lines', line=dict(color='blue', dash='dash', width=2)))

        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"❌ Errore durante la generazione del Volcano Plot: {e}")
