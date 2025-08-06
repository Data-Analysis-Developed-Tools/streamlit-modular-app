import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def mostra_volcano_plot():
    st.title("Volcano Plot")

    uploaded_file = st.file_uploader("Carica il file Excel", type=["xlsx"])

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)

            expected_columns = ["Log2FoldChange", "p-value"]
            for col in expected_columns:
                if col not in df.columns:
                    st.error(f"Colonna mancante: '{col}'")
                    st.stop()

            if "MediaLog" not in df.columns:
                df["MediaLog"] = 1.0
            else:
                df["MediaLog"] = pd.to_numeric(df["MediaLog"], errors="coerce").fillna(1.0)

            if "NomeVariabile" not in df.columns:
                df["NomeVariabile"] = ""
            else:
                df["NomeVariabile"] = df["NomeVariabile"].fillna("")

            threshold_pvalue = 0.1
            threshold_log2fc = 1.0

            df["significant"] = (df["p-value"] < threshold_pvalue) & (abs(df["Log2FoldChange"]) > threshold_log2fc)

            st.sidebar.subheader("Opzioni di visualizzazione")
            mostra_etichette = st.sidebar.checkbox("Mostra etichette delle variabili")
            dimensiona_punti = st.sidebar.checkbox("Dimensiona punti per media valori (n^MediaLog)")
            colora_punti = st.sidebar.checkbox("Colora punti per media valori", value=True)

            st.success("✅ Funzione prepara_dati eseguita correttamente.")
            st.write("Numero di punti nel grafico:", df.shape[0])
            st.write(df.head())

            fig = px.scatter(
                df,
                x="Log2FoldChange",
                y=-np.log10(df["p-value"]),
                size=(df["MediaLog"] ** 1.2) if dimensiona_punti else None,
                color=df["MediaLog"] if colora_punti else None,
                hover_name="NomeVariabile",
                text=df["NomeVariabile"] if mostra_etichette else None,
                color_continuous_scale="RdYlBu_r",
                size_max=40,
            )

            fig.add_vline(x=threshold_log2fc, line_dash="dash", line_color="red")
            fig.add_vline(x=-threshold_log2fc, line_dash="dash", line_color="red")
            fig.add_hline(y=-np.log10(threshold_pvalue), line_dash="dash", line_color="blue")

            fig.update_traces(marker=dict(opacity=0.8), selector=dict(mode='markers'))
            fig.update_layout(
                height=600,
                width=1000,
                title={"text": "Volcano Plot", "x": 0.5, "xanchor": "center"},
                xaxis_title="Log2FoldChange",
                yaxis_title="-log10(p-value)"
            )

            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Errore durante l'elaborazione del file: {e}")
