from pathlib import Path

# Contenuto corretto del file differential_analysis.py (senza errori CSS)
contenuto_corretto = """import streamlit as st
import pandas as pd
import re  # 📌 Libreria per rimuovere i suffissi numerici

# 🚀 `st.set_page_config()` deve essere la PRIMA istruzione eseguita
st.set_page_config(page_title="Analisi Dati - Volcano Plot e Tabella", layout="wide")

from components.data_loader import carica_dati

# 🚀 Importiamo i moduli solo quando servono, evitando problemi
try:
    from volcano_plot_app import mostra_volcano_plot
    st.write("✅ Importazione di mostra_volcano_plot avvenuta con successo.")
except Exception as e:
    st.error(f"❌ Errore nell'import di mostra_volcano_plot: {e}")

try:
    from table_app import mostra_tabella
    st.write("✅ Importazione di mostra_tabella avvenuta con successo.")
except Exception as e:
    st.error(f"❌ Errore nell'import di mostra_tabella: {e}")

# Sidebar - Caricamento file
st.sidebar.title("📂 Caricamento Dati")
file = st.sidebar.file_uploader("Carica il file Excel", type=['xlsx'])

# Sidebar - Form per specificare i parametri di filtraggio
st.sidebar.subheader("⚙️ Parametri di filtraggio")
st.session_state["fold_change_threshold"] = st.sidebar.number_input("Soglia Log2FoldChange", value=0.0)
st.session_state["p_value_threshold"] = st.sidebar.number_input("Soglia -log10(p-value)", value=0.0)

# Debug: Visualizziamo i valori impostati nella sidebar
st.write(f"🔍 Valori soglia selezionati - Log2FC: {st.session_state['fold_change_threshold']}, -log10(p-value): {st.session_state['p_value_threshold']}")

# Controllo se il file è stato caricato
if file is not None:
    if "file_name" not in st.session_state or st.session_state["file_name"] != file.name:
        dati, classi_con_duplicate = carica_dati(file)

        # **📌 Rimuove i suffissi numerici (.1, .2, .3, ecc.) per evitare classi duplicate**
        classi_pulite = [re.sub(r'\\.\\d+$', '', classe) for classe in classi_con_duplicate]

        # **Rimuove eventuali duplicati causati dai suffissi**
        classi_uniche = list(set(classi_pulite))

        if dati is not None and len(classi_uniche) > 1:
            st.session_state["dati_completi"] = dati
            st.session_state["classi"] = classi_uniche
            st.session_state["file_name"] = file.name
            st.session_state["dati_filtrati"] = None
        else:
            st.sidebar.warning("⚠️ Il file caricato non contiene abbastanza classi per l'analisi.")
            st.stop()

    # Sidebar - Selezione delle classi
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

# Dopo la conferma della selezione, abilitare la navigazione
if "dati_filtrati" in st.session_state and st.session_state["dati_filtrati"] is not None:
    st.sidebar.title("📊 Navigazione")
    sezione = st.sidebar.radio("Scegli una sezione:", ["Volcano Plot", "Tabella Dati"])

    if sezione == "Volcano Plot":
        mostra_volcano_plot()
    elif sezione == "Tabella Dati":
        mostra_tabella()
else:
    st.sidebar.info("🔹 Carica un file e seleziona due classi per procedere.")
"""

# Scrivo il contenuto su file
file_path = Path("/mnt/data/differential_analysis.py")
file_path.write_text(contenuto_corretto)

file_path.name
