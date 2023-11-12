# Import library
import pandas as pd
import numpy as np
import streamlit as st
import requests

# === Preparing data for visualization ===
# Function to get csv dataframe from url
def get_df_from_url(url):
    df = pd.read_csv(url, index_col=0)
    return df

# Read dataframe from csv file
data_harga_df = get_df_from_url('https://raw.githubusercontent.com/Kingki19/DSI-Playground---Harga-Pangan/main/data_harga.csv')
bm_summary_df = get_df_from_url('https://raw.githubusercontent.com/Kingki19/DSI-Playground---Harga-Pangan/main/bm_summary_pred.csv')
dar_summary_df = get_df_from_url('https://raw.githubusercontent.com/Kingki19/DSI-Playground---Harga-Pangan/main/dar_summary_pred.csv')
bp_summary_df = get_df_from_url('https://raw.githubusercontent.com/Kingki19/DSI-Playground---Harga-Pangan/main/bp_summary_pred.csv')

# Split data_harga_df into categorical
df_bm = data_harga_df[data_harga_df['Komoditas'] == 'Bawang merah']
df_dar = data_harga_df[data_harga_df['Komoditas'] == 'Daging Ayam Ras']
df_bp = data_harga_df[data_harga_df['Komoditas'] == 'Beras Premium']

# Function to datetime index from string into datetime (numerical like '20-09-2019')
def bulan_to_angka(bulan):
    bulan_dict = {
        'Januari': '01',
        'Februari': '02',
        'Maret': '03',
        'April': '04',
        'Mei': '05',
        'Juni': '06',
        'Juli': '07',
        'Agustus': '08',
        'September': '09',
        'Oktober': '10',
        'November': '11',
        'Desember': '12'
    }
    return bulan_dict.get(bulan, bulan)

# Function to change categorical df to useful df
def set_data_to_right_df(df):
    date = df.columns[df.columns.get_loc('Januari 2018'):].tolist()
    tanggal_list = []
    for item in date:
        if isinstance(item, str):  # Check if the element is a string month
            bulan, tahun = item.split(' ')
            angka_bulan = bulan_to_angka(bulan)
            tanggal_list.append(f"{angka_bulan}/{tahun}")
        elif isinstance(item, datetime):  # If the element is a datetime object, convert it to date format
            tanggal_list.append(item.strftime('%m/%Y'))
        else:
            tanggal_list.append(item)  # Leave other elements unchanged

    dict_copy = {
        'date': tanggal_list, 
        'Aceh': [],
        'Sumatera Utara': [], 
        'Sumatera Barat': [],
        'Riau': [], 
        'Jambi': [],
        'Sumatera Selatan': [], 
        'Bengkulu': [],
        'Lampung': [], 
        'Bangka Belitung': [],
        'Kepulauan Riau': [], 
        'DKI Jakarta': [],
        'Jawa Barat': [], 
        'Jawa Tengah': [],
        'D.I. Yogyakarta': [], 
        'Jawa Timur': [],
        'Banten': [], 
        'Bali': [], 
        'Nusa Tenggara Barat': [],
        'Nusa Tenggara Timur': [], 
        'Kalimantan Barat': [],
        'Kalimantan Tengah': [], 
        'Kalimantan Selatan': [],
        'Kalimantan Timur': [], 
        'Kalimantan Utara': [],
        'Sulawesi Utara': [], 
        'Sulawesi Tengah': [],
        'Sulawesi Selatan': [], 
        'Sulawesi Tenggara': [],
        'Gorontalo': [], 
        'Sulawesi Barat': [],
        'Maluku': [], 
        'Maluku Utara': [],
        'Papua Barat': [], 
        'Papua': []
    }

    for provinsi in dict_copy.keys():
        if provinsi == 'date':
            continue  # Skip to the next province if this is 'date'

        # Get data for the current province
        provinsi_data = df[df['Lokasi'] == provinsi].iloc[:, 2:].values.tolist()

        # Add data to the dictionary according to the province
        for row in provinsi_data:
            dict_copy[provinsi].extend(row)

    # Convert the date to datetime format
    dict_copy['date'] = pd.to_datetime(dict_copy['date'], format="%m/%Y")

    # If there are empty columns in 'dict_copy', they will be removed
    dict_copy = {key: value for key, value in dict_copy.items() if key == 'date' or any(value)}
    df_copy = pd.DataFrame(dict_copy)
    df_copy = df_copy.set_index('date')
    # df_copy = df_copy.resample('M').sum()
    return df_copy

# Apply the above function to categorical data
tsdf_bm = set_data_to_right_df(df_bm)
tsdf_dar = set_data_to_right_df(df_dar)
tsdf_bp = set_data_to_right_df(df_bp)

