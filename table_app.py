import streamlit as st
import pandas as pd
import numpy as np  # ✅ Per il calcolo del p-value e Log2FoldChange

def mostra_tabella():
    st.title("Tabella Dati Filtrati")

    # Controlla se i dati filtrati esistono in session_state
    if "dati_filtrati" not in st.session_state or st.session_state["dati_filtrati"] is None:
        st.error("⚠️ Nessun dato filtrato disponibile. Torna alla homepage e seleziona le classi.")
        return
    st.write("✅ Dati filtrati trovati in session_state.")

    # Creiamo una copia dei dati per evitare modifiche indesiderate
    dati = st.session_state["dati_filtrati"].copy()

    # **Gestione Multi-Indice**
    if isinstance(dati.columns, pd.MultiIndex):
        st.write("🔍 Il dataset ha colonne Multi-Index. Le ristrutturiamo.")
        dati.columns = ["_".join(col).strip() for col in dati.columns.values]  # Concateniamo i livelli del MultiIndex

    # **Eliminiamo la prima riga che contiene le classi**
    dati = dati.iloc[1:].reset_index(drop=True)  # ✅ Rimuove la prima riga

    # **Mostra le colonne disponibili dopo la pulizia**
    st.write("📊 Colonne disponibili dopo la ristrutturazione:", dati.columns.tolist())

    # **Verifica che il dataset contenga dati validi**
    if dati.empty:
        st.error("⚠️ Il dataset filtrato è vuoto dopo la rimozione delle classi!")
        return

    # **Identificazione della colonna delle variabili**
    colonna_variabili = dati.columns[0]  # La prima colonna contiene i nomi delle variabili
    dati.rename(columns={colonna_variabili: "Variabile"}, inplace=True)  # Rinominiamo per chiarezza

    # **Selezioniamo le colonne numeriche corrette**
    colonne_numeriche = dati.select_dtypes(include=[np.number]).columns
    if len(colonne_numeriche) < 2:
        st.error("❌ Errore: Non ci sono abbastanza colonne numeriche per calcolare Log2FoldChange.")
        return

    # **Calcolo di Log2FoldChange**
    try:
        dati["Log2FoldChange"] = np.log2(dati[colonne_numeriche[0]] / dati[colonne_numeriche[1]])
    except Exception as e:
        st.error(f"❌ Errore nel calcolo di Log2FoldChange: {e}")
        return

    # **Calcolo di -log10(p-value) se non presente**
    if "-log10(p-value)" not in dati.columns:
        try:
            dati["-log10(p-value)"] = -np.log10(dati["p-value"])
        except KeyError:
            st.error("❌ Errore: Non è possibile calcolare -log10(p-value) perché manca la colonna 'p-value'.")
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
