import streamlit as st
import pandas as pd
import numpy as np
import glob
import os
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

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

# Kelompokkan stasiun ke dalam kategori wilayah
station_categories = {
    "Aotizhongxin": "Perkotaan",
    "Dongsi": "Perkotaan",
    "Guanyuan": "Perkotaan",
    "Wanshouxigong": "Perkotaan",
    "Gucheng": "Industri",
    "Changping": "Pinggiran/Suburban",
    "Huairou": "Pinggiran/Suburban",
    "Shunyi": "Pinggiran/Suburban",
    "Dingling": "Sejarah & Budaya",
    "Tiantan": "Sejarah & Budaya",
    "Wanliu": "Pendidikan & Penelitian",
    "Nongzhanguan": "Pendidikan & Penelitian"
}

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
            
            # Tambahkan kolom tanggal, bulan, dan tahun untuk agregasi
            df['date'] = df['datetime'].dt.date
            df['month'] = df['datetime'].dt.month
            df['year'] = df['datetime'].dt.year
            
            # Tambahkan kategori wilayah
            df['Kategori'] = station_categories.get(station, "Tidak Dikategorikan")
            
            # Pastikan semua kolom numerik
            columns_to_clean = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3", "TEMP", "PRES", "DEWP", "RAIN", "WSPM"]
            for col in columns_to_clean:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Imputasi missing value dan outlier
            df.sort_values('datetime', inplace=True)
            
            for col in columns_to_clean:
                df[f"{col}_clean"] = df[col].interpolate(method='linear')
                df[f"{col}_clean"] = df[f"{col}_clean"].ffill().bfill()
                df[f"{col}_clean"] = df[f"{col}_clean"].fillna(df[f"{col}_clean"].mean())
                df[f"{col}_imputed"] = impute_outliers(df[f"{col}_clean"])
            
            station_data[station] = df
    
    return station_data

# Fungsi untuk mendapatkan agregasi bulanan
def get_monthly_stats(df):
    monthly_stats = df.groupby(['year', 'month']).agg({
        'PM2.5_imputed': ['mean', 'min', 'max', 'std']
    }).reset_index()
    monthly_stats.columns = ['year', 'month', 'mean', 'min', 'max', 'std']
    monthly_stats['Year-Month'] = pd.to_datetime(monthly_stats['year'].astype(str) + '-' + monthly_stats['month'].astype(str))
    return monthly_stats

# Fungsi untuk membuat plot matplotlib untuk streamlit
def fig_to_plt():
    return plt.gcf()

# Judul Dashboard
st.title("Dashboard Analisis Kualitas Udara - PM2.5")
st.write("Dashboard ini menyajikan analisis tren konsentrasi PM2.5 dan perbandingan kualitas udara antar stasiun.")
# st.subheader("Informasi Kategori Stasiun")
# # Konversi dictionary ke DataFrame untuk ditampilkan sebagai tabel
# station_categories_df = pd.DataFrame({
#     'Stasiun': list(station_categories.keys()),
#     'Kategori': list(station_categories.values())
# })
# st.dataframe(station_categories_df)
with st.sidebar.expander("Informasi Kategori Stasiun"):
    for station, category in station_categories.items():
        st.write(f"**{station}**: {category}")

# Sidebar: Pilihan stasiun dan fitur tambahan
st.sidebar.header("Pengaturan Dashboard")

