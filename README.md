# Proyek Analisis Data: Kualitas Udara (PM2.5)

Proyek ini bertujuan untuk melakukan analisis eksploratif pada dataset kualitas udara dengan fokus pada parameter **PM2.5**. Analisis dilakukan untuk memahami tren kualitas udara dari waktu ke waktu, mengidentifikasi faktor-faktor penyebab perbedaan kualitas udara antar lokasi, serta menyajikan dashboard interaktif yang memudahkan eksplorasi data.

---

## Tujuan Proyek

1. **Menganalisis Tren PM2.5 di Masing-Masing Stasiun**  
   - Menggunakan visualisasi *time series* dan agregasi musiman (misalnya, rata-rata bulanan) untuk mengidentifikasi pola dan fluktuasi konsentrasi PM2.5.

2. **Menemukan Faktor Penyebab Perbedaan Kualitas Udara Antar Stasiun**  
   - Memanfaatkan *boxplot* untuk membandingkan distribusi PM2.5 di setiap stasiun.  
   - Menganalisis korelasi PM2.5 dengan parameter lain (PM10, NO2, CO, O3, dan kondisi cuaca) guna melihat sumber polusi yang potensial.

---

## Struktur Proyek

```
submission/
├── csv/                         # Folder CSV dataset
│   ├── PRSA_Data_...            
│   └── ...
├── dashboard/
│   └── app.py                   # Dashboard interaktif Streamlit
├── Proyek_Analisis_Data.ipynb   # Notebook utama analisis eksploratif
├── requirements.txt             # Library Python yang dibutuhkan
├── url.txt                      # URL dashboard
└── README.md                    # Dokumentasi proyek
```

1. **dashboard/app.py**  
   File utama untuk menjalankan dashboard interaktif.

2. **Proyek_Analisis_Data.ipynb**  
   Notebook Jupyter yang memuat proses EDA, data cleaning, dan analisis lanjutan.

3. **requirements.txt**  
   Daftar library Python yang diperlukan.

4. **url.txt**  
   (Opsional) Menyimpan link jika dashboard di-*deploy* secara online.

---

## Panduan Menjalankan Proyek

### 1. Menjalankan Notebook

1. **Instal dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Jalankan Jupyter Notebook**:

   ```bash
   jupyter notebook Proyek_Analisis_Data.ipynb
   ```

3. **Eksplorasi Notebook**  
   Notebook memuat tahapan EDA (menampilkan contoh data, descriptive statistics, agregasi, dan visualisasi), proses cleaning (interpolasi missing value dan imputasi outlier), serta analisis lanjutan untuk menjawab pertanyaan bisnis.

### 2. Menjalankan Dashboard Interaktif (Streamlit)

1. **Jalankan perintah berikut di terminal** pada direktori proyek:

   ```bash
   streamlit run dashboard/app.py
   ```

2. **Akses Dashboard**  
   - Secara default, dashboard akan terbuka di browser pada alamat [http://localhost:8501](http://localhost:8501).  
   - Di sidebar, Anda dapat memilih stasiun serta menampilkan atau menyembunyikan berbagai grafik.  
   - Terdapat slider interaktif untuk memfilter data berdasarkan rentang waktu, memudahkan analisis tren PM2.5 secara mendalam.

---

## Dependencies Utama

- **pandas**  
- **numpy**  
- **matplotlib**  
- **seaborn**  
- **streamlit**  
- **plotly** (untuk visualisasi interaktif)

> Instal semua dependencies sekaligus menggunakan:
>
> ```bash
> pip install -r requirements.txt
> ```

---

## Insight dari Analisis

- **Tren PM2.5**  
  Konsentrasi PM2.5 menunjukkan pola musiman dengan nilai yang lebih tinggi pada periode tertentu (misalnya, musim dingin), diduga dipengaruhi oleh suhu, curah hujan, dan aktivitas manusia (seperti pembakaran dan pemanasan).

- **Perbedaan Antar Stasiun**  
  Distribusi PM2.5 antar stasiun bervariasi cukup signifikan. Beberapa stasiun memiliki median PM2.5 lebih tinggi, mengindikasikan sumber polusi lokal seperti aktivitas industri atau padatnya lalu lintas. Korelasi tinggi antara PM2.5 dan polutan lain (PM10, NO2, CO) menunjukkan kemungkinan besar sumber emisi yang serupa.

- **Efektivitas Data Cleaning**  
  Proses interpolasi *missing values* dan imputasi outlier dengan median terbukti menurunkan bias pada nilai rata-rata. Data menjadi lebih siap untuk analisis trend dan korelasi.

---

## Kontak

Untuk pertanyaan lebih lanjut atau kolaborasi, silakan hubungi:

- **Nama**: Izzuddin Ahmad Afif  
- **Email**: [izzuddinafif@gmail.com](mailto:izzuddinafif@gmail.com)  
- **ID Dicoding**: izzuddinafif

Terima kasih telah mengunjungi proyek ini. Semoga analisis dan *dashboard* yang disediakan dapat membantu dalam memahami dinamika kualitas udara dan menjadi acuan untuk tindakan atau kebijakan lebih lanjut.
