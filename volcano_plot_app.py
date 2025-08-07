import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from components.data_loader import prepara_dati

def mostra_volcano_plot():
    st.title("Volcano Plot Interattivo")

    if "dati_filtrati" not in st.session_state or st.session_state["dati_filtrati"] is None:
        st.error("⚠️ Nessun dato filtrato disponibile. Torna alla homepage e seleziona le classi.")
        return
    st.write("✅ Dati filtrati trovati in session_state.")

    dati = st.session_state["dati_filtrati"]
    classi = [st.session_state.get("class_1"), st.session_state.get("class_2")]

    if None in classi:
        st.error("⚠️ Le classi non sono state selezionate correttamente.")
        return
    st.write(f"📊 Generazione Volcano Plot per classi: {classi}")

    default_fold_change = 0.0
    default_p_value = 0.05
    fold_change_threshold = st.session_state.get("fold_change_threshold", default_fold_change)
    p_value_threshold = st.session_state.get("p_value_threshold", default_p_value)

    size_by_media = st.sidebar.checkbox("Dimensiona punti per media valori (n^MediaLog)", value=False)
    color_by_media = st.sidebar.checkbox("Colora punti per media valori", value=False)

    if size_by_media:
        n_base = st.sidebar.slider("Scegli la base dell'esponenziale (n)", min_value=1, max_value=25, value=10)
    else:
        n_base = None  

    st.write(f"📊 Soglie impostate: Log2FC={fold_change_threshold}, -log10(p-value)={p_value_threshold}")

    try:
        dati_preparati = prepara_dati(dati, classi, fold_change_threshold, p_value_threshold)
        st.write("✅ Funzione `prepara_dati` eseguita correttamente.")
    except Exception as e:
        st.error(f"❌ Errore in `prepara_dati`: {e}")
        return

    if dati_preparati is None or dati_preparati.empty:
        st.error("⚠️ Il dataframe 'dati_preparati' è vuoto! Controlla i parametri di filtraggio.")
        return

    if size_by_media and n_base is not None:
        dati_preparati["SizeScaled"] = np.power(n_base, dati_preparati["MediaLog"])
    else:
        dati_preparati["SizeScaled"] = 0.0001  

    x_min = min(dati_preparati['Log2FoldChange'].min(), -fold_change_threshold * 1.2)
    x_max = max(dati_preparati['Log2FoldChange'].max(), fold_change_threshold * 1.2)
    y_max = max(dati_preparati['-log10(p-value)'].max(), p_value_threshold * 1.2)

    try:
        fig = px.scatter(
            dati_preparati,
            x='Log2FoldChange',
            y='-log10(p-value)',
            text=None,  # ❌ Etichette disattivate
            hover_data=['Variabile'],
            color=dati_preparati['MediaLog'] if color_by_media else None,
            size=dati_preparati['SizeScaled'],
            color_continuous_scale='RdYlBu_r',
            size_max=10
        )

        # Tooltip personalizzato
def crea_tooltip(riga):
    nome_var = f"<span style='font-size:16px'><b>{riga['etichettae']}</b></span><br>"
    over = f"<span style='font-size:10px'>Sovraespresso: {riga['Media_Tesi_Sovra']}</span><br>"
    under = f"<span style='font-size:10px'>Sottoespresso: {riga['Media_Tesi_Sotto']}</span>"
    return nome_var + over + under

# Crea una nuova colonna con il contenuto formattato
dati_preparati["tooltip"] = dati_preparati.apply(crea_tooltip, axis=1)

# Genera il Volcano Plot
fig = px.scatter(
    dati_preparati,
    x='Log2FoldChange',
    y='-log10(p-value)',
    color=dati_preparati['MediaLog'] if color_by_media else None,
    size=dati_preparati['SizeScaled'],
    custom_data=["tooltip"],
    color_continuous_scale='RdYlBu_r',
    size_max=10
)

fig.update_traces(
    hovertemplate="%{customdata[0]}<extra></extra>",
    marker=dict(size=8)
)

fig.update_layout(
    title="Volcano Plot",
    xaxis_title="Log2 Fold Change",
    yaxis_title="-log10(p-value)",
    showlegend=False,
    height=1000
)

st.plotly_chart(fig, use_container_width=True)

        fig.add_trace(go.Scatter(x=[-fold_change_threshold, -fold_change_threshold], 
                                 y=[0, y_max], 
                                 mode='lines', line=dict(color='red', dash='dash', width=2)))

        fig.add_trace(go.Scatter(x=[fold_change_threshold, fold_change_threshold], 
                                 y=[0, y_max], 
                                 mode='lines', line=dict(color='red', dash='dash', width=2)))

        fig.add_trace(go.Scatter(x=[x_min, x_max], 
                                 y=[p_value_threshold, p_value_threshold], 
                                 mode='lines', line=dict(color='blue', dash='dash', width=2)))

        fig.add_trace(go.Scatter(x=[0, 0], 
                                 y=[0, y_max], 
                                 mode='lines', line=dict(color='lightgray', dash='dash', width=1.5)))

        st.plotly_chart(fig)
        st.write("✅ Volcano Plot generato con successo!")
    except Exception as e:
        st.error(f"❌ Errore durante la generazione del Volcano Plot: {e}")
    
    if fold_change_threshold != default_fold_change or p_value_threshold != default_p_value:
        st.subheader("🔎 Variabili che superano le soglie impostate")
        variabili_significative = dati_preparati[
            (dati_preparati['-log10(p-value)'] > p_value_threshold) & 
            (abs(dati_preparati['Log2FoldChange']) > fold_change_threshold)
        ][['Variabile', '-log10(p-value)', 'Log2FoldChange']]

        if not variabili_significative.empty:
            st.dataframe(variabili_significative, use_container_width=True)
        else:
            st.write("❌ Nessuna variabile supera entrambe le soglie impostate.")
