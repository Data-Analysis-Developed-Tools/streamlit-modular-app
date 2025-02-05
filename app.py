import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from components.data_loader import carica_dati, prepara_dati

def mostra_tabella(file, class_1, class_2):
    st.title("Tabella dei Dati")

    if file is not None:
        dati, classi = carica_dati(file)  # Carica il dataset
        
        if dati is not None:
            # **Filtra solo le due classi selezionate**
            dati_filtrati = dati.loc[:, dati.columns.get_level_values(1).isin([class_1, class_2])]

            # Prepara i dati con le classi selezionate
            dati_preparati = prepara_dati(dati_filtrati, [class_1, class_2], 0.0, 0.05)

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
                st.error("⚠️ Nessun dato preparato per la tabella!")
        else:
            st.error("Dati non caricati correttamente.")
    else:
        st.warning("Carica un file Excel.")
