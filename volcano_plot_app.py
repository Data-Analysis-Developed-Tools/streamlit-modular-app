import streamlit as st
import pandas as pd
import plotly.express as px

def mostra_volcano_plot():
    st.title("🌋 Volcano Plot")

    # Caricamento file
    file_caricato = st.file_uploader("Carica un file Excel", type=["xlsx"])
    if file_caricato is None:
        st.warning("📂 Carica un file per visualizzare il Volcano Plot.")
        return

    # Leggi il file
    try:
        dati = pd.read_excel(file_caricato)
    except Exception as e:
        st.error(f"Errore durante la lettura del file: {e}")
        return

    # Rinominare la prima colonna in 'EtichettaVariabile' se non già presente
    if "EtichettaVariabile" not in dati.columns:
        prima_colonna = dati.columns[0]
        dati = dati.rename(columns={prima_colonna: "EtichettaVariabile"})

    # Calcoli
    try:
        dati["-log10(p-value)"] = -np.log10(dati["p-value"])
    except Exception as e:
        st.error("Errore nel calcolo del -log10(p-value). Assicurati che esista la colonna 'p-value'.")
        return

    # Selezione soglie
    st.sidebar.header("🎚️ Filtri Volcano Plot")
    default_fold_change = 1.0
    default_p_value = 1.3
    fold_change_threshold = st.sidebar.slider("Soglia Log2FoldChange", 0.0, 5.0, default_fold_change, step=0.1)
    p_value_threshold = st.sidebar.slider("Soglia -log10(p-value)", 0.0, 10.0, default_p_value, step=0.1)

    # Tooltip personalizzato
    def genera_tooltip(riga):
        nome_var = f"<span style='font-size:16px'><b>{riga['EtichettaVariabile']}</b></span><br>"
        over = f"<span style='font-size:10px'>Sovraespresso: {riga['Media_Tesi_Sovra']}</span><br>"
        under = f"<span style='font-size:10px'>Sottoespresso: {riga['Media_Tesi_Sotto']}</span>"
        return nome_var + over + under

    if "Media_Tesi_Sovra" in dati.columns and "Media_Tesi_Sotto" in dati.columns:
        dati["tooltip"] = dati.apply(genera_tooltip, axis=1)
    else:
        dati["tooltip"] = dati["EtichettaVariabile"]

    # Colori
    colori = dati.apply(lambda riga: "red" if (riga["Log2FoldChange"] > fold_change_threshold and riga["-log10(p-value)"] > p_value_threshold)
                        else "blue" if (riga["Log2FoldChange"] < -fold_change_threshold and riga["-log10(p-value)"] > p_value_threshold)
                        else "grey", axis=1)

    dati["colore"] = colori

    # Plot
    fig = px.scatter(
        dati,
        x="Log2FoldChange",
        y="-log10(p-value)",
        color="colore",
        hover_data={"colore": False, "tooltip": True, "EtichettaVariabile": False},
        custom_data=["tooltip"],
        labels={"Log2FoldChange": "Log2 Fold Change", "-log10(p-value)": "-log10(p-value)"},
    )

    fig.update_traces(
        hovertemplate="%{customdata[0]}<extra></extra>",
        marker=dict(size=8),
    )

    fig.update_layout(
        showlegend=False,
        title="Volcano Plot personalizzato",
    )

    st.plotly_chart(fig, use_container_width=True)

    # Tabella sotto al grafico
    if fold_change_threshold != default_fold_change or p_value_threshold != default_p_value:
        st.subheader("🔎 Variabili che superano le soglie impostate")
        try:
            variabili_significative = dati[
                (dati['-log10(p-value)'] > p_value_threshold) &
                (abs(dati['Log2FoldChange']) > fold_change_threshold)
            ][['EtichettaVariabile', '-log10(p-value)', 'Log2FoldChange']]
            st.dataframe(variabili_significative)
        except KeyError as e:
            st.error(f"Errore: {e}")
