import streamlit as st
from volcano_plot_app import mostra_volcano_plot
from table_app import mostra_tabella
from components.data_loader import carica_dati

# Configurazione della pagina Streamlit
st.set_page_config(page_title="Analisi Dati - Volcano Plot e Tabella", layout="wide")

# Sidebar - Caricamento del file
st.sidebar.title("📂 Caricamento Dati")
file = st.sidebar.file_uploader("Carica il file Excel", type=['xlsx'])

if file is not None:
    dati, classi = carica_dati(file)  # Carica i dati una sola volta

    if dati is not None and len(classi) > 1:
        # Sidebar - Selezione della modalità
        st.sidebar.title("🔍 Navigazione")
        sezione = st.sidebar.radio("Scegli una sezione:", ["Volcano Plot", "Tabella Dati"])

        # Mostra la sezione selezionata
        if sezione == "Volcano Plot":
            mostra_volcano_plot(dati, classi)
        elif sezione == "Tabella Dati":
            mostra_tabella(dati, classi)
    else:
        st.sidebar.warning("⚠️ Il file caricato non contiene abbastanza classi per l'analisi.")
else:
    st.sidebar.warning("⚠️ Carica un file Excel per iniziare.")
