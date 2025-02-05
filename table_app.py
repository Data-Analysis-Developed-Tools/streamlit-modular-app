import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from components.data_loader import carica_dati, prepara_dati

def mostra_tabella():
    st.title("Tabella dei Dati")
    file = st.file_uploader("Carica il file Excel", type=['xlsx'])

    if file is not None:
        dati, classi = carica_dati(file)
        if dati is not None:
            fold_change_threshold = st.number_input('Soglia Log2FoldChange', value=0.0)
            p_value_threshold = st.number_input('Soglia -log10(p-value)', value=0.05)
            dati_preparati = prepara_dati(dati, classi, fold_change_threshold, p_value_threshold)

            if dati_preparati is not None and not dati_preparati.empty:
                st.write("Dati visibili attualmente nel grafico:")
                norm = mcolors.TwoSlopeNorm(vmin=dati_preparati['-log10(p-value) x Log2FoldChange'].min(),
                                            vcenter=0,
                                            vmax=dati_preparati['-log10(p-value) x Log2FoldChange'].max())
                colormap = plt.cm.coolwarm
                st.dataframe(dati_preparati.style.applymap(
                    lambda x: f'background-color: {mcolors.to_hex(colormap(norm(x)))}',
                    subset=['-log10(p-value) x Log2FoldChange']
                ))

                # Download della tabella in formato CSV
                csv = dati_preparati.to_csv(index=False).encode('utf-8')
                st.download_button(label="📥 Scarica tabella CSV", data=csv, file_name="dati_volcano_plot.csv", mime='text/csv')
            else:
                st.error("⚠️ Il dataframe 'dati_preparati' è vuoto!")
        else:
            st.error("Dati non caricati correttamente.")
    else:
        st.warning("Si prega di caricare un file Excel.")
