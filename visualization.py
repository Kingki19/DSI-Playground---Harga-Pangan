# Import library
import pandas as pd
import numpy as np
import streamlit as st
import requests

# Funct to get data from url
def get_df_from_url(url):
        df = pd.read_csv(url, index_col=0)
        return(df)

# Read dataframe from csv file
data_harga_df = get_df_from_url('https://raw.githubusercontent.com/Kingki19/DSI-Playground---Harga-Pangan/main/data_harga.csv')
bm_summary_df = get_df_from_url('https://raw.githubusercontent.com/Kingki19/DSI-Playground---Harga-Pangan/main/bm_summary_pred.csv')
dar_summary_df = get_df_from_url('https://raw.githubusercontent.com/Kingki19/DSI-Playground---Harga-Pangan/main/dar_summary_pred.csv')
bp_summary_df = get_df_from_url('https://raw.githubusercontent.com/Kingki19/DSI-Playground---Harga-Pangan/main/bp_summary_pred.csv')

# Tes
st.title("Visualization data and prediction for \'DSI-Playground Harga Pangan\' Competition")

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )
