import streamlit as st
import pandas as pd
import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import seaborn as sns

def impute_outliers(s, lower_quantile=0.25, upper_quantile=0.75, k=1.5):
    Q1 = s.quantile(lower_quantile)
    Q3 = s.quantile(upper_quantile)
    IQR = Q3 - Q1
    lower_bound = Q1 - k * IQR
    upper_bound = Q3 + k * IQR
    median_val = s.median()
    s_imputed = s.copy()
    s_imputed[s < lower_bound] = median_val
    s_imputed[s > upper_bound] = median_val
    return s_imputed

def load_and_clean_data(data_folder):
    csv_files = glob.glob(os.path.join(data_folder, 'PRSA_Data_*.csv'))
    station_data = {}
    for file in csv_files:
        base_name = os.path.basename(file)
        parts = base_name.split('_')
        if len(parts) > 3:
            station = parts[2].strip()  
            df = pd.read_csv(file)
            df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
            df.drop(['year', 'month', 'day', 'hour'], axis=1, inplace=True)
            dt = df.pop('datetime')
            df.insert(1, 'datetime', dt)
            df['PM2.5'] = pd.to_numeric(df['PM2.5'], errors='coerce')
            df.sort_values('datetime', inplace=True)
            df['PM2.5_clean'] = df['PM2.5'].interpolate(method='linear')
            df['PM2.5_imputed'] = impute_outliers(df['PM2.5_clean'])
            station_data[station] = df
    return station_data

data_folder = 'csv'
cleaned_dataframes = load_and_clean_data(data_folder)

st.sidebar.header("Pilih Stasiun")
station_options = list(cleaned_dataframes.keys())
selected_station = st.sidebar.selectbox("Stasiun", station_options)

st.title("Dashboard Analisis Kualitas Udara - PM2.5")
st.write("Dashboard ini menyajikan analisis tren konsentrasi PM2.5 dan perbandingan kualitas udara antar stasiun.")

if selected_station in cleaned_dataframes:
    df_station = cleaned_dataframes[selected_station]
    st.subheader(f"Time Series PM2.5 - {selected_station}")
    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(df_station['datetime'], df_station['PM2.5_imputed'], label="PM2.5 (Imputed)", color="blue")
    ax.set_xlabel("Datetime")
    ax.set_ylabel("PM2.5")
    ax.set_title(f"Tren Konsentrasi PM2.5 - {selected_station}")
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.write(f"Data untuk stasiun {selected_station} tidak ditemukan.")

if selected_station in cleaned_dataframes:
    df_station['month'] = df_station['datetime'].dt.month
    monthly_avg = df_station.groupby('month')['PM2.5_imputed'].mean()
    st.subheader(f"Rata-rata Bulanan PM2.5 - {selected_station}")
    fig2, ax2 = plt.subplots(figsize=(10,6))
    monthly_avg.plot(kind='bar', color='skyblue', ax=ax2)
    ax2.set_xlabel("Bulan")
    ax2.set_ylabel("Rata-rata PM2.5 (Imputed)")
    ax2.set_title(f"Rata-rata PM2.5 Bulanan - {selected_station}")
    st.pyplot(fig2)

st.subheader("Perbandingan Distribusi PM2.5 Antar Stasiun")
all_data = []
for station, df in cleaned_dataframes.items():
    temp = df[['datetime', 'PM2.5_imputed']].copy()
    temp['Station'] = station
    all_data.append(temp)
all_data_df = pd.concat(all_data)
fig3, ax3 = plt.subplots(figsize=(12,6))
sns.boxplot(x="Station", y="PM2.5_imputed", data=all_data_df, ax=ax3)
ax3.set_xlabel("Stasiun")
ax3.set_ylabel("PM2.5 (Imputed)")
ax3.set_title("Distribusi PM2.5 Antar Stasiun")
plt.xticks(rotation=45)
st.pyplot(fig3)

st.subheader(f"Matriks Korelasi Parameter - {selected_station}")
numeric_cols = ["PM2.5_imputed", "PM10", "SO2", "NO2", "CO", "O3", "TEMP", "PRES", "DEWP", "RAIN", "WSPM"]
if selected_station in cleaned_dataframes:
    df_station_corr = cleaned_dataframes[selected_station]
    corr_matrix = df_station_corr[numeric_cols].corr()
    fig4, ax4 = plt.subplots(figsize=(10,8))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax4)
    ax4.set_title(f"Matriks Korelasi - {selected_station}")
    st.pyplot(fig4)

st.subheader(f"Distribusi PM2.5 - {selected_station}")
if selected_station in cleaned_dataframes:
    fig5, ax5 = plt.subplots(figsize=(10,6))
    sns.histplot(df_station['PM2.5_imputed'], bins=30, kde=True, color="green", ax=ax5)
    ax5.set_xlabel("PM2.5 (Imputed)")
    ax5.set_title(f"Histogram dan Density Plot PM2.5 - {selected_station}")
    st.pyplot(fig5)