# Memuat data
data_folder = 'csv'
try:
    cleaned_dataframes = load_and_clean_data(data_folder)
    
    # Gabungkan semua data untuk analisis berdasarkan kategori
    all_data = []
    for station, df in cleaned_dataframes.items():
        all_data.append(df)
    
    all_data_df = pd.concat(all_data)
    
    # Modifikasi: Menggunakan multiselect untuk pemilihan stasiun
    station_options = list(cleaned_dataframes.keys())
    selected_stations = st.sidebar.multiselect(
        "Pilih Stasiun",
        options=["All Stations"] + station_options,
        default=["All Stations"]
    )
    
    # Jika tidak ada stasiun dipilih atau All Stations dipilih, gunakan semua stasiun
    if not selected_stations or "All Stations" in selected_stations:
        selected_stations = station_options
    
    # Filter data kategori
    kategori_options = list(set(station_categories.values()))
    selected_kategori = st.sidebar.multiselect(
        "Pilih Kategori Wilayah",
        options=["All Categories"] + kategori_options,
        default=["All Categories"]
    )
    
    # Jika tidak ada kategori dipilih atau All Categories dipilih, gunakan semua kategori
    if not selected_kategori or "All Categories" in selected_kategori:
        selected_kategori = kategori_options
    
    st.sidebar.subheader("Tampilkan Grafik")
    show_timeseries = st.sidebar.checkbox("Time Series PM2.5", value=True)
    show_monthly_kategori = st.sidebar.checkbox("Tren Bulanan Berdasarkan Kategori", value=True)
    show_monthly_pattern = st.sidebar.checkbox("Pola Bulanan PM2.5", value=True)
    show_boxplot = st.sidebar.checkbox("Distribusi PM2.5 Antar Stasiun", value=True)
    show_corr = st.sidebar.checkbox("Matriks Korelasi", value=True)
    show_kategori_comparison = st.sidebar.checkbox("Perbandingan Kategori Wilayah", value=True)
    show_factors = st.sidebar.checkbox("Faktor yang Mempengaruhi PM2.5", value=True)
    
    # Tab untuk menampilkan hasil analisis
    tab1, tab2 = st.tabs(["Visualisasi", "Kesimpulan"])
    
    with tab1:
        # Grafik Time Series Agregat Bulanan
        if show_timeseries and selected_stations:
            st.subheader("Time Series PM2.5 (Agregat Bulanan)")
            
            # Agregasi data bulanan untuk semua stasiun yang dipilih
            all_monthly_data = []
            for station in selected_stations:
                monthly_stats = get_monthly_stats(cleaned_dataframes[station])
                monthly_stats['Station'] = station
                all_monthly_data.append(monthly_stats)
            
            if all_monthly_data:
                monthly_df = pd.concat(all_monthly_data)
                
                fig_ts = px.line(
                    monthly_df,
                    x="Year-Month",
                    y="mean",
                    color="Station",
                    title="Tren Bulanan Rata-rata PM2.5 per Stasiun",
                    labels={"mean": "Rata-rata PM2.5 (Imputed)", "Year-Month": "Bulan-Tahun"}
                )
                st.plotly_chart(fig_ts, use_container_width=True)
        
        # Visualisasi Tren PM2.5 Bulanan Berdasarkan Kategori Wilayah
        if show_monthly_kategori:
            st.subheader("Tren PM2.5 Bulanan Berdasarkan Kategori Wilayah")
            
            # Filter data berdasarkan kategori wilayah yang dipilih
            filtered_kategori_data = all_data_df[all_data_df['Kategori'].isin(selected_kategori)]
            
            # Agregasi data bulanan
            kategori_monthly_data = []
            for kategori, df in filtered_kategori_data.groupby("Kategori"):
                monthly_trend = df.groupby(["year", "month"])["PM2.5_imputed"].mean().reset_index()
                monthly_trend["Year-Month"] = pd.to_datetime(monthly_trend["year"].astype(str) + "-" + monthly_trend["month"].astype(str))
                monthly_trend['Kategori'] = kategori
                kategori_monthly_data.append(monthly_trend)
                
            if kategori_monthly_data:
                kategori_monthly_df = pd.concat(kategori_monthly_data)
                
                fig_kategori = px.line(
                    kategori_monthly_df,
                    x="Year-Month",
                    y="PM2.5_imputed",
                    color="Kategori",
                    title="Tren Bulanan Rata-rata PM2.5 Berdasarkan Kategori Wilayah",
                    labels={"PM2.5_imputed": "Rata-rata PM2.5 (Imputed)", "Year-Month": "Bulan-Tahun"}
                )
                st.plotly_chart(fig_kategori, use_container_width=True)
        
        # Visualisasi Pola Bulanan PM2.5 dalam setahun
        if show_monthly_pattern:
            st.subheader("Pola Bulanan PM2.5 Dalam Setahun")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Pola rata-rata semua stasiun
                monthly_avg_all = all_data_df.groupby("month")["PM2.5_imputed"].mean().reset_index()
                
                fig_monthly_all = px.line(
                    monthly_avg_all,
                    x="month",
                    y="PM2.5_imputed",
                    markers=True,
                    title="Rata-rata PM2.5 per Bulan (Semua Stasiun)",
                    labels={"PM2.5_imputed": "Rata-rata PM2.5", "month": "Bulan"}
                )
                fig_monthly_all.update_xaxes(
                    tickvals=list(range(1, 13)),
                    ticktext=["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
                )
                st.plotly_chart(fig_monthly_all, use_container_width=True)
            
            with col2:
                # Pola bulanan berdasarkan kategori
                filtered_kategori_data = all_data_df[all_data_df['Kategori'].isin(selected_kategori)]
                kategori_monthly_pattern = []
                
                for kategori, df in filtered_kategori_data.groupby("Kategori"):
                    monthly_avg = df.groupby("month")["PM2.5_imputed"].mean().reset_index()
                    monthly_avg['Kategori'] = kategori
                    kategori_monthly_pattern.append(monthly_avg)
                
                if kategori_monthly_pattern:
                    kategori_monthly_pattern_df = pd.concat(kategori_monthly_pattern)
                    
                    fig_monthly_kategori = px.line(
                        kategori_monthly_pattern_df,
                        x="month",
                        y="PM2.5_imputed",
                        color="Kategori",
                        markers=True,
                        title="Rata-rata PM2.5 per Bulan Berdasarkan Kategori",
                        labels={"PM2.5_imputed": "Rata-rata PM2.5", "month": "Bulan"}
                    )
                    
                    # Meningkatkan ukuran grafik
                    fig_monthly_kategori.update_layout(
                        height=500,  # Menambahkan tinggi spesifik
                        margin=dict(l=50, r=50, b=50, t=80),  # Menyesuaikan margin
                        legend=dict(
                            orientation="v",  
                            yanchor="top",
                            y=0.95, 
                            xanchor="left",
                            x=1.02  
                        )
                    )
                    
        # Memperbaiki format label sumbu x
        fig_monthly_kategori.update_xaxes(
            tickvals=list(range(1, 13)),
            ticktext=["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"],
            tickangle=0  # Menjaga label horizontal
        )
        
        # Memperjelas grid untuk kemudahan membaca
        fig_monthly_kategori.update_yaxes(
            gridcolor='rgba(200, 200, 200, 0.2)',  # Grid lebih transparan
            showgrid=True
        )
        
        # Gunakan custom width alih-alih use_container_width
        st.plotly_chart(fig_monthly_kategori, use_container_width=False, width=650)
        
        # Boxplot Perbandingan Distribusi
        if show_boxplot and selected_stations:
            st.subheader("Perbandingan Distribusi PM2.5 Antar Stasiun")
            
            # Kumpulkan data agregat bulanan dari semua stasiun yang dipilih
            all_data = []
            for station in selected_stations:
                temp = get_monthly_stats(cleaned_dataframes[station])
                temp['Station'] = station
                all_data.append(temp)
            
            if all_data:
                all_data_df_selected = pd.concat(all_data)
                
                fig_box = px.box(
                    all_data_df_selected,
                    x="Station",
                    y="mean",
                    title="Distribusi Rata-rata Bulanan PM2.5 per Stasiun",
                    labels={"mean": "Rata-rata PM2.5 (Imputed)"}
                )
                st.plotly_chart(fig_box, use_container_width=True)
        
        # Visualisasi perbandingan kategori wilayah
        if show_kategori_comparison:
            st.subheader("Perbandingan PM2.5 Berdasarkan Kategori Wilayah")
            
            # Filter data berdasarkan kategori yang dipilih
            filtered_kategori_data = all_data_df[all_data_df['Kategori'].isin(selected_kategori)]
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Bar chart rata-rata PM2.5 per kategori
                pm25_per_kategori = filtered_kategori_data.groupby("Kategori")["PM2.5_imputed"].mean().reset_index()
                
                fig_bar_kategori = px.bar(
                    pm25_per_kategori,
                    x="Kategori",
                    y="PM2.5_imputed",
                    color="Kategori",
                    title="Rata-rata PM2.5 Berdasarkan Kategori Wilayah",
                    labels={"PM2.5_imputed": "Rata-rata PM2.5", "Kategori": "Kategori Wilayah"}
                )
                st.plotly_chart(fig_bar_kategori, use_container_width=True)
            
            with col2:
                # Boxplot distribusi PM2.5 per kategori
                fig_box_kategori = px.box(
                    filtered_kategori_data,
                    x="Kategori",
                    y="PM2.5_imputed",
                    color="Kategori",
                    title="Distribusi PM2.5 Berdasarkan Kategori Wilayah",
                    labels={"PM2.5_imputed": "PM2.5", "Kategori": "Kategori Wilayah"}
                )
                st.plotly_chart(fig_box_kategori, use_container_width=True)
        
        # Matriks Korelasi
        if show_corr:
            st.subheader("Matriks Korelasi Parameter")
            
            # Pilih hanya kolom numerik yang relevan untuk korelasi
            relevant_cols = ["PM2.5_imputed", "PM10_imputed", "SO2_imputed", "NO2_imputed",
                            "CO_imputed", "O3_imputed", "TEMP_imputed", "PRES_imputed", 
                            "DEWP_imputed", "WSPM_imputed"]
            
            # Filter data berdasarkan stasiun yang dipilih
            filtered_station_data = all_data_df[all_data_df['No'].isin([cleaned_dataframes[station]['No'][0] for station in selected_stations])]
            
            numeric_df = filtered_station_data[relevant_cols]
            
            # Hitung matriks korelasi
            corr_matrix = numeric_df.corr().round(2)
            
            # Visualisasi korelasi dengan plotly
            fig_corr = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.index,
                text=corr_matrix.values,
                texttemplate="%{text}",
                textfont={"size": 10},
                hoverongaps=False,
                colorscale="RdBu"
            ))
            
            fig_corr.update_layout(
                title="Matriks Korelasi Antar Parameter",
                height=600
            )
            
            st.plotly_chart(fig_corr, use_container_width=True)
        
        # Visualisasi faktor yang mempengaruhi PM2.5
        if show_factors:
            st.subheader("Faktor yang Mempengaruhi PM2.5")
            
            # Fokus pada faktor yang lebih relevan (berdasarkan korelasi)
            factors = ["DEWP_imputed", "WSPM_imputed"]
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Scatter plot untuk DEWP
                fig_dewp = px.scatter(
                    all_data_df,
                    x="DEWP_imputed",
                    y="PM2.5_imputed",
                    opacity=0.3,
                    title="Hubungan Titik Embun (DEWP) dengan PM2.5",
                    labels={"DEWP_imputed": "Titik Embun", "PM2.5_imputed": "PM2.5"}
                )
                st.plotly_chart(fig_dewp, use_container_width=True)
            
            with col2:
                # Scatter plot untuk WSPM
                fig_wspm = px.scatter(
                    all_data_df,
                    x="WSPM_imputed",
                    y="PM2.5_imputed",
                    opacity=0.3,
                    title="Hubungan Kecepatan Angin (WSPM) dengan PM2.5",
                    labels={"WSPM_imputed": "Kecepatan Angin", "PM2.5_imputed": "PM2.5"}
                )
                st.plotly_chart(fig_wspm, use_container_width=True)
    
    with tab2:
        st.header("Kesimpulan Analisis")
        
        st.subheader("1. Tren Perubahan Konsentrasi PM2.5")
        st.markdown("""
        - Konsentrasi PM2.5 mengalami pola musiman yang jelas, dengan peningkatan signifikan pada akhir tahun hingga awal tahun berikutnya, dan penurunan selama pertengahan tahun.
        - Tren ini konsisten di semua stasiun, menunjukkan adanya faktor musiman yang memengaruhi kualitas udara, seperti kondisi atmosfer yang stabil dan peningkatan aktivitas pemanasan pada musim dingin.
        - Wilayah industri dan perkotaan memiliki tingkat PM2.5 lebih tinggi dibandingkan wilayah pinggiran/suburban dan sejarah & budaya, mengindikasikan bahwa aktivitas manusia berperan besar dalam meningkatkan polusi udara.
        """)
        
        st.subheader("2. Faktor yang Memengaruhi Perubahan Kualitas Udara")
        st.markdown("""
        - Faktor lingkungan memiliki pengaruh yang bervariasi terhadap konsentrasi PM2.5.
        - Kecepatan angin (WSPM) memiliki korelasi negatif (-0.22) dengan PM2.5, menunjukkan bahwa angin membantu menyebarkan polutan dan mengurangi konsentrasinya.
        - Titik embun (DEWP) memiliki korelasi positif (0.20), yang menunjukkan bahwa kelembapan dapat mempengaruhi akumulasi polutan di udara.
        - Suhu (TEMP) dan tekanan udara (PRES) memiliki korelasi yang sangat rendah dengan PM2.5, menunjukkan bahwa faktor ini tidak berdampak signifikan terhadap polusi udara.
        """)
        
        st.subheader("3. Sumber Polusi dan Korelasi dengan Polutan Lain")
        st.markdown("""
        - PM2.5 memiliki korelasi tinggi dengan PM10 (0.78), yang menunjukkan bahwa keduanya kemungkinan berasal dari sumber yang sama, seperti emisi kendaraan dan industri.
        - CO dan NO2 juga memiliki korelasi sedang dengan PM2.5 (0.62 dan 0.53), menegaskan bahwa aktivitas transportasi berkontribusi besar terhadap polusi udara.
        - SO2 memiliki korelasi lebih rendah (0.31), yang menunjukkan bahwa pembakaran batu bara dan aktivitas industri masih berpengaruh, tetapi tidak sebesar transportasi.
        """)
        
        st.subheader("4. Rekomendasi")
        st.markdown("""
        - **Pengawasan dan intervensi lebih ketat pada periode kritis**, terutama pada bulan-bulan dengan konsentrasi PM2.5 tertinggi.
        - **Peningkatan kebijakan ramah lingkungan**, terutama di wilayah perkotaan dan industri, untuk mengurangi dampak emisi kendaraan.
        - **Pemantauan dan analisis lanjutan di wilayah dengan konsentrasi PM2.5 tinggi**, guna mengidentifikasi sumber spesifik polusi dan menentukan kebijakan mitigasi yang lebih efektif.
        - **Penerapan sistem peringatan dini** berbasis faktor lingkungan seperti kecepatan angin dan kelembapan, untuk memperkirakan potensi lonjakan polusi udara.
        - **Penyesuaian kebijakan pengendalian emisi** dengan mempertimbangkan faktor lokal dan musim, agar strategi mitigasi lebih tepat sasaran.
        """)
        
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Pastikan folder 'csv' berisi file-file data yang diperlukan.")