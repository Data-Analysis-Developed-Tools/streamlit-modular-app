import streamlit as st
import pandas as pd

def mostra_tabella(dati, class_1, class_2):
    st.title("Tabella dei Dati")

    if dati is not None and not dati.empty:
        st.subheader(f"Dati filtrati: {class_1} vs {class_2}")
        st.dataframe(dati)

        # Download della tabella in formato CSV
        csv = dati.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Scarica tabella CSV", data=csv, file_name="dati_volcano_plot.csv", mime='text/csv')
    else:
        st.error("⚠️ Nessun dato disponibile per la visualizzazione.")
