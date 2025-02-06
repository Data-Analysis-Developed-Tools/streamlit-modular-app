import streamlit as st
import pandas as pd
import numpy as np  # ✅ Per calcolare il p-value e altre metriche

def mostra_tabella():
    st.title("Tabella Dati Filtrati")

    # Controlla se i dati filtrati esistono in session_state
    if "dati_filtrati" not in st.session_state or st.session_state["dati_filtrati"] is None:
        st.error("⚠️ Nessun dato filtrato disponibile. Torna alla homepage e seleziona le classi.")
        return
    st.write("✅ Dati filtrati trovati in session_state.")

    dati = st.session_state["dati_filtrati"].copy()  # ✅ Creiamo una copia per evitare SettingWithCopyWarning

    # **Verifica che il dataset contenga dati validi**
    if dati.empty:
        st.error("⚠️ Il dataset filtrato è vuoto!")
        return

    # **Calcolo di Log2FoldChange e -log10(p-value)**
    try:
        dati.loc[:, "Log2FoldChange"] = np.log2(dati.iloc[:, 1] / dati.iloc[:, 2])  # ⚠️ Modifica se gli indici delle colonne non sono corretti
        dati.loc[:, "-log10(p-value)"] = -np.log10(dati["p-value"])
    except Exception as e:
        st.error(f"❌ Errore nel calcolo di Log2FoldChange e -log10(p-value): {e}")
        return

    # **Calcolo delle nuove colonne**
    dati.loc[:, "p-value"] = np.power(10, -dati["-log10(p-value)"])  # ✅ Calcolo del p-value
    dati.loc[:, "Prodotto"] = dati["-log10(p-value)"] * dati["Log2FoldChange"]  # ✅ Prodotto

    # **Selezione delle colonne richieste**
    colonne_finali = ["Variabile", "Log2FoldChange", "-log10(p-value)", "p-value", "Prodotto"]
    tabella_finale = dati[colonne_finali]

    # **Mostra la tabella**
    st.dataframe(tabella_finale, use_container_width=True)
