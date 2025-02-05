import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from table_app import mostra_tabella

import streamlit as st
from volcano_plot_app import mostra_volcano_plot
from table_app import mostra_tabella
from components.data_loader import carica_dati  # Importiamo la funzione di caricamento dati

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
        # **Selezione delle classi da confrontare senza valori di default**
        st.sidebar.subheader("Seleziona le classi da confrontare:")
        class_1 = st.sidebar.selectbox("Classe 1", ["Seleziona una classe"] + list(classi), index=0)
        class_2 = st.sidebar.selectbox("Classe 2", ["Seleziona una classe"] + list(classi), index=0)

        # **Controllo se l'utente ha selezionato due classi valide prima di procedere**
        if class_1 != "Seleziona una classe" and class_2 != "Seleziona una classe" and class_1 != class_2:
            if selezione == "Volcano Plot":
                mostra_volcano_plot(file, class_1, class_2)
            elif selezione == "Tabella Dati":
                mostra_tabella(file, class_1, class_2)
        else:
            st.warning("⚠️ Seleziona due classi diverse per procedere.")
    else:
        st.error("⚠️ Il file caricato non contiene abbastanza classi per il confronto.")
else:
    st.warning("⚠️ Carica un file Excel per iniziare.")
