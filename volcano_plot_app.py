import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from components.data_loader import prepara_dati

def mostra_volcano_plot():
    st.title("Volcano Plot Interattivo")

    # Controlla se i dati filtrati esistono in session_state
    if "dati_filtrati" not in st.session_state or st.session_state["dati_filtrati"] is None:
        st.error("⚠️ Nessun dato filtrato disponibile. Torna alla homepage e seleziona le classi.")
        return

    dati = st.session_state["dati_filtrati"]
    classi = [st.session_state.get("class_1"), st.session_state.get("class_2")]

    # Controlla se le classi sono state selezionate
    if None in classi:
        st.error("⚠️ Le classi non sono state selezionate correttamente.")
        return

    # Recupera i parametri impostati nella sidebar
    fold_change_threshold = st.session_state.get("fold_change_threshold", 0.0)
    p_value_threshold = st.session_state.get("p_value_threshold", 0.05)
    show_labels = st.sidebar.checkbox("Mostra etichette delle variabili", value=True)
    size_by_media = st.sidebar.checkbox("Dimensiona punti per media valori (n^MediaLog)", value=False)
    color_by_media = st.sidebar.checkbox("Colora punti per media valori", value=False)

    # Se "Dimensiona punti per media valori" è attivato, mostra il cursore per scegliere la base dell'esponenziale
    if size_by_media:
        n_base = st.sidebar.slider("Scegli la base dell'esponenziale (n)", min_value=1, max_value=25, value=10)
    else:
        n_base = None

    # Prepara i dati per il Volcano Plot
    try:
        dati_preparati = prepara_dati(dati, classi, fold_change_threshold, p_value_threshold)
    except Exception as e:
        st.error(f"❌ Errore in `prepara_dati`: {e}")
        return

    if dati_preparati is None or dati_preparati.empty:
        st.error("⚠️ Il dataframe 'dati_preparati' è vuoto! Controlla i parametri di filtraggio.")
        return

    # Calcolo della dimensione dei punti con n^MediaLog se l'opzione è attivata
    if size_by_media and n_base is not None:
        dati_preparati["SizeScaled"] = np.power(n_base, dati_preparati["MediaLog"])
    else:
        dati_preparati["SizeScaled"] = 0.0001

    # **Forzare l'estensione dell'asse verticale**
    y_max_original = dati_preparati['-log10(p-value)'].max()
    y_max_forzato = max(y_max_original * 3, 10)  # 🔥 Forza un'estensione 3x con un minimo di 10

    x_min = min(dati_preparati['Log2FoldChange'].min(), -fold_change_threshold * 1.2)
    x_max = max(dati_preparati['Log2FoldChange'].max(), fold_change_threshold * 1.2)

    # Generazione del Volcano Plot con scala dinamica
    try:
        fig = px.scatter(dati_preparati, x='Log2FoldChange', y='-log10(p-value)', 
                         text='Variabile' if show_labels else None,
                         hover_data=['Variabile'],
                         color=dati_preparati['MediaLog'] if color_by_media else None,
                         size=dati_preparati['SizeScaled'],
                         color_continuous_scale='RdYlBu_r', size_max=10)

        fig.update_layout(xaxis=dict(range=[x_min, x_max]), 
                          yaxis=dict(range=[0, y_max_forzato]))  # 🔥 **Forza l'estensione dell'asse verticale**

        # Linee di soglia Log2FoldChange
        fig.add_trace(go.Scatter(x=[-fold_change_threshold, -fold_change_threshold], 
                                 y=[0, y_max_forzato], 
                                 mode='lines', line=dict(color='red', dash='dash', width=2),
                                 name=f"-Log2FC soglia ({-fold_change_threshold})"))

        fig.add_trace(go.Scatter(x=[fold_change_threshold, fold_change_threshold], 
                                 y=[0, y_max_forzato], 
                                 mode='lines', line=dict(color='red', dash='dash', width=2),
                                 name=f"+Log2FC soglia ({fold_change_threshold})"))

        # Linea di soglia -log10(p-value)
        fig.add_trace(go.Scatter(x=[x_min, x_max], 
                                 y=[p_value_threshold, p_value_threshold], 
                                 mode='lines', line=dict(color='blue', dash='dash', width=2),
                                 name=f"Soglia -log10(p-value) ({p_value_threshold})"))

        # Aggiunta della linea verticale grigio chiaro a x=0 (asse Log2FoldChange)
        fig.add_trace(go.Scatter(x=[0, 0], 
                                 y=[0, y_max_forzato], 
                                 mode='lines', line=dict(color='lightgray', dash='dash', width=1.5),
                                 name="Log2FC = 0"))

        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"❌ Errore durante la generazione del Volcano Plot: {e}")

    # **Generazione della tabella solo se le soglie sono state modificate**
    if fold_change_threshold != 0.0 or p_value_threshold != 0.05:
        st.subheader("🔎 Variabili che superano le soglie impostate")
        
        # Filtriamo le variabili che superano entrambe le soglie
        variabili_significative = dati_preparati[
            (dati_preparati['-log10(p-value)'] > p_value_threshold) & 
            (abs(dati_preparati['Log2FoldChange']) > fold_change_threshold)
        ][['Variabile', '-log10(p-value)', 'Log2FoldChange']]

        if not variabili_significative.empty:
            st.dataframe(variabili_significative, use_container_width=True)
        else:
            st.write("❌ Nessuna variabile supera entrambe le soglie impostate.")
