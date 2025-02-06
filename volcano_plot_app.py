import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from components.data_loader import prepara_dati

# Recupera i parametri impostati nella sidebar
fold_change_threshold = st.session_state.get("fold_change_threshold", 0.0)
p_value_threshold = st.session_state.get("p_value_threshold", 0.05)

# Debug: Verifica che i valori vengano ricevuti
st.write(f"📡 Ricevuto in Volcano Plot - Log2FC: {fold_change_threshold}, -log10(p-value): {p_value_threshold}")

def mostra_volcano_plot():
    st.title("Volcano Plot Interattivo")

    # Controlla se i dati filtrati esistono in session_state
    if "dati_filtrati" not in st.session_state or st.session_state["dati_filtrati"] is None:
        st.error("⚠️ Nessun dato filtrato disponibile. Torna alla homepage e seleziona le classi.")
        return
    st.write("✅ Dati filtrati trovati in session_state.")

    dati = st.session_state["dati_filtrati"]
    classi = [st.session_state.get("class_1"), st.session_state.get("class_2")]

    # Controlla se le classi sono state selezionate
    if None in classi:
        st.error("⚠️ Le classi non sono state selezionate correttamente.")
        return
    st.write(f"📊 Generazione Volcano Plot per classi: {classi}")

    # Recupera i parametri impostati nella sidebar
    fold_change_threshold = st.session_state.get("fold_change_threshold", 0.0)
    p_value_threshold = st.session_state.get("p_value_threshold", 0.05)
    show_labels = st.sidebar.checkbox("Mostra etichette delle variabili", value=True)
    size_by_media = st.sidebar.checkbox("Dimensiona punti per media valori", value=False)
    color_by_media = st.sidebar.checkbox("Colora punti per media valori", value=False)

    st.write(f"📊 Soglie impostate: Log2FC={fold_change_threshold}, -log10(p-value)={p_value_threshold}")

    # Prepara i dati per il Volcano Plot
    try:
        dati_preparati = prepara_dati(dati, classi, fold_change_threshold, p_value_threshold)
        st.write("✅ Funzione `prepara_dati` eseguita correttamente.")
    except Exception as e:
        st.error(f"❌ Errore in `prepara_dati`: {e}")
        return

    if dati_preparati is None or dati_preparati.empty:
        st.error("⚠️ Il dataframe 'dati_preparati' è vuoto! Controlla i parametri di filtraggio.")
        return

    # Determina i limiti della scala in base ai dati filtrati
    x_min = min(dati_preparati['Log2FoldChange'].min(), -fold_change_threshold * 1.2)
    x_max = max(dati_preparati['Log2FoldChange'].max(), fold_change_threshold * 1.2)
    y_max = max(dati_preparati['-log10(p-value)'].max(), p_value_threshold * 1.2)

    # Generazione del Volcano Plot con scala dinamica
    try:
        fig = px.scatter(dati_preparati, x='Log2FoldChange', y='-log10(p-value)', 
                         text='Variabile' if show_labels else None,
                         hover_data=['Variabile'],
                         color=dati_preparati['MediaLog'] if color_by_media else None,
                         size=dati_preparati['MediaLog'] if size_by_media else None,
                         color_continuous_scale='RdYlBu_r', size_max=50)

        fig.update_layout(xaxis=dict(range=[x_min, x_max]), 
                          yaxis=dict(range=[0, y_max]))

        fig.add_trace(go.Scatter(x=[-fold_change_threshold, -fold_change_threshold], 
                                 y=[0, y_max], 
                                 mode='lines', line=dict(color='red', dash='dash', width=2),
                                 name=f"-Log2FC soglia ({-fold_change_threshold})"))

        fig.add_trace(go.Scatter(x=[fold_change_threshold, fold_change_threshold], 
                                 y=[0, y_max], 
                                 mode='lines', line=dict(color='red', dash='dash', width=2),
                                 name=f"+Log2FC soglia ({fold_change_threshold})"))

        fig.add_trace(go.Scatter(x=[x_min, x_max], 
                                 y=[p_value_threshold, p_value_threshold], 
                                 mode='lines', line=dict(color='blue', dash='dash', width=2),
                                 name=f"Soglia -log10(p-value) ({p_value_threshold})"))

        st.plotly_chart(fig)
        st.write("✅ Volcano Plot generato con successo!")
    except Exception as e:
        st.error(f"❌ Errore durante la generazione del Volcano Plot: {e}")
