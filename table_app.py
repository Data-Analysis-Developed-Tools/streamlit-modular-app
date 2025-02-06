import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from components.data_loader import carica_dati, prepara_dati

def mostra_tabella():
    st.title("Tabella dei Dati")

    # Utilizza i dati filtrati dalla sessione di Streamlit
    dati, classi = carica_dati()

    if dati is not None:
        # Input per le soglie di filtraggio
        fold_change_threshold = st.number_input('Soglia Log2FoldChange', value=0.0)
        p_value_threshold = st.number_input('Soglia -log10(p-value)', value=0.05)

        # Preparazione dei dati per la tabella
        dati_preparati = prepara_dati(dati, classi, fold_change_threshold, p_value_threshold)

        if dati_preparati is not None and not dati_preparati.empty:
            st.write("Dati visibili attualmente nella tabella:")

            # Creazione di una colormap per la tabella
            norm = mcolors.TwoSlopeNorm(vmin=dati_preparati['-log10(p-value) x Log2FoldChange'].min(),
                                        vcenter=0,
                                        vmax=dati_preparati['-log10(p-value) x Log2FoldChange'].max())
            colormap = plt.cm.coolwarm

            # Visualizzazione della tabella con colori dinamici
            st.dataframe(dati_preparati.style.applymap(
                lambda x: f'background-color: {mcolors.to_hex(colormap(norm(x)))}',
                subset=['-log10(p-value) x Log2FoldChange']
            ))

            # Download della tabella in formato CSV
            csv = dati_preparati.to_csv(index=False).encode('utf-8')
            st.download_button(label="📥 Scarica tabella CSV",
                               data=csv,
                               file_name="dati_volcano_plot.csv",
                               mime='text/csv')
        else:
            st.error("⚠️ Il dataframe 'dati_preparati' è vuoto!")
    else:
        st.error("⚠️ Nessun dato filtrato disponibile. Carica un file e conferma la selezione delle classi.")
