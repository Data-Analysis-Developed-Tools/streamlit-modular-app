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
    # Carica i dati e li salva in session_state
    dati, classi = carica_dati()

    if dati is not None and len(classi) > 1:
        # Sidebar - Selezione delle classi
        st.sidebar.subheader("🔍 Seleziona le classi da confrontare:")
        class_1 = st.sidebar.selectbox("Classe 1", classi, key="classe1")
        class_2 = st.sidebar.selectbox("Classe 2", classi, key="classe2")

        # Tasto di conferma selezione
        if st.sidebar.button("✅ Conferma selezione"):
            if class_1 and class_2 and class_1 != class_2:
                # Filtrare i dati solo per le classi selezionate
                dati_filtrati = dati.loc[:, dati.columns.get_level_values(1).isin([class_1, class_2])]

                # Memorizzare i dati filtrati in session_state
                st.session_state["dati_filtrati"] = dati_filtrati
                st.session_state["class_1"] = class_1
                st.session_state["class_2"] = class_2

                st.sidebar.success("✅ Selezione confermata! Scegli un'analisi.")

    else:
        st.sidebar.warning("⚠️ Il file caricato non contiene abbastanza classi per l'analisi.")

# Dopo la conferma della selezione, abilitare la navigazione
if "dati_filtrati" in st.session_state:
    st.sidebar.title("📊 Navigazione")
    sezione = st.sidebar.radio("Scegli una sezione:", ["Volcano Plot", "Tabella Dati"])

    # Recuperare i dati filtrati dalla sessione
    dati_filtrati = st.session_state["dati_filtrati"]
    class_1 = st.session_state["class_1"]
    class_2 = st.session_state["class_2"]

    # Mostra la sezione selezionata con i dati filtrati
    if sezione == "Volcano Plot":
        mostra_volcano_plot(dati_filtrati, [class_1, class_2])
    elif sezione == "Tabella Dati":
        mostra_tabella(dati_filtrati, [class_1, class_2])
else:
    st.sidebar.info("🔹 Carica un file e seleziona due classi per procedere.")
