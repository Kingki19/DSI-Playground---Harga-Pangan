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
    st.markdown("If you are interested, connect with me via:")
    st.markdown("**Linkedin**: [Muhammad Rizqi](www.linkedin.com/in/muhammad-rizqi-921538248)")

    
# Create a 'Dashboard' object
class Dashboard:
    def __init__(self, df, col_name):
        self.df = df
        self.col_name = col_name
        self.col_data = df[col_name]
        
province_selectbox = st.selectbox(
    "Choose a province to visualize:",
    ('Aceh', 'Sumatera Utara', 'Sumatera Barat', 'Riau', 'Jambi', 'Sumatera Selatan', 'Bengkulu', 'Lampung',
            'Bangka Belitung', 'Kepulauan Riau', 'DKI Jakarta', 'Jawa Barat', 'Jawa Tengah', 'D.I. Yogyakarta',
            'Jawa Timur', 'Banten', 'Bali', 'Nusa Tenggara Barat', 'Nusa Tenggara Timur', 'Kalimantan Barat',
            'Kalimantan Tengah', 'Kalimantan Selatan', 'Kalimantan Timur', 'Kalimantan Utara', 'Sulawesi Utara',
            'Sulawesi Tengah', 'Sulawesi Selatan', 'Sulawesi Tenggara', 'Gorontalo', 'Sulawesi Barat', 'Maluku',
            'Maluku Utara', 'Papua Barat', 'Papua')
)
column_name = province_selectbox
st.header(column_name)
st.divider()

if data_radio == "Bawang merah / Shallots":
    bm_dashboard = Dashboard(bm_gabungan, column_name)
    st.line_chart(bm_dashboard.col_data)
    
elif data_radio == "Daging ayam ras / Purebred chicken meat":
    dar_dashboard = Dashboard(dar_gabungan, column_name)
    st.line_chart(dar_dashboard.col_data)
    
elif data_radio == "Beras premium / Premium rice":
    if column_name == 'Gorontalo':
        st.error("There's no Gorontalo in this dataframe")
    else:
        bp_dashboard = Dashboard(bp_gabungan, column_name)
        st.line_chart(bp_dashboard.col_data)

