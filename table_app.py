import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from components.data_loader import prepara_dati

def mostra_tabella():
    st.title("Tabella dei Dati - Volcano Plot")

    # **Verifica che i dati filtrati siano presenti**
    if "dati_filtrati" not in st.session_state or st.session_state["dati_filtrati"] is None:
        st.error("⚠️ Nessun dato disponibile. Torna alla homepage e seleziona le classi.")
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

    # **Calcolo della tabella senza visualizzare il Volcano Plot**
    dati_preparati["p-value"] = np.power(10, -dati_preparati["-log10(p-value)"])  
    dati_preparati["Prodotto"] = dati_preparati["-log10(p-value)"] * dati_preparati["Log2FoldChange"]

    # **Selezione delle colonne richieste**
    colonne_tabella = ["Variabile", "Log2FoldChange", "-log10(p-value)", "p-value", "Prodotto"]
    tabella_finale = dati_preparati[colonne_tabella]

    # **Mostra la tabella**
    st.dataframe(tabella_finale, use_container_width=True)
