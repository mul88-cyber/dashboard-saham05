import streamlit as st
import pandas as pd

def show_summary_tab(df):
    st.subheader("🧮 Summary Skoring Saham")

    df['Score'] = 0
    df['Score'] += df['Volume'] > df.groupby('Stock Code')['Volume'].transform(lambda x: x.rolling(5).mean())
    df['Score'] += df['Close'] > df.groupby('Stock Code')['Close'].transform(lambda x: x.rolling(5).mean())
    df['Score'] += df['Net Foreign'] > 0
    df['Score'] += df['Foreign Buy'] / (df['Foreign Sell'] + 1) > 1.5

    latest = df[df['Last Trading Date'] == df['Last Trading Date'].max()]
    top = latest.sort_values('Score', ascending=False).head(20)

    st.dataframe(
        top[['Last Trading Date', 'Stock Code', 'Company Name', 'Close', 'Volume', 'Net Foreign', 'Score']],
        use_container_width=True
    )