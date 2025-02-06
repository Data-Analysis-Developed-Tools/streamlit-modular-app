import pandas as pd
import openpyxl

def filter_and_save_excel(input_file, output_sheet="selected class"):
    # Caricare il file Excel
    df = pd.read_excel(input_file, engine='openpyxl')
    
    # Selezionare solo le colonne con meno del 90% di valori NaN
    threshold = 0.9 * len(df)
    selected_columns = df.loc[:, df.isnull().sum() < threshold]
    
    # Salvare i dati filtrati in un nuovo foglio del file originale
    with pd.ExcelWriter(input_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        selected_columns.to_excel(writer, sheet_name=output_sheet, index=False)
    
    print(f"Colonne filtrate salvate nel file '{input_file}' nel foglio '{output_sheet}'.")

# Esempio di utilizzo
input_file = "dataset.xlsx"  # Sostituire con il proprio file Excel
filter_and_save_excel(input_file)
