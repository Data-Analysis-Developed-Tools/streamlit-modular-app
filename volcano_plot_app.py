import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from components.data_loader import prepara_dati

def mostra_volcano_plot():
    st.title("Volcano Plot Interattivo")

    # Recupera i dati filtrati dalla sessione
    if "dati_filtrati" in st.session_state and st.session_state["dati_filtrati"] is not None:
        dati = st.session_state["dati_filtrati"]
        classi = [st.session_state["class_1"], st.session_state["class_2"]]

        # Recupera i parametri impostati nella sidebar
        fold_change_threshold = st.session_state.get("fold_change_threshold", 0.0)
        p_value_threshold = st.session_state.get("p_value_threshold", 0.0)

        # Preparazione dei dati per il Volcano Plot
        dati_preparati = prepara_dati(dati, classi, fold_change_threshold, p_value_threshold)

        if dati_preparati is not None and not dati_preparati.empty:
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
        else:
            st.error("⚠️ Il dataframe 'dati_preparati' è vuoto!")
    else:
        st.error("⚠️ Nessun dato filtrato disponibile. Torna alla homepage e seleziona le classi.")
