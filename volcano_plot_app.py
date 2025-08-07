import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def mostra_volcano_plot():
    st.title("🌋 Volcano Plot")

    # ✅ Recupera i dati filtrati da session_state
    dati_preparati = st.session_state.get("dati_preparati")

    if dati_preparati is None or dati_preparati.empty:
        st.warning("⚠️ Nessun dato disponibile per il Volcano Plot. Carica un file e seleziona due classi.")
        return

    # ✅ Rinominare prima colonna in 'EtichettaVariabile' se non già presente
    if "EtichettaVariabile" not in dati_preparati.columns:
        prima_colonna = dati_preparati.columns[0]
        dati_preparati = dati_preparati.rename(columns={prima_colonna: "EtichettaVariabile"})

    # Recupera i valori delle soglie dalla sidebar
    fold_change_threshold = st.session_state.get("fold_change_threshold", 1.0)
    p_value_threshold = st.session_state.get("p_value_threshold", 1.3)
    default_fold_change = 1.0
    default_p_value = 1.3

    # Tooltip personalizzato
    def genera_tooltip(riga):
        nome = f"<span style='font-size:16px'><b>{riga['EtichettaVariabile']}</b></span><br>"
        over = f"<span style='font-size:10px'>Sovraespresso: {riga.get('Media_Tesi_Sovra', 'N/A')}</span><br>"
        under = f"<span style='font-size:10px'>Sottoespresso: {riga.get('Media_Tesi_Sotto', 'N/A')}</span>"
        return nome + over + under

    # Applichiamo il tooltip
    if "Media_Tesi_Sovra" in dati_preparati.columns and "Media_Tesi_Sotto" in dati_preparati.columns:
        dati_preparati["tooltip"] = dati_preparati.apply(genera_tooltip, axis=1)
    else:
        dati_preparati["tooltip"] = dati_preparati["EtichettaVariabile"]

    # Colori in base alle soglie
    dati_preparati["colore"] = dati_preparati.apply(
        lambda r: "red" if r["Log2FoldChange"] > fold_change_threshold and r["-log10(p-value)"] > p_value_threshold
        else "blue" if r["Log2FoldChange"] < -fold_change_threshold and r["-log10(p-value)"] > p_value_threshold
        else "grey",
        axis=1
    )

    # 🎯 Volcano plot
    fig = px.scatter(
        dati_preparati,
        x="Log2FoldChange",
        y="-log10(p-value)",
        color="colore",
        hover_data={"colore": False, "tooltip": True, "EtichettaVariabile": False},
        custom_data=["tooltip"],
        labels={"Log2FoldChange": "Log2 Fold Change", "-log10(p-value)": "-log10(p-value)"},
        text=None  # 🚫 Disattiva visualizzazione etichette sul grafico
    )

    fig.update_traces(
        hovertemplate="%{customdata[0]}<extra></extra>",
        marker=dict(size=8)
    )

    fig.update_layout(
        showlegend=False,
        title="Volcano Plot personalizzato"
    )

    st.plotly_chart(fig, use_container_width=True)

    # 🔍 Mostra tabella sotto il grafico se soglie diverse dai default
    if fold_change_threshold != default_fold_change or p_value_threshold != default_p_value:
        st.subheader("🔎 Variabili che superano le soglie impostate")
        try:
            variabili_significative = dati_preparati[
                (dati_preparati['-log10(p-value)'] > p_value_threshold) &
                (abs(dati_preparati['Log2FoldChange']) > fold_change_threshold)
            ][['EtichettaVariabile', '-log10(p-value)', 'Log2FoldChange']]
            st.dataframe(variabili_significative)
        except KeyError as e:
            st.error(f"Errore: {e}")
