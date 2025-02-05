import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))  # Aggiunge la directory corrente ai percorsi di ricerca

import streamlit as st
from volcano_plot_app import mostra_volcano_plot
from table_app import mostra_tabella

# Configurazione della pagina
st.set_page_config(page_title="Volcano Plot e Tabella", layout="wide")

# Barra di navigazione
st.sidebar.title("Navigazione")
selezione = st.sidebar.radio("Scegli una sezione:", ["Volcano Plot", "Tabella Dati"])

# Mostra la sezione selezionata
if selezione == "Volcano Plot":
    mostra_volcano_plot()
elif selezione == "Tabella Dati":
    mostra_tabella()
