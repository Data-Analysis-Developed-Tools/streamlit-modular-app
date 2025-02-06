import streamlit as st
import pandas as pd
import numpy as np  # ✅ Per calcolare p-value

def mostra_tabella():
    st.title("Tabella Dati Filtrati")

    # Controlla se i dati filtrati esistono in session_state
    if "dati_filtrati" not in st.session_state or st.session_state["dati_filtrati"] is None:
        st.error("⚠️ Nessun dato filtrato disponibile. Torna alla homepage e seleziona le classi.")
        return
    st.write("✅ Dati filtrati trovati in session_state.")

    dati = st.session_state["dati_filtrati"]

    # Controlla se le colonne necessarie esistono nel dataframe
    colonne_necessarie = {"Variabile", "Log2FoldChange", "-log10(p-value)"}
    if not colonne_necessarie.issubset(dati.columns):
        st.error("⚠️ Il dataset non contiene tutte le colonne richieste.")
        return

    # **Calcolo delle nuove colonne**
    dati["p-value"] = np.power(10, -dati["-log10(p-value)"])  # ✅ Calcolo del p-value
    dati["Prodotto"] = dati["-log10(p-value)"] * dati["Log2FoldChange"]  # ✅ Prodotto

    # **Selezione delle colonne richieste**
    tabella_finale = dati[["Variabile", "Log2FoldChange", "-log10(p-value)", "p-value", "Prodotto"]]

    # **Mostra la tabella**
    st.dataframe(tabella_finale, use_container_width=True)
