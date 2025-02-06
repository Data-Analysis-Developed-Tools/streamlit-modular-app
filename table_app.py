import streamlit as st
import pandas as pd
import numpy as np
from components.data_loader import carica_dati

def processa_dati():
    if "dati_filtrati" not in st.session_state or st.session_state["dati_filtrati"] is None:
        return  # Se non ci sono dati filtrati, non fa nulla

    dati = st.session_state["dati_filtrati"]
    classi = [st.session_state.get("class_1"), st.session_state.get("class_2")]

    if None in classi:
        return  # Se le classi non sono selezionate, non fa nulla

    # **Filtra solo le colonne delle classi selezionate**
    dati_filtrati = dati.loc[:, dati.columns.get_level_values(1).isin([class_1, class_2])]

    # **Calcolo di Log2FoldChange**
    colonne_numeriche = dati_filtrati.select_dtypes(include=[np.number]).columns
    if len(colonne_numeriche) >= 2:
        dati_filtrati["Log2FoldChange"] = np.log2(dati_filtrati[colonne_numeriche[0]] / dati_filtrati[colonne_numeriche[1]])

    # **Calcolo di -log10(p-value)**
    if "p-value" in dati_filtrati.columns:
        dati_filtrati["-log10(p-value)"] = -np.log10(dati_filtrati["p-value"])

    # **Salva i dati processati nel session_state**
    st.session_state["dati_processati"] = dati_filtrati
