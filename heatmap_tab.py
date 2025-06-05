import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

def show_heatmap_tab(df):
    st.subheader("🔥 Heatmap Volume vs Net Foreign")
    pivot = df.pivot_table(index='Stock Code', columns='Last Trading Date', values='Net Foreign', aggfunc='sum').fillna(0)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(pivot, cmap='RdYlGn', center=0, ax=ax)
    st.pyplot(fig)