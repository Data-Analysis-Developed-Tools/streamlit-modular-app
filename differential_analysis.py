import streamlit as st
from volcano_plot_app import mostra_volcano_plot
from table_app import mostra_tabella
from components.data_loader import carica_dati

# Configurazione della pagina Streamlit
st.set_page_config(page_title="Analisi Dati - Volcano Plot e Tabella", layout="wide")

# Sidebar - Caricamento del file
st.sidebar.title("📂 Caricamento Dati")
file = st.sidebar.file_uploader("Carica il file Excel", type=['xlsx'])

# Inizializzazione dei dati filtrati
dati_filtrati = None
class_1 = None
class_2 = None

if file is not None:
    # Carica i dati
    dati, classi = carica_dati(file)

    if dati is not None and len(classi) > 1:
        # Sidebar - Selezione delle classi
        st.sidebar.subheader("🔍 Seleziona le classi da confrontare:")
        class_1 = st.sidebar.selectbox("Classe 1", classi)
        class_2 = st.sidebar.selectbox("Classe 2", classi)

        if class_1 and class_2 and class_1 != class_2:
            # Filtrare i dati solo per le classi selezionate
            dati_filtrati = dati.loc[:, dati.columns.get_level_values(1).isin([class_1, class_2])]

            # Sidebar - Navigazione dopo la selezione delle classi
            st.sidebar.title("📊 Navigazione")
            sezione = st.sidebar.radio("Scegli una sezione:", ["Volcano Plot", "Tabella Dati"])

            # Mostra la sezione selezionata con i dati filtrati
            if sezione == "Volcano Plot":
                mostra_volcano_plot(dati_filtrati, [class_1, class_2])
            elif sezione == "Tabella Dati":
                mostra_tabella(dati_filtrati, [class_1, class_2])
        else:
            st.sidebar.warning("⚠️ Seleziona due classi diverse per procedere.")
    else:
        st.sidebar.warning("⚠️ Il file caricato non contiene abbastanza classi per l'analisi.")
else:
    st.sidebar.warning("⚠️ Carica un file Excel per iniziare.")
