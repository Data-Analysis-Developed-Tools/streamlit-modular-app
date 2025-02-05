import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def mostra_tabella(dati, class_1, class_2):
    """
    Funzione per mostrare la tabella con i dati ricevuti da differential_analysis.py.
    """
    st.title("Tabella dei Dati")
    
    if dati is None or dati.empty:
        st.error("⚠️ Il DataFrame è vuoto. Controlla il caricamento del file.")
        return
    
    # Controlla i nomi delle colonne disponibili
    st.write("Colonne disponibili nel DataFrame:", dati.columns.tolist())

    # Verifica se la colonna 'Classe' esiste o se ha un nome simile
    colonna_classe = "Classe"
    if colonna_classe not in dati.columns:
        colonna_classe = [str(col).lower() for col in dati.columns if "class" in str(col).lower()]
        if colonna_classe:
            colonna_classe = colonna_classe[0]  # Usa il primo match trovato
        else:
            st.error("⚠️ Nessuna colonna corrispondente a 'Classe' trovata nel dataset.")
            return

    # Filtra i dati solo per le classi selezionate
    st.subheader(f"Dati filtrati: {class_1} vs {class_2}")
    dati_filtrati = dati[(dati[colonna_classe] == class_1) | (dati[colonna_classe] == class_2)]
    
    if '-log10(p-value) x Log2FoldChange' in dati_filtrati.columns:
        norm = mcolors.TwoSlopeNorm(vmin=dati_filtrati['-log10(p-value) x Log2FoldChange'].min(),
                                    vcenter=0,
                                    vmax=dati_filtrati['-log10(p-value) x Log2FoldChange'].max())
        colormap = plt.cm.coolwarm
        
        st.dataframe(dati_filtrati.style.applymap(
