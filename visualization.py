# Import library
import pandas as pd
import numpy as np
import streamlit as st
import requests

# Funct to get data from url
def get_df_from_url(url):
        df = pd.read_csv(url)
        return(df)

# Read dataframe
data_harga = get_df_from_url('https://raw.githubusercontent.com/Kingki19/DSI-Playground---Harga-Pangan/main/data_harga.csv')

# Tes
st.title("Visualization data and prediction for \'DSI-Playground Harga Pangan\' Competition")
st.dataframe(data_harga)
