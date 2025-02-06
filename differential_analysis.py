import pandas as pd
import openpyxl
import streamlit as st

def filter_and_save_excel(uploaded_file, output_sheet="selected class"):
    """Filtra e salva le colonne non vuote nel file Excel caricato da Streamlit"""
    
    # Caricare il file direttamente dal buffer senza salvarlo su disco
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    
    # Selezionare solo le colonne con meno del 90% di valori NaN
    threshold = 0.9 * len(df)
    selected_columns = df.loc[:, df.isnull().sum() < threshold]
    
    # Creare un buffer per salvare il file Excel modificato
    with pd.ExcelWriter(uploaded_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        selected_columns.to_excel(writer, sheet_name=output_sheet, index=False)
    
    st.success(f"✅ Colonne filtrate salvate nel foglio '{output_sheet}'.")

# Streamlit UI
st.sidebar.title("Caricamento dati")
file = st.sidebar.file_uploader("Carica il file Excel", type=['xlsx'])

if file is not None:
    filter_and_save_excel(file)
