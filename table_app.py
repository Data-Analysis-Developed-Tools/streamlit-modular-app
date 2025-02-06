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

    # Creiamo una copia dei dati per evitare problemi con pandas
    dati = st.session_state["dati_filtrati"].copy()

    # **Verifica che il dataset contenga dati validi**
    if dati.empty:
        st.error("⚠️ Il dataset filtrato è vuoto!")
        return

    # **Controllo colonne disponibili**
    st.write("📊 Colonne disponibili nel dataset:", dati.columns.tolist())

    # **Calcolo di Log2FoldChange se le colonne sono presenti**
    try:
        colonne_numeriche = dati.select_dtypes(include=[np.number]).columns
        if len(colonne_numeriche) >= 2:
            # Prendiamo le prime due colonne numeriche per calcolare il Log2FoldChange
            dati["Log2FoldChange"] = np.log2(dati[colonne_numeriche[0]] / dati[colonne_numeriche[1]])
        else:
            st.error("❌ Errore: Non ci sono abbastanza colonne numeriche per calcolare Log2FoldChange.")
            return
    except Exception as e:
        st.error(f"❌ Errore nel calcolo di Log2FoldChange: {e}")
        return

    # **Calcolo di -log10(p-value) se non presente**
    if "-log10(p-value)" not in dati.columns:
        st.error("❌ Errore: la colonna '-log10(p-value)' non è presente nel dataset.")
        return

    # **Calcolo di p-value**
    try:
        dati["p-value"] = np.power(10, -dati["-log10(p-value)"])
    except Exception as e:
        st.error(f"❌ Errore nel calcolo del p-value: {e}")
        return

    # **Calcolo della colonna "Prodotto"**
    try:
        dati["Prodotto"] = dati["-log10(p-value)"] * dati["Log2FoldChange"]
    except Exception as e:
        st.error(f"❌ Errore nel calcolo del Prodotto: {e}")
        return

    # **Selezione delle colonne richieste**
    colonne_finali = ["Variabile", "Log2FoldChange", "-log10(p-value)", "p-value", "Prodotto"]
    tabella_finale = dati[colonne_finali]

    # **Mostra la tabella**
    st.dataframe(tabella_finale, use_container_width=True)
