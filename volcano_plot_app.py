import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from components.data_loader import prepara_dati


def mostra_volcano_plot():
    st.title("Volcano Plot Interattivo")

    if "dati_filtrati" not in st.session_state or st.session_state["dati_filtrati"] is None:
        st.error("⚠️ Nessun dato filtrato disponibile. Torna alla homepage e seleziona le classi.")
        return

    dati = st.session_state["dati_filtrati"]
    classi = [st.session_state.get("class_1"), st.session_state.get("class_2")]

    if None in classi:
        st.error("⚠️ Le classi non sono state selezionate correttamente.")
        return

    fold_change_threshold = st.session_state.get("fold_change_threshold", 0.0)
    p_value_threshold = st.session_state.get("p_value_threshold", 0.05)

    show_labels = st.sidebar.checkbox("Mostra etichette delle variabili", value=True)
    size_by_media = st.sidebar.checkbox("Dimensiona punti per media valori (n^MediaLog)", value=False)
    color_by_media = st.sidebar.checkbox("Colora punti per media valori", value=False)

    if size_by_media:
        n_base = st.sidebar.slider("Scegli la base dell'esponenziale (n)", min_value=1, max_value=25, value=10)
    else:
        n_base = None

    dati_preparati = prepara_dati(dati, classi, fold_change_threshold, p_value_threshold)

    if dati_preparati is None or dati_preparati.empty:
        st.error("⚠️ Il dataframe 'dati_preparati' è vuoto! Controlla i parametri di filtraggio.")
        return

    if "Variabile" in dati_preparati.columns:
        dati_preparati = dati_preparati.rename(columns={"Variabile": "EtichettaVariabile"})
    elif "etichette" in dati_preparati.columns:
        dati_preparati = dati_preparati.rename(columns={"etichette": "EtichettaVariabile"})

    if size_by_media and n_base is not None:
        dati_preparati["SizeScaled"] = np.power(n_base, dati_preparati["MediaLog"])
    else:
        dati_preparati["SizeScaled"] = 8  # default size

    # Calcola medie
    media_class_1 = dati[classi[0]].mean(axis=1)
    media_class_2 = dati[classi[1]].mean(axis=1)
    dati_preparati["MediaClasse1"] = media_class_1.values
    dati_preparati["MediaClasse2"] = media_class_2.values

    # Crea tooltip personalizzato
    def crea_tooltip(row):
        nome = f"<b style='font-size:16px'>{row['EtichettaVariabile']}</b><br>"
        if row['Log2FoldChange'] > 0:
            sopra = f"<span style='font-size:12px'>Media in {classi[0]}: {row['MediaClasse1']:.2f}</span><br>"
            sotto = f"<span style='font-size:12px'>Media in {classi[1]}: {row['MediaClasse2']:.2f}</span>"
        else:
            sopra = f"<span style='font-size:12px'>Media in {classi[1]}: {row['MediaClasse2']:.2f}</span><br>"
            sotto = f"<span style='font-size:12px'>Media in {classi[0]}: {row['MediaClasse1']:.2f}</span>"
        return nome + sopra + sotto

    dati_preparati["hover_text"] = dati_preparati.apply(crea_tooltip, axis=1)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dati_preparati["Log2FoldChange"],
        y=dati_preparati["-log10(p-value)"],
        mode="markers+text" if show_labels else "markers",
        text=dati_preparati["EtichettaVariabile"] if show_labels else None,
        textposition="top center",
        marker=dict(
            size=dati_preparati["SizeScaled"],
            color=dati_preparati["MediaLog"] if color_by_media else 'blue',
            colorscale='RdYlBu',
            showscale=color_by_media,
            colorbar=dict(title='MediaLog') if color_by_media else None
        ),
        hovertemplate=dati_preparati["hover_text"]
    ))

    fig.update_layout(
        xaxis_title="Log2 Fold Change",
        yaxis_title="-log10(p-value)",
        height=800
    )

    fig.add_shape(type='line', x0=-fold_change_threshold, x1=-fold_change_threshold, y0=0, y1=dati_preparati["-log10(p-value)"].max(),
                  line=dict(color='red', dash='dash'))
    fig.add_shape(type='line', x0=fold_change_threshold, x1=fold_change_threshold, y0=0, y1=dati_preparati["-log10(p-value)"].max(),
                  line=dict(color='red', dash='dash'))
    fig.add_shape(type='line', x0=dati_preparati["Log2FoldChange"].min(), x1=dati_preparati["Log2FoldChange"].max(),
                  y0=p_value_threshold, y1=p_value_threshold, line=dict(color='blue', dash='dash'))

    st.plotly_chart(fig, use_container_width=True)

    if fold_change_threshold != 0.0 or p_value_threshold != 0.05:
        st.subheader("🔎 Variabili che superano le soglie impostate")
        variabili_significative = dati_preparati[
            (dati_preparati['-log10(p-value)'] > p_value_threshold) &
            (abs(dati_preparati['Log2FoldChange']) > fold_change_threshold)
        ][['EtichettaVariabile', '-log10(p-value)', 'Log2FoldChange']]

        if not variabili_significative.empty:
            st.dataframe(variabili_significative, use_container_width=True)
        else:
            st.write("❌ Nessuna variabile supera entrambe le soglie impostate.")
