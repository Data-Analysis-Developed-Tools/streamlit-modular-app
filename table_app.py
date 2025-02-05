import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def mostra_tabella(dati, class_1, class_2):
    """
    Funzione per mostrare la tabella con i dati ricevuti da differential_analysis.py.
    """
    st.title("Tabella dei Dati")
    
    if dati is not None and not dati.empty:
        st.subheader(f"Dati filtrati: {class_1} vs {class_2}")
        dati_filtrati = dati[(dati['Classe'] == class_1) | (dati['Classe'] == class_2)]
        
        if '-log10(p-value) x Log2FoldChange' in dati_filtrati.columns:
            norm = mcolors.TwoSlopeNorm(vmin=dati_filtrati['-log10(p-value) x Log2FoldChange'].min(),
                                        vcenter=0,
                                        vmax=dati_filtrati['-log10(p-value) x Log2FoldChange'].max())
            colormap = plt.cm.coolwarm
            
            st.dataframe(dati_filtrati.style.applymap(
                lambda x: f'background-color: {mcolors.to_hex(colormap(norm(x)))}',
                subset=['-log10(p-value) x Log2FoldChange']
            ))
            
            # Download della tabella in formato CSV
            csv = dati_filtrati.to_csv(index=False).encode('utf-8')
            st.download_button(label="📥 Scarica tabella CSV", data=csv, file_name="dati_volcano_plot.csv", mime='text/csv')
        else:
            st.error("⚠️ La colonna '-log10(p-value) x Log2FoldChange' non è presente nei dati!")
    else:
        st.error("⚠️ Nessun dato disponibile per la visualizzazione.")
