import streamlit as st
import pandas as pd
import numpy as np
import glob
import os
import plotly.express as px

# Fungsi untuk imputasi outlier
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

# Fungsi untuk memuat dan membersihkan data
def load_and_clean_data(data_folder):
    csv_files = glob.glob(os.path.join(data_folder, 'PRSA_Data_*.csv'))
    station_data = {}
    for file in csv_files:
        base_name = os.path.basename(file)
        parts = base_name.split('_')
        if len(parts) > 3:
            station = parts[2].strip()
            df = pd.read_csv(file)
            # Gabungkan kolom tanggal menjadi satu kolom datetime
            df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
            df.drop(['year', 'month', 'day', 'hour'], axis=1, inplace=True)
            dt = df.pop('datetime')
            df.insert(1, 'datetime', dt)
            # Pastikan PM2.5 berupa numerik
            df['PM2.5'] = pd.to_numeric(df['PM2.5'], errors='coerce')
            df.sort_values('datetime', inplace=True)
            # Imputasi missing value dan outlier
            df['PM2.5_clean'] = df['PM2.5'].interpolate(method='linear')
            df['PM2.5_imputed'] = impute_outliers(df['PM2.5_clean'])
            station_data[station] = df
    return station_data

# Memuat data
data_folder = 'csv'
cleaned_dataframes = load_and_clean_data(data_folder)

# Sidebar: Pilihan stasiun dan fitur tambahan
st.sidebar.header("Pengaturan Dashboard")
station_options = list(cleaned_dataframes.keys())
selected_station = st.sidebar.selectbox("Pilih Stasiun", station_options)

st.sidebar.subheader("Tampilkan Grafik")
show_timeseries = st.sidebar.checkbox("Time Series PM2.5", value=True)
show_monthly = st.sidebar.checkbox("Rata-rata Bulanan PM2.5", value=True)
show_boxplot = st.sidebar.checkbox("Distribusi PM2.5 Antar Stasiun", value=True)
show_corr = st.sidebar.checkbox("Matriks Korelasi", value=True)
show_hist = st.sidebar.checkbox("Histogram PM2.5", value=True)

# Judul Dashboard
st.title("Dashboard Analisis Kualitas Udara - PM2.5")
st.write("Dashboard ini menyajikan analisis tren konsentrasi PM2.5 dan perbandingan kualitas udara antar stasiun.")

# Pastikan data stasiun tersedia
if selected_station in cleaned_dataframes:
    df_station = cleaned_dataframes[selected_station]
else:
    st.write(f"Data untuk stasiun {selected_station} tidak ditemukan.")
    st.stop()

# Grafik Time Series + Slider
if show_timeseries:
    st.subheader(f"Time Series PM2.5 - {selected_station}")

    # Tampilkan keterangan di bawah subheader
    st.markdown("Silakan pilih rentang waktu untuk memfilter data PM2.5 di bawah:")

    # Atur rentang tanggal minimum dan maksimum
    min_date = df_station['datetime'].min().date()
    max_date = df_station['datetime'].max().date()

    # Slider untuk menentukan rentang waktu
    selected_date_range = st.slider(
        "Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="MM/DD/YYYY"
    )
    start_date, end_date = selected_date_range

    # Filter data berdasarkan rentang waktu
    df_station_filtered = df_station[(df_station['datetime'] >= pd.to_datetime(start_date)) &
                                     (df_station['datetime'] <= pd.to_datetime(end_date))]

    # Plot time series dengan data yang sudah difilter
    fig_ts = px.line(
        df_station_filtered, 
        x="datetime", 
        y="PM2.5_imputed",
        title=f"Tren Konsentrasi PM2.5 - {selected_station} (Filtered)",
        labels={"PM2.5_imputed": "PM2.5 (Imputed)", "datetime": "Datetime"}
    )
    st.plotly_chart(fig_ts, use_container_width=True)

# Grafik Rata-rata Bulanan
if show_monthly:
    df_station['month'] = df_station['datetime'].dt.month
    monthly_avg = df_station.groupby('month')['PM2.5_imputed'].mean().reset_index()
    st.subheader(f"Rata-rata Bulanan PM2.5 - {selected_station}")
    fig2 = px.bar(monthly_avg, x="month", y="PM2.5_imputed",
                  title=f"Rata-rata PM2.5 Bulanan - {selected_station}",
                  labels={"month": "Bulan", "PM2.5_imputed": "Rata-rata PM2.5 (Imputed)"})
    st.plotly_chart(fig2, use_container_width=True)

# Boxplot Perbandingan Distribusi Antar Stasiun
if show_boxplot:
    st.subheader("Perbandingan Distribusi PM2.5 Antar Stasiun")
    all_data = []
    for station, df in cleaned_dataframes.items():
        temp = df[['datetime', 'PM2.5_imputed']].copy()
        temp['Station'] = station
        all_data.append(temp)
    all_data_df = pd.concat(all_data)
    fig3 = px.box(all_data_df, x="Station", y="PM2.5_imputed",
                  title="Distribusi PM2.5 Antar Stasiun",
                  labels={"PM2.5_imputed": "PM2.5 (Imputed)"})
    st.plotly_chart(fig3, use_container_width=True)

# Matriks Korelasi
if show_corr:
    st.subheader(f"Matriks Korelasi Parameter - {selected_station}")
    numeric_cols = ["PM2.5_imputed", "PM10", "SO2", "NO2", "CO", "O3", "TEMP", "PRES", "DEWP", "RAIN", "WSPM"]
    df_station_corr = cleaned_dataframes[selected_station]
    corr_matrix = df_station_corr[numeric_cols].corr()
    fig4 = px.imshow(corr_matrix, text_auto=True, color_continuous_scale='RdBu_r',
                     title=f"Matriks Korelasi - {selected_station}")
    fig4.update_layout(font=dict(size=16))
    st.plotly_chart(fig4, use_container_width=True)

# Histogram & Density Plot
if show_hist:
    st.subheader(f"Distribusi PM2.5 - {selected_station}")
    fig5 = px.histogram(df_station, x="PM2.5_imputed", nbins=30,
                        title=f"Histogram dan Density Plot PM2.5 - {selected_station}",
                        marginal="violin",
                        labels={"PM2.5_imputed": "PM2.5 (Imputed)"})
    st.plotly_chart(fig5, use_container_width=True)
