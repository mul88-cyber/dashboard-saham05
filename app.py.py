import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Dashboard Saham", layout="wide")

# Load data dari GCS
@st.cache_data
def load_data():
    url = "https://storage.googleapis.com/stock-csvku/hasil_gabungan.csv"
    try:
        df = pd.read_csv(url)
        df['Last Trading Date'] = pd.to_datetime(df['Last Trading Date'])
        df['Net Foreign'] = df['Foreign Buy'] - df['Foreign Sell']
        df['VWAP'] = df['Value'] / df['Volume']
        df['Sinyal'] = df.apply(lambda row: 'Akumulasi' if row['Close'] > row['VWAP'] and row['Net Foreign'] > 0
                                else 'Distribusi' if row['Close'] < row['VWAP'] and row['Net Foreign'] < 0
                                else 'Netral', axis=1)
        return df
    except Exception as e:
        st.error("❌ Gagal memuat data dari GCS. Pastikan file bisa diakses publik.")
        st.stop()

# Load once
df = load_data()

# Sidebar filters
st.sidebar.title("📊 Filter")
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [df['Last Trading Date'].min(), df['Last Trading Date'].max()])
selected_stock = st.sidebar.multiselect("Pilih Saham", options=sorted(df['Stock Code'].unique()), default=[])

# Filter data
if len(date_range) == 2:
    df = df[(df['Last Trading Date'] >= pd.to_datetime(date_range[0])) & 
            (df['Last Trading Date'] <= pd.to_datetime(date_range[1]))]

if selected_stock:
    df = df[df['Stock Code'].isin(selected_stock)]

st.title("📈 Dashboard Analisis Saham Harian (Bandarmologi)")

# Summary Table
st.subheader("🧠 Tabel Analisis Harian")
st.dataframe(
    df[['Last Trading Date', 'Stock Code', 'Company Name', 'Close', 'VWAP', 'Net Foreign', 'Sinyal']]
    .sort_values(['Last Trading Date', 'Net]()_
