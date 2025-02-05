def prepara_dati(dati, classi, fold_change_threshold, p_value_threshold):
    if dati is not None and len(classi) == 2:
        class_1, class_2 = classi  # Assumiamo che classi contenga solo le due selezionate
        
        media_log = calcola_media_log(dati)  # Calcoliamo la media logaritmica su tutte le variabili

        risultati = []
        for var in dati.index:
            valori_1 = dati.loc[var, dati.columns.get_level_values(1) == class_1].dropna().values
            valori_2 = dati.loc[var, dati.columns.get_level_values(1) == class_2].dropna().values

            if len(valori_1) > 0 and len(valori_2) > 0:
                media_diff = np.log2(np.mean(valori_1) / np.mean(valori_2))
                t_stat, p_val = ttest_ind(valori_1, valori_2, equal_var=False)
                p_val_log = -np.log10(p_val) if p_val > 0 else None
                pval_log2fc = p_val_log * media_diff if p_val_log is not None else None

                risultati.append([var, media_diff, p_val_log, pval_log2fc, media_log[var]])
        
        risultati_df = pd.DataFrame(risultati, columns=['Variabile', 'Log2FoldChange', '-log10(p-value)', '-log10(p-value) x Log2FoldChange', 'MediaLog'])
        return risultati_df
    else:
        st.error("⚠️ Il dataframe è vuoto o non contiene le due classi selezionate.")
        return None
