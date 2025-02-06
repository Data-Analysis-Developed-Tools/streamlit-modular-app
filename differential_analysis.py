import streamlit as st
from volcano_plot_app import mostra_volcano_plot
from table_app import mostra_tabella
from components.data_loader import carica_dati

# Debug: Controlliamo se la funzione esiste
st.write("✅ Importazione di mostra_volcano_plot avvenuta con successo:", callable(mostra_volcano_plot))

# Configurazione della pagina Streamlit
st.set_page_config(page_title="Analisi Dati - Volcano Plot e Tabella", layout="wide")

# Sidebar - Caricamento del file
st.sidebar.title("📂 Caricamento Dati")
file = st.sidebar.file_uploader("Carica il file Excel", type=['xlsx'])

# Controllo se il file è stato caricato
if file is not None:
    if "file_name" not in st.session_state or st.session_state["file_name"] != file.name:
        dati, classi = carica_dati(file)
        if dati is not None and len(classi) > 1:
            st.session_state["dati_completi"] = dati
            st.session_state["classi"] = classi
            st.session_state["file_name"] = file.name
            st.session_state["dati_filtrati"] = None
        else:
            st.sidebar.warning("⚠️ Il file caricato non contiene abbastanza classi per l'analisi.")
            st.stop()

    # Sidebar - Selezione delle classi
    if "classi" in st.session_state:
        st.sidebar.subheader("🔍 Seleziona le classi da confrontare:")
        class_1 = st.sidebar.selectbox("Classe 1", st.session_state["classi"], key="classe1")
        class_2 = st.sidebar.selectbox("Classe 2", st.session_state["classi"], key="classe2")

        if st.sidebar.button("✅ Conferma selezione"):
            if class_1 and class_2 and class_1 != class_2:
                dati_filtrati = st.session_state["dati_completi"].loc[:, 
                    st.session_state["dati_completi"].columns.get_level_values(1).isin([class_1, class_2])]

                st.session_state["dati_filtrati"] = dati_filtrati
                st.session_state["class_1"] = class_1
                st.session_state["class_2"] = class_2

                st.sidebar.success("✅ Selezione confermata! Scegli un'analisi.")

# Sidebar - Form per specificare i parametri di filtraggio
st.sidebar.subheader("⚙️ Parametri di filtraggio")
st.session_state["fold_change_threshold"] = st.sidebar.number_input("Soglia Log2FoldChange", value=0.0)
st.session_state["p_value_threshold"] = st.sidebar.number_input("Soglia -log10(p-value)", value=0.0)

# Debug: Controlliamo se i dati filtrati esistono
st.write("🔎 Dati filtrati disponibili:", "dati_filtrati" in st.session_state)

if "dati_filtrati" in st.session_state and st.session_state["dati_filtrati"] is not None:
    st.sidebar.title("📊 Navigazione")
    sezione = st.sidebar.radio("Scegli una sezione:", ["Volcano Plot", "Tabella Dati"])

    if sezione == "Volcano Plot":
        st.write("📢 Chiamata a mostra_volcano_plot()...")  # Debug
        mostra_volcano_plot()
    elif sezione == "Tabella Dati":
        st.write("📢 Chiamata a mostra_tabella()...")  # Debug
        mostra_tabella()
else:
    st.sidebar.info("🔹 Carica un file e seleziona due classi per procedere.")
