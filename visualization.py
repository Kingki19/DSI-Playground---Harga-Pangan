# Import library
import pandas as pd
import numpy as np
import streamlit as st
import requests
from datetime import datetime

# === Preparing data for visualization ===
# Function to get csv dataframe from url
def get_df_from_url(url):
    df = pd.read_csv(url, index_col=0)
    return df

# Read dataframe from csv file
bm_gabungan = get_df_from_url('https://raw.githubusercontent.com/Kingki19/DSI-Playground---Harga-Pangan/main/df_bm_gabungan.csv')
dar_gabungan = get_df_from_url('https://raw.githubusercontent.com/Kingki19/DSI-Playground---Harga-Pangan/main/df_dar_gabungan.csv')
bp_gabungan = get_df_from_url('https://raw.githubusercontent.com/Kingki19/DSI-Playground---Harga-Pangan/main/df_bp_gabungan.csv')

# Create combined dataframe in 1 dictionary
df_combined = {
    'bawang_merah': bm_gabungan,
    'daging_ayam_ras': dar_gabungan,
    'beras_premium': bp_gabungan
}

# Create province list for options to visualize later
provinces = [
    'Aceh', 'Sumatera Utara', 'Sumatera Barat', 'Riau', 'Jambi', 'Sumatera Selatan', 'Bengkulu', 'Lampung',
    'Bangka Belitung', 'Kepulauan Riau', 'DKI Jakarta', 'Jawa Barat', 'Jawa Tengah', 'D.I. Yogyakarta',
    'Jawa Timur', 'Banten', 'Bali', 'Nusa Tenggara Barat', 'Nusa Tenggara Timur', 'Kalimantan Barat',
    'Kalimantan Tengah', 'Kalimantan Selatan', 'Kalimantan Timur', 'Kalimantan Utara', 'Sulawesi Utara',
    'Sulawesi Tengah', 'Sulawesi Selatan', 'Sulawesi Tenggara', 'Gorontalo', 'Sulawesi Barat', 'Maluku',
    'Maluku Utara', 'Papua Barat', 'Papua'
]

# === Create functions or objects to visualize ===
# Function to find location (index, column) in dataframe based target value
def find_position_in_df(df, target_value):
    result = df.where(df == target_value).stack()
    locations = list(zip(result.index.get_level_values(0), result.index.get_level_values(1)))
    return locations
    
# Create a 'Container' that contain one or multiple element
# 'container' is local variable in 'Container' object to make sure all element in one 'container'
class Container:
    def __init__(self, df_combined, provinces):
        self.df_combined = df_combined # it's dictionary 
        self.provinces = provinces # list
        self.selected_df = None # Choose between value in 'df_combined'
        self.df = None # self.df = self.df_combined[selected_df]
        self.selected_province = None # province that want to display 
        self.province_data = {} # province_data = {'province_name1': province_data1, ...}
        self.container = st.container()
        
    # Add options for user to choose one or multiple provinces and which data to visualize
    def options(self):
        with self.container:
            # Options for categorical data
            data_option = st.selectbox(
                "Select the data you want to visualize:",
                ('bawang_merah', 'daging_ayam_ras', 'beras_premium')
            )
            # Multi-Options for provinces 
            provinces_option = st.multiselect(
                "Select which provinces you want to display:",
                self.provinces,
                ['Aceh']
            )
        if (data_option == 'beras_premium') and ('Gorontalo' in provinces_option):
            st.warning('There\'s no \'Gorontalo\' Column in \'beras_premium\' data')
            st.stop()
        else:
            self.selected_df = data_option # return string type
            self.df = self.df_combined[self.selected_df]
            index_list = self.df.index.to_list()
        # Slider options for datetime range
            with self.container:
                date_range = st.select_slider(
                    "Choose date range to visualize:",
                    options = index_list,
                    value = (index_list[0], index_list[-1])
                )
            start_range = date_range[0]
            end_range = date_range[1]
            self.df = self.df.loc[start_range:end_range]
            self.selected_province = provinces_option # return list type
            self.province_data = pd.DataFrame({province : self.df[province] for province in self.selected_province})
            
            
    # Create metrics that include
    def add_metrics(self):
        if len(self.selected_province) == 0:
            st.info("You didn't choose a single province!")
        elif len(self.selected_province) > 0:
            min = round(self.province_data.stack().min())
            min_index, min_column = find_position_in_df(self.province_data, min)[0]
            mean = round(self.province_data.stack().mean())
            max = round(self.province_data.stack().max())
            max_index, max_column = find_position_in_df(self.province_data, max)[0]
            with self.container:
                min_col, mean_col, max_col = st.columns(3)
                min_col.metric(
                    label = "Minimum price", 
                    value = f"Rp {min:,}",
                    delta = f"{min_column} : {min_index}",
                    delta_color = 'off',
                    help = f"The lowest value in seleced data / provinces"
                )
                mean_col.metric(
                    label = "Mean price", 
                    value = f"Rp {mean:,}",
                    help = f"Mean value of seleced data / provinces"
                )
                max_col.metric(
                    label = "Maximum price", 
                    value = f"Rp {max:,}",
                    delta = f"{max_column} : {max_index}"
                    delta_color = "off",
                    help = f"The highest value in seleced data / provinces"
                )
        else:
            st.error("It can't be possible!")
        
    # Create line chart into container
    def add_line_chart(self):
        with self.container:
            st.line_chart(self.province_data)

# === VISUALIZATION USING STREAMLIT ===
# PAGE CONFIGURATION
st.set_page_config(
    page_title="DSI Playground - Harga Pangan",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="auto",
)

# SIDEBAR
with st.sidebar:
    st.title("Visualization data and prediction for \'DSI Playground-Harga Pangan\' Competition")
    st.divider()
    st.markdown("**Better to use Computer or Laptop when using this app!**")
    st.divider()
    st.markdown("If you are interested, connect with me via:")
    st.markdown("[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](www.linkedin.com/in/muhammad-rizqi-921538248)")
    st.markdown("[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Kingki19)")
    st.markdown("[![Kaggle](https://img.shields.io/badge/Kaggle-035a7d?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/kingki19)")


# DASHBOARD
# Container 1
container1 = Container(df_combined, provinces)
container1.options()
container1.add_metrics()
container1.add_line_chart()

