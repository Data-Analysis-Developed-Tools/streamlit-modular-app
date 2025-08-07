import streamlit as st
import pandas as pd
import numpy as np

def carica_file():
    st.sidebar.header("📁 Carica il file Excel")
    file = st.sidebar.file_uploader("Scegli un file Excel", type=["xlsx"])

    if file is not None:
        try:
            df = pd.read_excel(file, header=0)
            df.rename(columns={df.columns[0]: "Variabile"}, inplace=True)
            df["Variabile"] = df["Variabile"].astype(str)
            df = df.dropna(subset=["Variabile"])  # Elimina righe con Variabile mancante
            st.session_state["dati_caricati"] = df
            st.success("✅ File caricato con successo!")
        except Exception as e:
            st.error(f"❌ Errore durante il caricamento del file: {e}")

def seleziona_classi(df):
    st.sidebar.header("🎯 Seleziona due classi da confrontare")
    colonne = df.columns[1:]

    classi = st.sidebar.multiselect("Scegli due classi", colonne, default=colonne[:2])

    if len(classi) != 2:
        st.warning("⚠️ Devi selezionare esattamente due classi.")
        return None, None
    return classi[0], classi[1]

def prepara_dati(df, classi, soglia_log2fc, soglia_pvalue):
    df = df.copy()

    media_1 = df[classi[0]].astype(float)
    media_2 = df[classi[1]].astype(float)

    df["Log2FoldChange"] = np.log2((media_2 + 1e-9) / (media_1 + 1e-9))
    df["MediaLog"] = np.log10((media_1 + media_2) / 2 + 1e-9)

    # Calcolo p-value con t-test a due campioni (semplificato)
    from scipy.stats import ttest_ind
    p_values = []
    for i in range(len(df)):
        val1 = media_1[i]
        val2 = media_2[i]
        _, p = ttest_ind([val1], [val2], equal_var=False)
        p_values.append(p)
    df["p-value"] = p_values
    df["-log10(p-value)"] = -np.log10(df["p-value"] + 1e-300)
    df["-log10(p-value) x Log2FoldChange"] = df["-log10(p-value)"] * df["Log2FoldChange"]

    df["Media_Classe_1"] = media_1
    df["Media_Classe_2"] = media_2

    return df

def mostra_homepage():
    st.title("🧪 Analisi Differenziale - Homepage")

    if "dati_caricati" not in st.session_state:
        st.info("📄 Carica un file Excel dalla barra laterale.")
        return

    df = st.session_state["dati_caricati"]
    st.subheader("📋 Anteprima dei dati")
    st.dataframe(df.head(), use_container_width=True)

    class_1, class_2 = seleziona_classi(df)
    if class_1 and class_2:
        st.session_state["class_1"] = class_1
        st.session_state["class_2"] = class_2

        st.sidebar.header("⚙️ Parametri di soglia")
        log2fc_threshold = st.sidebar.slider("Soglia Log2 Fold Change", 0.0, 5.0, 1.0, 0.1)
        pvalue_threshold = st.sidebar.slider("Soglia p-value", 0.0, 0.1, 0.05, 0.001)

        st.session_state["fold_change_threshold"] = log2fc_threshold
        st.session_state["p_value_threshold"] = -np.log10(pvalue_threshold)

        st.success("✅ Classi e soglie impostate. Ora puoi generare il Volcano Plot.")
