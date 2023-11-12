# Import library
import pandas as pd
import numpy as np
import streamlit as st
import requests

# Funct to get data from url
def get_data(url):
    req = requests.get(url)
    if req.status_code == requests.codes.ok:
        req = req.json()  # the response is a JSON
        # req is now a dict with keys: name, encoding, url, size ...
        # and content. But it is encoded with base64.
        content = base64.decodestring(req['content'])
        return(content)
    else:
        print('Content was not found.')

# Read dataframe
data_harga = get_data("https://api.github.com/Kingki19/DSI-Playground---Harga-Pangan/raw/main/data_harga.xlsx")

# Tes
st.title("Visualization data and prediction for \'DSI-Playground Harga Pangan\' Competition")
st.dataframe(data_harga)
