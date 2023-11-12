# Import library
import pandas as pd
import numpy as np
import streamlit as st

# Read dataframe
data_harga = pd.read_excel("https://github.com/Kingki19/DSI-Playground---Harga-Pangan/blob/main/data_harga.xlsx")

# Tes
st.title("Visualization data and prediction for \'DSI-Playground Harga Pangan\' Competition")
st.dataframe(data_harga)
