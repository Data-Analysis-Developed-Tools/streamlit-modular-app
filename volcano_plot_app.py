import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from components.data_loader import prepara_dati

def mostra_volcano_plot():
    st.title("Volcano Plot Interattivo")

    # **Verifica che i dati filtrati siano presenti**
    if "dati_filtrati" not in st.session_state or st.session_state["dati_filtrati"] is None:
        st.error("⚠️ Nessun dato disponibile per generare il Volcano Plot.")
        return
    dati = st.session_state["dati_filtrati"]
    classi = [st.session_state.get("class_1"), st.session_state.get("class_2")]

    # **Verifica che le classi siano state selezionate**
    if None in classi:
        st.error("⚠️ Le classi non sono state selezionate correttamente.")
        return

    # **Recupera i parametri impostati nella sidebar**
    fold_change_threshold = st.session_state.get("fold_change_threshold", 0.0)
    p_value_threshold = st.session_state.get("p_value_threshold", 0.05)

    # **Prepara i dati**
    try:
        dati_preparati = prepara_dati(dati, classi, fold_change_threshold, p_value_threshold)
    except Exception as e:
        st.error(f"❌ Errore in `prepara_dati`: {e}")
        return

    if dati_preparati is None or dati_preparati.empty:
        st.error("⚠️ Il dataframe 'dati_preparati' è vuoto! Controlla i parametri di filtraggio.")
        return

    # **Calcolo della tabella**
    dati_preparati["p-value"] = np.power(10, -dati_preparati["-log10(p-value)"])  # Calcolo del p-value
    dati_preparati["Prodotto"] = dati_preparati["-log10(p-value)"] * dati_preparati["Log2FoldChange"]

    # **Selezione delle colonne richieste**
    colonne_tabella = ["Variabile", "-log10(p-value)", "p-value", "Log2FoldChange", "Prodotto"]
    tabella_finale = dati_preparati[colonne_tabella]

    # **Esportiamo la tabella in session_state per il modulo table_app.py**
    st.session_state["dati_tabella"] = tabella_finale
