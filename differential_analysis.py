import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Analisi Dati - Volcano Plot e Tabella", layout="wide")

# Import moduli con gestione errori
try:
    from volcano_plot_app import mostra_volcano_plot
    st.write("✅ Importazione di mostra_volcano_plot avvenuta con successo.")
except Exception as e:
    st.error(f"❌ Errore nell'import di mostra_volcano_plot: {e}")
    def mostra_volcano_plot():
        st.error("❌ La funzione `mostra_volcano_plot()` non è disponibile.")

try:
    from table_app import mostra_tabella
    st.write("✅ Importazione di mostra_tabella avvenuta con successo.")
except Exception as e:
    st.error(f"❌ Errore nell'import di mostra_tabella: {e}")
    def mostra_tabella():
        st.error("❌ La funzione `mostra_tabella()` non è disponibile.")

# Sidebar - Caricamento
st.sidebar.title("📂 Caricamento Dati")
file = st.sidebar.file_uploader("Carica il file Excel", type=['xlsx'])

# Sidebar - Parametri di filtraggio
st.sidebar.subheader("⚙️ Parametri di filtraggio")
st.session_state["fold_change_threshold"] = st.sidebar.number_input("Soglia Log2FoldChange", value=0.0)
st.session_state["p_value_threshold"] = st.sidebar.number_input("Soglia -log10(p-value)", value=0.0)

st.write(f"🔍 Valori soglia selezionati - Log2FC: {st.session_state['fold_change_threshold']}, -log10(p-value): {st.session_state['p_value_threshold']}")

# Caricamento file
if file is not None:
    if "file_name" not in st.session_state or st.session_state["file_name"] != file.name:
        try:
            # 👇 Legge le prime 2 righe per header multi-livello
            df = pd.read_excel(file, header=[0, 1])

            # 👇 Prende la prima colonna (variabili) e la imposta come indice
            df.index = df.iloc[:, 0]
            df = df.iloc[:, 1:]

            # 👇 Elimina colonne indesiderate
            df = df.loc[:, ~df.columns.get_level_values(0).str.contains("Unnamed", na=False)]

            # 👇 Estrae le classi dal secondo livello del MultiIndex
            classi_con_duplicate = df.columns.get_level_values(1).tolist()
            classi_pulite = [re.sub(r'\.\d+$', '', str(cl)) for cl in classi_con_duplicate]
            classi_uniche = sorted(list(set(classi_pulite)))

            if df is not None and len(classi_uniche) > 1:
                st.session_state["dati_completi"] = df
                st.session_state["classi"] = classi_uniche
                st.session_state["file_name"] = file.name
                st.session_state["dati_filtrati"] = None
            else:
                st.sidebar.warning("⚠️ Il file caricato non contiene abbastanza classi.")
                st.stop()
        except Exception as e:
            st.error(f"❌ Errore durante la lettura del file: {e}")
            st.stop()

    # Sidebar - Selezione classi
    if "classi" in st.session_state:
        st.sidebar.subheader("🔍 Seleziona le classi da confrontare:")
        class_1 = st.sidebar.selectbox("Classe 1", sorted(st.session_state["classi"]), key="classe1")
        class_2 = st.sidebar.selectbox("Classe 2", sorted(st.session_state["classi"]), key="classe2")

        if st.sidebar.button("✅ Conferma selezione"):
            if class_1 and class_2 and class_1 != class_2:
                dati_filtrati = st.session_state["dati_completi"].loc[:, 
                    st.session_state["dati_completi"].columns.get_level_values(1).isin([class_1, class_2])]

                st.session_state["dati_filtrati"] = dati_filtrati
                st.session_state["class_1"] = class_1
                st.session_state["class_2"] = class_2

                st.sidebar.success("✅ Selezione confermata! Scegli un'analisi.")

# Navigazione
if "dati_filtrati" in st.session_state and st.session_state["dati_filtrati"] is not None:
    st.sidebar.title("📊 Navigazione")
    sezione = st.sidebar.radio("Scegli una sezione:", ["Volcano Plot", "Tabella Dati"])

    if sezione == "Volcano Plot":
        mostra_volcano_plot()
    elif sezione == "Tabella Dati":
        mostra_tabella()
else:
    st.sidebar.info("🔹 Carica un file e seleziona due classi per procedere.")
