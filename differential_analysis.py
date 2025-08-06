import streamlit as st
from volcano_plot_app import mostra_volcano_plot
from table_app import mostra_tabella

# Titolo principale dell'app
st.set_page_config(page_title="Analisi Differenziale", layout="wide")
st.title("🔬 Analisi Differenziale Interattiva")

# Sidebar per selezione soglie
st.sidebar.header("🔧 Parametri di Filtraggio")

fold_change_threshold = st.sidebar.slider(
    label="Soglia Log2 Fold Change",
    min_value=0.0,
    max_value=5.0,
    value=1.0,
    step=0.1
)

p_value_threshold = st.sidebar.slider(
    label="Soglia -log10(p-value)",
    min_value=0.0,
    max_value=20.0,
    value=1.3,
    step=0.1
)

# Salva soglie nello stato globale (session_state)
st.session_state["fold_change_threshold"] = fold_change_threshold
st.session_state["p_value_threshold"] = p_value_threshold

# Sidebar per scelta sezione
sezione = st.sidebar.radio("📁 Scegli una sezione:", ["Volcano Plot", "Tabella Dati"])

# Mostra la sezione scelta
if sezione == "Volcano Plot":
    mostra_volcano_plot()
elif sezione == "Tabella Dati":
    mostra_tabella()
else:
    st.warning("❗ Seleziona una sezione dal menu laterale.")
