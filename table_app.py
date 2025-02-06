import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from components.data_loader import prepara_dati

def mostra_tabella():
    st.title("Tabella dei Dati")

    # Controlla se i dati filtrati esistono in session_state
    if "dati_filtrati" in st.session_state and st.session_state["dati_filtrati"] is not None:
        dati = st.session_state["dati_filtrati"]
        classi = [st.session_state["class_1"], st.session_state["class_2"]]

        # Parametri di filtraggio
        fold_change_threshold = st.number_input('Soglia Log2FoldChange', value=0.0)
        p_value_threshold = st.number_input('Soglia -log10(p-value)', value=0.05)

        # Chiamata a prepara_dati
        from components.data_loader import prepara_dati
        dati_preparati = prepara_dati(dati, classi, fold_change_threshold, p_value_threshold)

        if dati_preparati is not None and not dati_preparati.empty:
            st.dataframe(dati_preparati)
        else:
            st.error("⚠️ Nessun dato disponibile per la tabella.")
    else:
        st.error("⚠️ Nessun dato filtrato disponibile. Torna alla homepage e seleziona le classi.")

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
        st.error("⚠️ Nessun dato filtrato disponibile. Torna alla homepage e seleziona le classi.")
