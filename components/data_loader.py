import pandas as pd
import streamlit as st
import numpy as np
from scipy.stats import ttest_ind

# Funzione per caricare i dati
def carica_dati(file):
    try:
        dati = pd.read_excel(file, header=[0, 1], index_col=0)
        classi = dati.columns.get_level_values(1).unique()
        return dati, classi
    except Exception as e:
        st.error(f"Errore nel caricamento del file: {str(e)}")
        return None, None

# Funzione per calcolare la media logaritmica
def calcola_media_log(dati):
    media = dati.mean(axis=1)
    return np.log10(media + 1)  # Aggiunge 1 per evitare log di zero

# Funzione per preparare i dati per il Volcano Plot
def prepara_dati(dati, classi, fold_change_threshold, p_value_threshold):
    if dati is not None:
        media_log = calcola_media_log(dati.iloc[:, 1:])
        risultati = []
        for var in dati.index:
            valori = [dati.loc[var, dati.columns.get_level_values(1) == classe].dropna().values for classe in classi]
            if len(valori[0]) > 0 and len(valori[1]) > 0:
                media_diff = np.log2(np.mean(valori[0]) / np.mean(valori[1]))
                t_stat, p_val = ttest_ind(valori[0], valori[1], equal_var=False)
                p_val_log = -np.log10(p_val) if p_val > 0 else None
                pval_log2fc = p_val_log * media_diff if p_val_log is not None else None
                risultati.append([var, media_diff, p_val_log, pval_log2fc, media_log[var]])
        
        risultati_df = pd.DataFrame(risultati, columns=['Variabile', 'Log2FoldChange', '-log10(p-value)', '-log10(p-value) x Log2FoldChange', 'MediaLog'])
        return risultati_df
    else:
        st.error("Il dataframe non contiene un indice multi-livello come atteso.")
        return None

