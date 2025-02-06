import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from components.data_loader import prepara_dati

def mostra_volcano_plot():
    st.title("Volcano Plot Interattivo")

    # Recupera i dati filtrati dalla sessione
    if "dati_filtrati" not in st.session_state or st.session_state["dati_filtrati"] is None:
        st.error("⚠️ Nessun dato filtrato disponibile. Torna alla homepage e seleziona le classi.")
        return
    st.write("✅ Dati filtrati trovati in session_state.")

    dati = st.session_state["dati_filtrati"]
    classi = [st.session_state.get("class_1"), st.session_state.get("class_2")]

    # Recupera i parametri impostati nella sidebar
    fold_change_threshold = st.session_state.get("fold_change_threshold", 0.0)
    p_value_threshold = st.session_state.get("p_value_threshold", 0.0)
    st.write(f"📊 Generazione Volcano Plot con soglie: Log2FC={fold_change_threshold}, p-value={p_value_threshold}")

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

    # Generazione del Volcano Plot
    try:
        fig = px.scatter(dati_preparati, 
                         x='Log2FoldChange', 
                         y='-log10(p-value)', 
                         text='Variabile', 
                         hover_data=['Variabile'])

        fig.add_trace(go.Scatter(x=[0, 0], 
                                 y=[0, dati_preparati['-log10(p-value)'].max()], 
                                 mode='lines', line=dict(color='orange', width=2)))

        fig.add_annotation(x=dati_preparati['Log2FoldChange'].min(), 
                           y=dati_preparati['-log10(p-value)'].max()*1.05,
                           text=f"Over-expression in {classi[1]}", 
                           showarrow=False, font=dict(color="red", size=16), xanchor='left')

        fig.add_annotation(x=dati_preparati['Log2FoldChange'].max(), 
                           y=dati_preparati['-log10(p-value)'].max()*1.05,
                           text=f"Over-expression in {classi[0]}", 
                           showarrow=False, font=dict(color="green", size=16), xanchor='right')

        st.plotly_chart(fig)
        st.write("✅ Volcano Plot generato con successo!")
    except Exception as e:
        st.error(f"❌ Errore durante la generazione del Volcano Plot: {e}")
