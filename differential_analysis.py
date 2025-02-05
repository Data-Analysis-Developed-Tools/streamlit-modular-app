import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from components.data_loader import carica_dati  # Importa la funzione di caricamento dati

# Configurazione della pagina
st.set_page_config(page_title="Volcano Plot e Tabella", layout="wide")

# Barra laterale di navigazione
st.sidebar.title("Navigazione")
selezione = st.sidebar.radio("Scegli una sezione:", ["Volcano Plot", "Tabella Dati"])

# **Caricamento del file**
file = st.sidebar.file_uploader("Carica il file Excel", type=['xlsx'])

def mostra_tabella(dati, class_1, class_2):
    """
    Funzione per filtrare e mostrare una tabella con Streamlit.
    """
    if dati is not None:
        st.subheader(f"Tabella Dati: {class_1} vs {class_2}")
        dati_filtrati = dati[(dati['Classe'] == class_1) | (dati['Classe'] == class_2)]
        st.dataframe(dati_filtrati)  # Mostra la tabella filtrata
    else:
        st.error("⚠️ Nessun dato disponibile per la visualizzazione.")

if file is not None:
    # **Carica i dati e ottieni le classi**
    dati, classi = carica_dati(file)

    if dati is not None and len(classi) > 1:
        # **Selezione delle classi da confrontare**
        st.sidebar.subheader("Seleziona le classi da confrontare:")
        class_1 = st.sidebar.selectbox("Classe 1", classi)
        class_2 = st.sidebar.selectbox("Classe 2", classi)

        # **Controllo se le classi sono state selezionate prima di procedere**
        if class_1 and class_2 and class_1 != class_2:
            if selezione == "Tabella Dati":
                mostra_tabella(dati, class_1, class_2)
        else:
            st.warning("⚠️ Seleziona due classi valide per procedere.")
    else:
        st.error("⚠️ Il file caricato non contiene abbastanza classi per il confronto.")
else:
    st.warning("⚠️ Carica un file Excel per iniziare.")
