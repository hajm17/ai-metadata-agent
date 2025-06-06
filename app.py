import streamlit as st
import pandas as pd
from pandas.api.types import infer_dtype

st.set_page_config(page_title="AI Metadata Agent", layout="wide")
st.title("🤖 AI agent pro správu metadat")
st.markdown("Nahraj .csv soubor a AI zkontroluje chyby, navrhne typy a otaguje data.")

uploaded_file = st.file_uploader("Nahraj CSV soubor", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 Náhled dat")
    st.dataframe(df.head())

    st.subheader("🧪 Kontrola kvality dat")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Počet prázdných hodnot v každém sloupci:**")
        st.write(df.isnull().sum())

    with col2:
        st.markdown("**Detekovaný typ hodnot ve sloupcích:**")
        detected_types = df.apply(infer_dtype)
        st.write(detected_types)

    st.subheader("🏷️ Návrh metadat a tagů")
    metadata = []
    for col in df.columns:
        col_data = df[col]
        dtype = infer_dtype(col_data)
        tags = []

        if "date" in dtype:
            tags.append("datum")
        if "int" in dtype or "float" in dtype:
            tags.append("číselný")
        if "string" in dtype:
            if col_data.str.contains(r"@", na=False).any():
                tags.append("e-mail")
            elif col_data.str.contains(r"\+?[0-9]{9,}", na=False).any():
                tags.append("telefon")
            elif col.lower().find("id") != -1:
                tags.append("identifikátor")

        metadata.append({
            "sloupec": col,
            "typ": dtype,
            "prázdné_hodnoty": col_data.isnull().sum(),
            "tagy": tags
        })

    st.dataframe(pd.DataFrame(metadata))

    st.success("Analýza dokončena. Výsledky můžeš použít ve své práci nebo exportovat.")
