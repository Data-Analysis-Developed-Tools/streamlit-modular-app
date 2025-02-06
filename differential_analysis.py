import pandas as pd
import openpyxl
import streamlit as st
import io

def filter_and_save_excel(uploaded_file, output_sheet="selected class"):
    """Filtra e salva le colonne non vuote nel file Excel caricato da Streamlit"""
    
    # Leggere il file direttamente dal buffer (senza salvarlo su disco)
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl')
    except Exception as e:
        st.error(f"Errore durante la lettura del file: {e}")
        return

    # Selezionare solo le colonne con meno del 90% di valori NaN
    threshold = 0.9 * len(df)
    selected_columns = df.loc[:, df.isnull().sum() < threshold]

    # Creare un nuovo buffer di memoria per salvare il file modificato
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl', mode='w') as writer:
        df.to_excel(writer, sheet_name="Original Data", index=False)  # Mantiene i dati originali
        selected_columns.to_excel(writer, sheet_name=output_sheet, index=False)

    # Spostare il puntatore all'inizio del buffer
    output.seek(0)

    # Offrire il file da scaricare all'utente
    st.download_button(label="📥 Scarica il file con i dati filtrati",
                       data=output,
                       file_name="filtered_data.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    st.success(f"✅ Colonne filtrate salvate nel foglio '{output_sheet}' e pronte per il download.")

# Interfaccia Streamlit
st.sidebar.title("Caricamento dati")
file = st.sidebar.file_uploader("Carica il file Excel", type=['xlsx'])

if file is not None:
    filter_and_save_excel(file)
