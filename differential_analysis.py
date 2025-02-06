import streamlit as st
from volcano_plot_app import mostra_volcano_plot
from table_app import mostra_tabella

# Configurazione della pagina Streamlit
st.set_page_config(page_title="Analisi Dati - Volcano Plot e Tabella", layout="wide")

# Sidebar per la selezione della modalità
st.sidebar.title("Navigazione")
sezione = st.sidebar.radio("Scegli una sezione:", ["Volcano Plot", "Tabella Dati"])

# Mostra la sezione selezionata
if sezione == "Volcano Plot":
    mostra_volcano_plot()
elif sezione == "Tabella Dati":
    mostra_tabella()
