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
    st.write("✅ Dati filtrati trovati in session_state.")

    dati = st.session_state["dati_filtrati"]
    classi = [st.session_state.get("class_1"), st.session_state.get("class_2")]

    # Controlla se le classi sono state selezionate
    if None in classi or len(classi) < 2:
        st.error("⚠️ Le classi non sono state selezionate correttamente.")
        return

    # Recupera i parametri impostati nella sidebar
    fold_change_threshold = st.session_state.get("fold_change_threshold", 0.0)
    p_value_threshold = st.session_state.get("p_value_threshold", 0.05)
    show_labels = st.sidebar.checkbox("Mostra etichette delle variabili", value=True)
    size_by_media = st.sidebar.checkbox("Dimensiona punti per media valori (n^MediaLog)", value=False)
    color_by_media = st.sidebar.checkbox("Colora punti per media valori", value=False)

    if size_by_media:
        n_base = st.sidebar.slider("Scegli la base dell'esponenziale (n)", min_value=1, max_value=25, value=10)
    else:
        n_base = None  

    st.write(f"📊 Soglie impostate: Log2FC={fold_change_threshold}, -log10(p-value)={p_value_threshold}")

    # Prepara i dati per il Volcano Plot
    try:
        dati_preparati = prepara_dati(dati, classi, fold_change_threshold, p_value_threshold)
        st.success("✅ Funzione `prepara_dati` eseguita correttamente.")  
    except Exception as e:
        st.error(f"❌ Errore in `prepara_dati`: {e}")
        return

    if dati_preparati is None or dati_preparati.empty:
        st.error("⚠️ Il dataframe 'dati_preparati' è vuoto! Controlla i parametri di filtraggio.")
        return

    # **Etichette per le classi**
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; margin-bottom: 12px; margin-top: 10px;">
        <h3 style="color: red; text-align: left;">🔴 Over-expression in {classi[1]}</h3>
        <h3 style="color: green; text-align: right;">🟢 Over-expression in {classi[0]}</h3>
    </div>
    """, unsafe_allow_html=True)

    # **Generazione del Volcano Plot**
    if size_by_media and n_base is not None:
        dati_preparati["SizeScaled"] = np.power(n_base, dati_preparati["MediaLog"])
    else:
        dati_preparati["SizeScaled"] = 0.0001  

    # Calcoliamo i limiti effettivi della scala
    x_min_raw, x_max_raw = dati_preparati['Log2FoldChange'].min(), dati_preparati['Log2FoldChange'].max()
    y_max_raw = dati_preparati['-log10(p-value)'].max()

    x_margin = abs(x_max_raw - x_min_raw) * 0.1  
    y_margin = y_max_raw * 0.01  

    x_min = min(x_min_raw, -fold_change_threshold * 1.2) - x_margin
    x_max = max(x_max_raw, fold_change_threshold * 1.2) + x_margin
    y_max = y_max_raw + y_margin  

    try:
        fig = px.scatter(dati_preparati, x='Log2FoldChange', y='-log10(p-value)', 
                         text='Variabile' if show_labels else None,
                         hover_data=['Variabile'],
                         color=dati_preparati['MediaLog'] if color_by_media else None,
                         size=dati_preparati['SizeScaled'],
                         color_continuous_scale='RdYlBu_r', size_max=10)

        fig.update_layout(
            xaxis=dict(range=[x_min, x_max]),
            yaxis=dict(range=[0, y_max]),  
            height=1000,
            margin=dict(l=150, r=150, t=200, b=100)
        )

        # **Ripristino delle linee di soglia**
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

        fig.add_trace(go.Scatter(x=[0, 0], 
                                 y=[0, y_max], 
                                 mode='lines', line=dict(color='lightgray', dash='dash', width=1.5),
                                 name="Log2FC = 0"))

        st.plotly_chart(fig)
        st.write("✅ Volcano Plot generato con successo!")
    except Exception as e:
        st.error(f"❌ Errore durante la generazione del Volcano Plot: {e}")

    # **Aggiunta della tabella con i criteri di filtraggio originali**
    st.subheader("🔎 Variabili che superano le soglie impostate")

    if "-log10(p-value)" in dati_preparati.columns and "Log2FoldChange" in dati_preparati.columns:
        variabili_significative = dati_preparati[
            (dati_preparati['-log10(p-value)'] > p_value_threshold) & 
            (abs(dati_preparati['Log2FoldChange']) > fold_change_threshold)
        ][['Variabile', '-log10(p-value)', 'Log2FoldChange']]

        if not variabili_significative.empty:
            st.dataframe(variabili_significative, use_container_width=True)
        else:
            st.write("❌ Nessuna variabile supera entrambe le soglie impostate.")
