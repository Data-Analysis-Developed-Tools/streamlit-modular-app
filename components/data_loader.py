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
    if dati is not None and len(classi) == 2:
        class_1, class_2 = classi  # Assumiamo che classi contenga solo le due selezionate
        
        # Filtriamo solo le colonne relative alle classi selezionate
        dati_filtrati = dati.loc[:, dati.columns.get_level_values(1).isin([class_1, class_2])]
        
        risultati = []
        for var in dati_filtrati.index:
            valori_1 = dati_filtrati.loc[var, dati_filtrati.columns.get_level_values(1) == class_1].dropna().values
            valori_2 = dati_filtrati.loc[var, dati_filtrati.columns.get_level_values(1) == class_2].dropna().values

            if len(valori_1) > 0 and len(valori_2) > 0:
                media_diff = np.log2(np.mean(valori_1) / np.mean(valori_2))
                t_stat, p_val = ttest_ind(valori_1, valori_2, equal_var=False)
                p_val_log = -np.log10(p_val) if p_val > 0 else None
                risultati.append([var, media_diff, p_val_log])

        risultati_df = pd.DataFrame(risultati, columns=['Variabile', 'Log2FoldChange', '-log10(p-value)'])
        
        if risultati_df.empty:
            return None
        
        return risultati_df
    else:
        return None
