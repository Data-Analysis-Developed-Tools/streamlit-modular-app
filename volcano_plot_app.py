import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from components.data_loader import carica_dati, prepara_dati
def mostra_volcano_plot():
    st.title("Volcano Plot Interattivo")
    file = st.file_uploader("Carica il file Excel", type=['xlsx'])
    if file is not None:
        dati, classi = carica_dati(file)
        if dati is not None:
            fold_change_threshold = st.number_input('Soglia Log2FoldChange', value=0.0)
            p_value_threshold = st.number_input('Soglia -log10(p-value)', value=0.05)
            show_labels = st.checkbox("Mostra etichette delle variabili", value=True)
            size_by_media = st.checkbox("Dimensiona punti per media valori", value=False)
            color_by_media = st.checkbox("Colora punti per media valori", value=False)
            dati_preparati = prepara_dati(dati, classi, fold_change_threshold, p_value_threshold)
            if dati_preparati is not None and not dati_preparati.empty:
                fig = px.scatter(dati_preparati, x='Log2FoldChange', y='-log10(p-value)', text='Variabile' if show_labels else None,
                                 hover_data=['Variabile'], color=dati_preparati['MediaLog'] if color_by_media else None,
                                 size=dati_preparati['MediaLog'] if size_by_media else None,
                                 color_continuous_scale='RdYlBu_r', size_max=50)
                fig.add_trace(go.Scatter(x=[0, 0], y=[0, dati_preparati['-log10(p-value)'].max()], mode='lines', line=dict(color='orange', width=2)))
                fig.add_annotation(x=dati_preparati['Log2FoldChange'].min(), y=dati_preparati['-log10(p-value)'].max()*1.05,
                                   text=f"Over-expression in {classi[1]}", showarrow=False, font=dict(color="red", size=16), xanchor='left')
                fig.add_annotation(x=dati_preparati['Log2FoldChange'].max(), y=dati_preparati['-log10(p-value)'].max()*1.05,
                                   text=f"Over-expression in {classi[0]}", showarrow=False, font=dict(color="green", size=16), xanchor='right')
                st.plotly_chart(fig)
            else:
                st.error("⚠️ Il dataframe 'dati_preparati' è vuoto!")
        else:
            st.error("Dati non caricati correttamente.")
    else:
        st.warning("Si prega di caricare un file Excel.")
