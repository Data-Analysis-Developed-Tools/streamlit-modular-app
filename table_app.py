import streamlit as st
import pandas as pd
import numpy as np
from components.data_loader import carica_dati, prepara_dati

def processa_dati():
    # Controlla se i dati filtrati esistono in session_state
    if "dati_filtrati" not in st.session_state or st.session_state["dati_filtrati"] is None:
        return  # Se non ci sono dati, non fa nulla

    dati = st.session_state["dati_filtrati"]
    classi = [st.session_state.get("class_1"), st.session_state.get("class_2")]

    # Se le classi non sono state selezionate, non fa nulla
    if None in classi:
        return

    # **Recuperiamo i parametri impostati nella sidebar**
    fold_change_threshold = st.session_state.get("fold_change_threshold", 0.0)
    p_value_threshold = st.session_state.get("p_value_threshold", 0.05)

    # **Prepara i dati**
    try:
        dati_preparati = prepara_dati(dati, classi, fold_change_threshold, p_value_threshold)
    except Exception:
        return  # Se `prepara_dati` fallisce, il modulo non esegue nulla

    if dati_preparati is None or dati_preparati.empty:
        return  # Se i dati risultano vuoti, non fa nulla

    # **Calcolo di p-value se non è presente**
    if "p-value" not in dati_preparati.columns and "-log10(p-value)" in dati_preparati.columns:
        dati_preparati["p-value"] = np.power(10, -dati_preparati["-log10(p-value)"])

    # **Calcolo della colonna "Prodotto"**
    dati_preparati["Prodotto"] = dati_preparati["-log10(p-value)"] * dati_preparati["Log2FoldChange"]

    # **Salva i dati processati nel session_state**
    st.session_state["dati_processati"] = dati_preparati
