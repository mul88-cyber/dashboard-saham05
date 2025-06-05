import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    url = "https://storage.googleapis.com/stock-csvku/hasil_gabungan.csv"
    df = pd.read_csv(url)
    df['Last Trading Date'] = pd.to_datetime(df['Last Trading Date'])
    df['Net Foreign'] = df['Foreign Buy'] - df['Foreign Sell']
    df['VWAP'] = df['Value'] / df['Volume']
    df['Sinyal'] = df.apply(lambda row: 'Akumulasi' if row['Close'] > row['VWAP'] and row['Net Foreign'] > 0
                            else 'Distribusi' if row['Close'] < row['VWAP'] and row['Net Foreign'] < 0
                            else 'Netral', axis=1)
    return df

df = load_data()

st.set_page_config(page_title="📈 Dashboard Saham", layout="wide")
st.title("📊 Dashboard Analisis Saham Harian")

tab1, tab2, tab3 = st.tabs(["🏦 Bandarmologi", "🔥 Heatmap", "🧮 Summary Skoring"])

with tab1:
    from bandarmologi_tab import show_bandarmologi_tab
    show_bandarmologi_tab(df)

with tab2:
    from heatmap_tab import show_heatmap_tab
    show_heatmap_tab(df)

with tab3:
    from summary_tab import show_summary_tab
    show_summary_tab(df)

st.caption("🚀 Dibuat otomatis oleh AI untuk analisa saham harian tanpa broker summary.")