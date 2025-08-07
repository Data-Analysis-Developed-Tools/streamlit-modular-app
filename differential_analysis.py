import streamlit as st
import pandas as pd
import numpy as np

def differential_analysis(df, class_1, class_2):
    # Calcola media logaritmica e log2 fold change
    df_class_1 = df[df["Classe"] == class_1].drop("Classe", axis=1)
    df_class_2 = df[df["Classe"] == class_2].drop("Classe", axis=1)

    media_1 = df_class_1.mean()
    media_2 = df_class_2.mean()
    media_log = (media_1 + media_2) / 2

    # Aggiungi pseudocount per evitare divisione per zero
    pseudocount = 1e-9
    log2fc = np.log2((media_2 + pseudocount) / (media_1 + pseudocount))

    # Calcolo p-value con t-test (Welch)
    from scipy.stats import ttest_ind
    p_values = []
    for variabile in df_class_1.columns:
        _, p = ttest_ind(df_class_2[variabile], df_class_1[variabile], equal_var=False)
        p_values.append(p)

    # Crea DataFrame risultati
    risultati = pd.DataFrame({
        "Variabile": df_class_1.columns,
        "Log2FoldChange": log2fc.values,
        "pvalue": p_values,
        "MediaLog": media_log.values
    })

    return risultati


def run_analysis():
    st.title("Analisi Differenziale")

    uploaded_file = st.file_uploader("Carica il file Excel contenente i dati", type=["xlsx"])

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Errore nella lettura del file: {e}")
            return

        if df.shape[1] < 3:
            st.warning("Il file deve contenere almeno 3 colonne: EtichettaVariabile, Classe e almeno una variabile numerica.")
            return

        # Separazione delle colonne
        etichette = df.iloc[:, 0].astype(str)
        classi = df.iloc[:, 1]
        dati_numerici = df.iloc[:, 2:]

        # Ricostruzione DataFrame
        df_ristrutturato = dati_numerici.copy()
        df_ristrutturato["Classe"] = classi
        df_ristrutturato["EtichettaVariabile"] = etichette

        # Trasposizione per avere variabili come colonne
        df_trasposto = df_ristrutturato.set_index("EtichettaVariabile").transpose()
        df_trasposto["Classe"] = classi.values

        # Selezione delle classi
        classi_uniche = df_trasposto["Classe"].unique()
        class_1 = st.selectbox("Seleziona la prima classe", classi_uniche, key="class_1")
        class_2 = st.selectbox("Seleziona la seconda classe", [c for c in classi_uniche if c != class_1], key="class_2")

        if st.button("Esegui analisi differenziale"):
            with st.spinner("Analisi in corso..."):
                risultati = differential_analysis(df_trasposto, class_1, class_2)

                # Applica trasformazione -log10(p-value)
                risultati["-log10(p-value)"] = -np.log10(risultati["pvalue"])

                # Ripristina la colonna EtichettaVariabile correttamente
                risultati["EtichettaVariabile"] = risultati["Variabile"].astype(str)

                # ✅ Conversione esplicita in stringa
                risultati["EtichettaVariabile"] = risultati["EtichettaVariabile"].astype(str)

                st.session_state["dati_filtrati"] = risultati
                st.success("✅ Analisi completata! Vai alla sezione Volcano Plot.")
    else:
        st.info("📂 Carica un file Excel per iniziare.")
