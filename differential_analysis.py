import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from components.data_loader import carica_dati  # Importa la funzione di caricamento dati
from volcano_plot import mostra_volcano_plot  # Importa la funzione per il Volcano Plot
from table_display import mostra_tabella  # Importa la funzione per mostrare la tabella

# Configurazione della pagina
st.set_page_config(page_title="Volcano Plot e Tabella", layout="wide")

# Barra laterale di navigazione
st.sidebar.title("Navigazione")
selezione = st.sidebar.radio("Scegli una sezione:", ["Volcano Plot", "Tabella Dati"])

# **Caricamento del file**
file = st.sidebar.file_uploader("Carica il file Excel", type=['xlsx'])

if file is not None:
    # **Carica i dati e ottieni le classi**
    dati, classi = carica_dati(file)

    if dati is not None and len(classi) > 1:
        # **Selezione delle classi da confrontare**
        st.sidebar.subheader("Seleziona le classi da confrontare:")
        class_1 = st.sidebar.selectbox("Classe 1", classi)
        class_2 = st.sidebar.selectbox("Classe 2", classi)

        # **Bottone per avviare l'analisi**
        if st.sidebar.button("Procedi"):
            if class_1 and class_2 and class_1 != class_2:
                if selezione == "Volcano Plot":
                    mostra_volcano_plot(dati, class_1, class_2)
                elif selezione == "Tabella Dati":
                    mostra_tabella(dati, class_1, class_2)
            else:
                st.warning("⚠️ Seleziona due classi valide per procedere.")
    else:
        st.error("⚠️ Il file caricato non contiene abbastanza classi per il confronto.")
else:
    st.warning("⚠️ Carica un file Excel per iniziare.")
