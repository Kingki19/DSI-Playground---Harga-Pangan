# Import library
import pandas as pd
import numpy as np
import streamlit as st
import requests

# === Preparing data for visualization 

# Function to get csv dataframe from url
def get_df_from_url(url):
    df = pd.read_csv(url, index_col=0)
    return df

# Read dataframe from csv file
bm_gabungan = get_df_from_url('https://raw.githubusercontent.com/Kingki19/DSI-Playground---Harga-Pangan/main/df_bm_gabungan.csv')
dar_gabungan = get_df_from_url('https://raw.githubusercontent.com/Kingki19/DSI-Playground---Harga-Pangan/main/df_dar_gabungan.csv')
bp_gabungan = get_df_from_url('https://raw.githubusercontent.com/Kingki19/DSI-Playground---Harga-Pangan/main/df_bp_gabungan.csv')

# === VISUALIZATION USING STREAMLIT ===


# Using "with" notation
with st.sidebar:
    st.header("Visualization data and prediction for 'DSI-Playground Harga Pangan' Competition")
    data_radio = st.radio(
        "Choose a data to visualize:",
        ("Bawang Merah", "Daging Ayam Ras", "Beras Premium")
    )

st.dataframe(data_radio)
