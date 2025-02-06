import streamlit as st

def mostra_tabella():
    st.title("Tabella dei Dati")

    # Controlla se i dati filtrati esistono in session_state
    if "dati_filtrati" not in st.session_state or st.session_state["dati_filtrati"] is None:
        st.error("⚠️ Nessun dato filtrato disponibile. Torna alla homepage e seleziona le classi.")
        return
    st.write("✅ Dati filtrati trovati in session_state.")

    dati = st.session_state["dati_filtrati"]
    classi = [st.session_state.get("class_1"), st.session_state.get("class_2")]

    # Controlla se le classi sono state selezionate
    if None in classi:
        st.error("⚠️ Le classi non sono state selezionate correttamente.")
        return
    st.write(f"📋 Visualizzazione tabella per classi: {classi}")

    # Mostra la tabella
    try:
        st.dataframe(dati)
        st.write("✅ Tabella visualizzata con successo!")
    except Exception as e:
        st.error(f"❌ Errore durante la visualizzazione della tabella: {e}")
