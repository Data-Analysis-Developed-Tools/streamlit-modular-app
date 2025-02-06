import streamlit as st
import pandas as pd
import numpy as np
from components.data_loader import carica_dati

# **Caricamento del file**
file = st.sidebar.file_uploader("Carica il file Excel", type=['xlsx'])

if file is not None:
    # **Carica i dati e ottieni le classi**
    dati, classi = carica_dati(file)

    if dati is not None and len(classi) > 1:
        # **Selezione delle classi da confrontare senza valori di default**
        class_1 = st.sidebar.selectbox("Classe 1", [""] + list(classi))
        class_2 = st.sidebar.selectbox("Classe 2", [""] + list(classi))

        # **Controllo se le classi sono state selezionate prima di procedere**
        if class_1 and class_2 and class_1 != class_2:
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