# Clean categorical data using interpolate()
tsdf_bm = tsdf_bm.interpolate()
tsdf_dar = tsdf_dar.interpolate()
tsdf_bp = tsdf_bp.interpolate()
tsdf_bp = tsdf_bp.dropna()  # There are empty values in the first 3 months

# Function to mix dataframe 'data_harga' and another 3 summaries
def gabung_data(df, used_df):
    # Adding a new row
    provinsi = ['Aceh', 'Sumatera Utara', 'Sumatera Barat', 'Riau', 'Jambi', 'Sumatera Selatan', 'Bengkulu', 'Lampung',
                'Bangka Belitung', 'Kepulauan Riau', 'DKI Jakarta', 'Jawa Barat', 'Jawa Tengah', 'D.I. Yogyakarta',
                'Jawa Timur', 'Banten', 'Bali', 'Nusa Tenggara Barat', 'Nusa Tenggara Timur', 'Kalimantan Barat',
                'Kalimantan Tengah', 'Kalimantan Selatan', 'Kalimantan Timur', 'Kalimantan Utara', 'Sulawesi Utara',
                'Sulawesi Tengah', 'Sulawesi Selatan', 'Sulawesi Tenggara', 'Gorontalo', 'Sulawesi Barat', 'Maluku',
                'Maluku Utara', 'Papua Barat', 'Papua']

    prediksi = ['Juli', 'Agustus', 'September']

    for bulan in prediksi:
        new_row = pd.DataFrame()
        for prov in provinsi:
            row = pd.DataFrame({
                prov: [used_df.loc[used_df['Lokasi'] == prov, bulan].values[0]]
            })
            new_row = pd.concat([new_row, row], axis=1)
        df = pd.concat([df, new_row], axis=0)

    new_indices = ['2023-07-01 00:00:00', '2023-08-01 00:00:00', '2023-09-01 00:00:00']
    df.index = df.index[:-3].tolist() + new_indices
    df.index = pd.to_datetime(df.index)
    return df

# Apply it to only 2 dataframes
# Because there's Gorontalo in Provinsi meanwhile df_bp_gabungan didn't
df_bm_gabungan = gabung_data(tsdf_bm, bm_prediction)
df_dar_gabungan = gabung_data(tsdf_dar, dar_prediction)

# Only for tsdf_bp
df = tsdf_bp
used_df = bp_prediction

# Adding a new row
provinsi = ['Aceh', 'Sumatera Utara', 'Sumatera Barat', 'Riau', 'Jambi', 'Sumatera Selatan', 'Bengkulu', 'Lampung',
            'Bangka Belitung', 'Kepulauan Riau', 'DKI Jakarta', 'Jawa Barat', 'Jawa Tengah', 'D.I. Yogyakarta',
            'Jawa Timur', 'Banten', 'Bali', 'Nusa Tenggara Barat', 'Nusa Tenggara Timur', 'Kalimantan Barat',
            'Kalimantan Tengah', 'Kalimantan Selatan', 'Kalimantan Timur', 'Kalimantan Utara', 'Sulawesi Utara',
            'Sulawesi Tengah', 'Sulawesi Selatan', 'Sulawesi Tenggara', 'Sulawesi Barat', 'Maluku',
            'Maluku Utara', 'Papua Barat', 'Papua']  # No Gorontalo

prediksi = ['Juli', 'Agustus', 'September']
for bulan in prediksi:
    new_row = pd.DataFrame()
    for prov in provinsi:
        row = pd.DataFrame({
            prov: [used_df.loc[used_df['Lokasi'] == prov, bulan].values[0]]
        })
        new_row = pd.concat([new_row, row], axis=1)
    df = pd.concat([df, new_row], axis=0)

new_indices = ['2023-07-01 00:00:00', '2023-08-01 00:00:00', '2023-09-01 00:00:00']
df.index = df.index[:-3].tolist() + new_indices
df.index = pd.to_datetime(df.index)
df_bp_gabungan = df

# Reset index and change it into datetime
df_bm_gabungan.reset_index(level=0, inplace=True)
df_bm_gabungan.rename(columns={'index': 'date'}, inplace=True)
df_dar_gabungan.reset_index(level=0, inplace=True)
df_dar_gabungan.rename(columns={'index': 'date'}, inplace=True)
df_bp_gabungan.reset_index(level=0, inplace=True)
df_bp_gabungan.rename(columns={'index': 'date'}, inplace=True)

# === VISUALIZATION USING STREAMLIT ===
st.header("Visualization data and prediction for 'DSI-Playground Harga Pangan' Competition")

# Using "with" notation
with st.sidebar:
    st.title("Option:")
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )

st.dataframe(df_bm_gabungan)
st.dataframe(df_dar_gabungan)
st.dataframe(df_bp_gabungan)
