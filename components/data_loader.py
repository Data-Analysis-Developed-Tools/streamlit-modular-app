import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

def carica_dati(file):
    try:
        dati = pd.read_excel(file, header=[0, 1], index_col=0)
        classi = dati.columns.get_level_values(1).unique()
        return dati, classi
    except Exception as e:
        return None, None

def prepara_dati(dati, classi, fold_change_threshold, p_value_threshold):
    risultati = []
    for var in dati.index:
        valori_1 = dati.loc[var, dati.columns.get_level_values(1) == classi[0]].dropna().values
        valori_2 = dati.loc[var, dati.columns.get_level_values(1) == classi[1]].dropna().values

        if len(valori_1) > 0 and len(valori_2) > 0:
            media_diff = np.log2(np.mean(valori_1) / np.mean(valori_2))
            t_stat, p_val = ttest_ind(valori_1, valori_2, equal_var=False)
            p_val_log = -np.log10(p_val) if p_val > 0 else None
            risultati.append([var, media_diff, p_val_log])

    return pd.DataFrame(risultati, columns=['Variabile', 'Log2FoldChange', '-log10(p-value)'])
