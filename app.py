import streamlit as st
import pandas as pd
from volcano_plot_app import mostra_volcano_plot
from table_app import mostra_tabella
from components.data_loader import carica_dati  # Importa la funzione di caricamento dati

# Configurazione della pagina
st.set_page_config(page_title="Volcano Plot e Tabella", layout="wide")

# Barra laterale di navigazione
st.sidebar.title("Navigazione")
selezione = st.sidebar.radio("Scegli una sezione:", ["Volcano Plot", "Tabella Dati"])

# Caricamento del file
file = st.sidebar.file_uploader("Carica il file Excel", type=['xlsx'])

if file is not None:
    dati, classi = carica_dati(file)  # Carica il dataset e ottieni le classi uniche
    if dati is not None:
        # **Menu a tendina per selezionare le due classi**
        st.sidebar.subheader("Seleziona le classi da confrontare:")
        class_1 = st.sidebar.selectbox("Classe 1", classi, index=0)
        class_2 = st.sidebar.selectbox("Classe 2", classi, index=1)

        # Mostra la sezione selezionata, passando le classi selezionate
        if selezione == "Volcano Plot":
            mostra_volcano_plot(file, class_1, class_2)
        elif selezione == "Tabella Dati":
            mostra_tabella(file, class_1, class_2)

else:
    st.warning("⚠️ Carica un file Excel per iniziare.")
