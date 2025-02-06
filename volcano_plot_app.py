import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from components.data_loader import prepara_dati

def mostra_volcano_plot():
    st.title("Volcano Plot Interattivo")

    # Controlla se i dati filtrati esistono in session_state
    if "dati_filtrati" in st.session_state and st.session_state["dati_filtrati"] is not None:
        dati = st.session_state["dati_filtrati"]
        classi = [st.session_state["class_1"], st.session_state["class_2"]]

        # Parametri di filtraggio
        fold_change_threshold = st.number_input('Soglia Log2FoldChange', value=0.0)
        p_value_threshold = st.number_input('Soglia -log10(p-value)', value=0.05)

        # Chiamata a prepara_dati
        from components.data_loader import prepara_dati
        dati_preparati = prepara_dati(dati, classi, fold_change_threshold, p_value_threshold)

        if dati_preparati is not None and not dati_preparati.empty:
            st.plotly_chart(px.scatter(dati_preparati, x='Log2FoldChange', y='-log10(p-value)',
                                       text='Variabile', hover_data=['Variabile']))
        else:
            st.error("⚠️ Nessun dato disponibile per il Volcano Plot.")
    else:
        st.error("⚠️ Nessun dato filtrato disponibile. Torna alla homepage e seleziona le classi.")
