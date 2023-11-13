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
bm_gabungan = get_df_from_url(https://raw.githubusercontent.com/Kingki19/DSI-Playground---Harga-Pangan/main/df_bm_gabungan.csv)
dar_gabungan = get_df_from_url(https://raw.githubusercontent.com/Kingki19/DSI-Playground---Harga-Pangan/main/df_dar_gabungan.csv)
bp_gabungan = get_df_from_url(https://raw.githubusercontent.com/Kingki19/DSI-Playground---Harga-Pangan/main/df_bp_gabungan.csv)

# === VISUALIZATION USING STREAMLIT ===
st.header("Visualization data and prediction for 'DSI-Playground Harga Pangan' Competition")

# Using "with" notation
with st.sidebar:
    st.title("Option:")
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )

st.dataframe(bm_gabungan)
st.dataframe(dar_gabungan)
st.dataframe(bp_gabungan)
