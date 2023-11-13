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
# Config for page
st.set_page_config(
    page_title="DSI Playground - Harga Pangan",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="auto",
)

# Using "with" notation
with st.sidebar:
    st.title("Visualization data and prediction for \'DSI Playground-Harga Pangan\' Competition")
    st.divider()
    data_radio = st.radio(
        "Choose a data to visualize:",
        ("Bawang merah / Shallots", "Daging ayam ras / Purebred chicken meat", "Beras premium / Premium rice")
    )
    st.divider()
    province_selectbox = st.selectbox(
        "Choose a province to visualize:",
        ('Aceh', 'Sumatera Utara', 'Sumatera Barat', 'Riau', 'Jambi', 'Sumatera Selatan', 'Bengkulu', 'Lampung',
                'Bangka Belitung', 'Kepulauan Riau', 'DKI Jakarta', 'Jawa Barat', 'Jawa Tengah', 'D.I. Yogyakarta',
                'Jawa Timur', 'Banten', 'Bali', 'Nusa Tenggara Barat', 'Nusa Tenggara Timur', 'Kalimantan Barat',
                'Kalimantan Tengah', 'Kalimantan Selatan', 'Kalimantan Timur', 'Kalimantan Utara', 'Sulawesi Utara',
                'Sulawesi Tengah', 'Sulawesi Selatan', 'Sulawesi Tenggara', 'Gorontalo', 'Sulawesi Barat', 'Maluku',
                'Maluku Utara', 'Papua Barat', 'Papua')
    )

# class dashboard:
#     def __init__(self):
        
column = province_selectbox
st.header(column)
st.divider()
if data_radio == "Bawang merah / Shallots": 
    st.dataframe(bm_gabungan)
elif data_radio == "Daging ayam ras / Purebred chicken meat":
    st.dataframe(dar_gabungan)
elif data_radio == "Beras premium / Premium rice":
    if column == 'Gorontalo':
        st.error("There's no Gorontalo in this dataframe")
    else:
        st.dataframe(bp_gabungan)

