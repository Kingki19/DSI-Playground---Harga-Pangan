# Import library
import pandas as pd
import numpy as np
import streamlit as st
import requests

# Funct to get data from url
def get_df_from_url(url):
        myfile = requests.get(url)
        df=pd.read_excel(myfile.content)
        return(df)

# Read dataframe
data_harga = pd.read_excel('data_harga.xlsx')

# Tes
st.title("Visualization data and prediction for \'DSI-Playground Harga Pangan\' Competition")
st.dataframe(data_harga)
