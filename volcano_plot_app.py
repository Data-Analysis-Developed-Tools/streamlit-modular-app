import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def mostra_volcano_plot():
    st.title("Volcano Plot Interattivo")

    if "dati_filtrati" not in st.session_state or st.session_state["dati_filtrati"] is None:
        st.error("⚠️ Nessun dato filtrato disponibile. Torna alla homepage e seleziona le classi.")
        return
    st.write("✅ Dati filtrati trovati in session_state.")

    dati = st.session_state["dati_filtrati"]
    classi = [st.session_state.get("class_1"), st.session_state.get("class_2")]

    if None in classi or len(classi) < 2:
        st.error("⚠️ Le classi non sono state selezionate correttamente.")
        return

    fold_change_threshold = st.session_state.get("fold_change_threshold", 0.0)
    p_value_threshold = st.session_state.get("p_value_threshold", 0.0)

    show_labels = st.sidebar.checkbox("Mostra etichette delle variabili", value=True)
    size_by_media = st.sidebar.checkbox("Dimensiona punti per media valori (n^MediaLog)", value=False)
    color_by_media = st.sidebar.checkbox("Colora punti per media valori", value=False)

    if size_by_media:
        n_base = st.sidebar.slider("Scegli la base dell'esponenziale (n)", min_value=1, max_value=25, value=10)
    else:
        n_base = None

    st.write(f"📊 Soglie impostate: Log2FC={fold_change_threshold}, -log10(p-value)={p_value_threshold}")

    # Calcolo dei valori statistici
    try:
        medie = dati.groupby(level=1, axis=1).mean()
        media_log = medie.mean(axis=1)
        class_1, class_2 = classi
        fc = medie[class_2] - medie[class_1]
        p_valori = dati.apply(lambda row: t_test(row, class_1, class_2, dati.columns), axis=1)
        log2fc = fc
        neg_log10_p = -np.log10(p_valori)

        df_plot = pd.DataFrame({
            "Log2FoldChange": log2fc,
            "-log10(p-value)": neg_log10_p,
            "MediaLog": media_log
        })

        # 🔧 Usa la prima colonna del DataFrame originale per le etichette (come stringa)
        etichette = dati.index.astype(str)
        df_plot["Etichetta"] = etichette
    except Exception as e:
        st.error(f"❌ Errore in prepara_dati: {e}")
        return

    if size_by_media and n_base is not None:
        df_plot["SizeScaled"] = np.power(n_base, df_plot["MediaLog"])
    else:
        df_plot["SizeScaled"] = 0.0001  # minimo per rendere visibili i punti

    x_min_raw, x_max_raw = df_plot['Log2FoldChange'].min(), df_plot['Log2FoldChange'].max()
    y_max_raw = df_plot['-log10(p-value)'].max()
    x_margin = abs(x_max_raw - x_min_raw) * 0.1
    y_margin = y_max_raw * 0.01
    x_min = min(x_min_raw, -fold_change_threshold * 1.2) - x_margin
    x_max = max(x_max_raw, fold_change_threshold * 1.2) + x_margin
    y_max = y_max_raw + y_margin

# Assicura che la colonna delle etichette sia trattata come stringa
dati_preparati["EtichettaVariabile"] = dati_preparati.iloc[:, 0].astype(str)

fig = px.scatter(
    dati_preparati,
    x='Log2FoldChange',
    y='-log10(p-value)',
    text='EtichettaVariabile' if show_labels else None,
    hover_data=['EtichettaVariabile'],
    color=dati_preparati['MediaLog'] if color_by_media else None,
    size=dati_preparati['SizeScaled'],
    color_continuous_scale='RdYlBu_r',
    size_max=10
)


if show_labels:
    fig.update_traces(
        textposition='top center',
        textfont=dict(size=8),
        mode='markers+text'  # 🔥 necessario per rendere visibili le etichette
    )


    fig.update_layout(
        xaxis=dict(range=[x_min, x_max]),
        yaxis=dict(range=[0, y_max]),
        height=1000,
        margin=dict(l=150, r=150, t=200, b=100)
    )

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

    # Tabella dei dati significativi
    dati_significativi = df_plot[
        (abs(df_plot["Log2FoldChange"]) >= fold_change_threshold) &
        (df_plot["-log10(p-value)"] >= p_value_threshold)
    ]

    if not dati_significativi.empty:
        st.subheader("📋 Variabili Significative")
        st.dataframe(dati_significativi.sort_values("-log10(p-value)", ascending=False))
    else:
        st.info("🔹 Nessuna variabile supera entrambe le soglie selezionate.")

# Funzione per t-test (esempio semplificato, da sostituire con analisi reale)
def t_test(row, class_1, class_2, columns):
    from scipy.stats import ttest_ind
    idx_1 = [col for col in columns if col[1] == class_1]
    idx_2 = [col for col in columns if col[1] == class_2]
    return ttest_ind(row[idx_1], row[idx_2], equal_var=False).pvalue
