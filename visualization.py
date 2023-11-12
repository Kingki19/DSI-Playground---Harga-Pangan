# Import library
import pandas as pd
import numpy as np
import streamlit as st
import request

# Read dataframe
url = "https://github.com/Kingki19/DSI-Playground---Harga-Pangan/raw/main/data_harga.xlsx"
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Save the content to a local file
    with open("data_harga.xlsx", "wb") as f:
        f.write(response.content)

    # Now read the local file with pandas
    data_harga = pd.read_excel("data_harga.xlsx")
else:
    print(f"Failed to download the file. Status code: {response.status_code}")

# Tes
st.title("Visualization data and prediction for \'DSI-Playground Harga Pangan\' Competition")
st.dataframe(data_harga)
