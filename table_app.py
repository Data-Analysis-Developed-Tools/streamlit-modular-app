import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

import sys
import os

# Aggiunta del percorso per garantire l'importazione corretta dei moduli personalizzati
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "components")))

from data_loader import carica_dati  # Importiamo la funzione di caricamento dati
from volcano_plot import mostra_volcano_plot  # Importa la funzione per generare il Volcano Plot

def mostra_tabella(dati, class_1, class_2):
    """
    Funzione per filtrare e mostrare la tabella con Streamlit.
    """
    if dati is not None:
        st.subheader(f"Tabella Dati: {class_1} vs {class_2}")
        dati_filtrati = dati[(dati['Classe'] == class_1) | (dati['Classe'] == class_2)]
        st.dataframe(dati_filtrati)  # Mostra la tabella filtrata
    else:
        st.error("⚠️ Nessun dato disponibile per la visualizzazione.")

# Configurazione della pagina
st.set_page_config(page_title="Volcano Plot e Tabella", layout="wide")

# Barra laterale di navigazione
st.sidebar.title("Navigazione")
selezione = st.sidebar.radio("Scegli una sezione:", ["Volcano Plot", "Tabella Dati"])

# **Caric
