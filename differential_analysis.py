st.sidebar.title("📂 Caricamento Dati")
file = st.sidebar.file_uploader("Carica il file Excel", type=['xlsx'])

# Inizializzazione dei dati filtrati
# Variabili di stato
dati_filtrati = None
class_1 = None
class_2 = None
@@ -22,25 +22,39 @@
    if dati is not None and len(classi) > 1:
        # Sidebar - Selezione delle classi
        st.sidebar.subheader("🔍 Seleziona le classi da confrontare:")
        class_1 = st.sidebar.selectbox("Classe 1", classi)
        class_2 = st.sidebar.selectbox("Classe 2", classi)
        if class_1 and class_2 and class_1 != class_2:
            # Filtrare i dati solo per le classi selezionate
            dati_filtrati = dati.loc[:, dati.columns.get_level_values(1).isin([class_1, class_2])]
            # Sidebar - Navigazione dopo la selezione delle classi
            st.sidebar.title("📊 Navigazione")
            sezione = st.sidebar.radio("Scegli una sezione:", ["Volcano Plot", "Tabella Dati"])
            # Mostra la sezione selezionata con i dati filtrati
            if sezione == "Volcano Plot":
                mostra_volcano_plot(dati_filtrati, [class_1, class_2])
            elif sezione == "Tabella Dati":
                mostra_tabella(dati_filtrati, [class_1, class_2])
        else:
            st.sidebar.warning("⚠️ Seleziona due classi diverse per procedere.")
        class_1 = st.sidebar.selectbox("Classe 1", classi, key="classe1")
        class_2 = st.sidebar.selectbox("Classe 2", classi, key="classe2")
        # Tasto di conferma selezione
        if st.sidebar.button("✅ Conferma selezione"):
            if class_1 and class_2 and class_1 != class_2:
                # Filtrare i dati solo per le classi selezionate
                dati_filtrati = dati.loc[:, dati.columns.get_level_values(1).isin([class_1, class_2])]
                # Memorizzare i dati filtrati in session_state
                st.session_state["dati_filtrati"] = dati_filtrati
                st.session_state["class_1"] = class_1
                st.session_state["class_2"] = class_2
                st.sidebar.success("✅ Selezione confermata! Scegli un'analisi.")
    else:
        st.sidebar.warning("⚠️ Il file caricato non contiene abbastanza classi per l'analisi.")
# Dopo la conferma della selezione, abilitare la navigazione
if "dati_filtrati" in st.session_state:
    st.sidebar.title("📊 Navigazione")
    sezione = st.sidebar.radio("Scegli una sezione:", ["Volcano Plot", "Tabella Dati"])
    # Recuperare i dati filtrati dalla sessione
    dati_filtrati = st.session_state["dati_filtrati"]
    class_1 = st.session_state["class_1"]
    class_2 = st.session_state["class_2"]
    # Mostra la sezione selezionata con i dati filtrati
    if sezione == "Volcano Plot":
        mostra_volcano_plot(dati_filtrati, [class_1, class_2])
    elif sezione == "Tabella Dati":
        mostra_tabella(dati_filtrati, [class_1, class_2])
else:
    st.sidebar.warning("⚠️ Carica un file Excel per iniziare.")
    st.sidebar.info("🔹 Carica un file e seleziona due classi per procedere.")
