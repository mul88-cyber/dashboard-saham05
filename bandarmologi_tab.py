import streamlit as st
import pandas as pd

def show_bandarmologi_tab(df):
    st.subheader("🧠 Tabel Analisis Harian")
    date_range = st.sidebar.date_input("📅 Rentang Tanggal", [df['Last Trading Date'].min(), df['Last Trading Date'].max()])
    selected_stock = st.sidebar.multiselect("📌 Pilih Saham", options=sorted(df['Stock Code'].unique()), default=[])

    if len(date_range) == 2:
        df = df[(df['Last Trading Date'] >= pd.to_datetime(date_range[0])) & 
                (df['Last Trading Date'] <= pd.to_datetime(date_range[1]))]

    if selected_stock:
        df = df[df['Stock Code'].isin(selected_stock)]

    st.dataframe(
        df[['Last Trading Date', 'Stock Code', 'Company Name', 'Close', 'VWAP', 'Net Foreign', 'Sinyal']]
        .sort_values(['Last Trading Date', 'Net Foreign'], ascending=[False, False])
        .reset_index(drop=True),
        use_container_width=True
    )

    st.subheader("📈 Grafik Net Foreign")
    stocks_to_plot = selected_stock if selected_stock else df['Stock Code'].unique()[:1]
    for stock in stocks_to_plot:
        df_stock = df[df['Stock Code'] == stock]
        st.line_chart(
            df_stock.set_index('Last Trading Date')[['Net Foreign']],
            height=200,
            use_container_width=True,
        )

    st.subheader("📌 Volume Spike Detector")
    df['Avg Volume 5D'] = df.groupby('Stock Code')['Volume'].transform(lambda x: x.rolling(5).mean())
    df['Volume Spike'] = df['Volume'] > 2 * df['Avg Volume 5D']
    df_spike = df[df['Volume Spike'] == True]
    st.dataframe(
        df_spike[['Last Trading Date', 'Stock Code', 'Company Name', 'Volume', 'Avg Volume 5D']]
        .sort_values(['Last Trading Date', 'Volume'], ascending=[False, False]),
        use_container_width=True
    )

    st.subheader("📅 Akumulasi Mingguan")
    df['Minggu'] = df['Last Trading Date'] - pd.to_timedelta(df['Last Trading Date'].dt.dayofweek, unit='d')
    df_weekly = df.groupby(['Minggu', 'Stock Code']).agg({
        'Net Foreign': 'sum',
        'Volume': 'sum',
        'Value': 'sum'
    }).reset_index()
    df_weekly['Status'] = df_weekly['Net Foreign'].apply(lambda x: 'Akumulasi' if x > 0 else 'Distribusi' if x < 0 else 'Netral')

    st.dataframe(
        df_weekly.sort_values(['Minggu', 'Net Foreign'], ascending=[False, False]),
        use_container_width=True
    )

    st.download_button(
        label="📥 Download Data (CSV)",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name="analisa_saham.csv",
        mime='text/csv'
    )