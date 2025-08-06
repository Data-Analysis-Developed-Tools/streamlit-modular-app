import streamlit as st
import pandas as pd
import re  # 📌 Libreria per rimuovere i suffissi numerici

# 🚀 `st.set_page_config()` deve essere la PRIMA istruzione eseguita
st.set_page_config(page_title="Analisi Dati - Volcano Plot e Tabella", layout="wide")

# 🚀 Importiamo i moduli solo quando servono, evitando problemi
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
        # ✅ Legge il file saltando le prime 2 righe
        raw_df = pd.read_excel(file, header=[0, 1], skiprows=[0])

        # ✅ Rimuove la colonna Unnamed: 0 se presente
        if "Unnamed: 0" in raw_df.columns.get_level_values(0):
            raw_df = raw_df.drop(columns="Unnamed: 0")

        # ✅ Inserisce la colonna "etichette" come copia della prima colonna dati
        raw_df.insert(0, "etichette", raw_df.iloc[:, 0].values)

        # ✅ Rinomina le colonne Unnamed per evitare problemi
        new_cols = []
        for col in raw_df.columns:
            if isinstance(col, tuple):
                col_name = col[1] if col[0].startswith("Unnamed") else f"{col[0]}_{col[1]}"
                new_cols.append(col_name)
            else:
                new_cols.append(col)
        raw_df.columns = new_cols

        # ✅ Ricava le classi a partire dalla riga 2 del file originale (indice 1 di header)
        classi_con_duplicate = [c for c in raw_df.columns if c not in ["etichette"]]

        # **📌 Rimuove i suffissi numerici (.1, .2, .3, ecc.) per evitare classi duplicate**
        classi_pulite = [re.sub(r'\.\d+$', '', str(classe)) for classe in classi_con_duplicate]

        # **Rimuove eventuali duplicati causati dai suffissi**
        classi_uniche = list(set(classi_pulite))

        if raw_df is not None and len(classi_uniche) > 1:
            st.session_state["dati_completi"] = raw_df
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
                dati_filtrati = st.session_state["dati_completi"][["etichette", class_1, class_2]]
                st.session_state["dati_filtrati"] = dati_filtrati
                st.session_state["class_1"] = class_1
                st.session_state["class_2"] = class_2
                st.sidebar.success("✅ Selezione confermata! Scegli un'analisi.")
            else:
                st.sidebar.warning("⚠️ Seleziona due classi distinte.")

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
