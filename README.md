# Proyek Analisis Data: Kualitas Udara (PM2.5)

Proyek ini merupakan analisis eksploratif dataset kualitas udara dengan fokus pada parameter PM2.5. Analisis dilakukan untuk memahami tren kualitas udara dari waktu ke waktu serta mengidentifikasi faktor-faktor yang menyebabkan perbedaan kualitas udara antar lokasi.

## Tujuan Proyek

Proyek ini bertujuan menjawab dua pertanyaan bisnis utama:

1. **Bagaimana tren konsentrasi PM2.5 di masing-masing stasiun dari waktu ke waktu?**
   - Dianalisis menggunakan visualisasi time series dan agregasi musiman (misalnya rata-rata bulanan).

2. **Apa faktor penyebab perbedaan kualitas udara antar stasiun?**
   - Dilakukan analisis distribusi PM2.5 antar lokasi menggunakan boxplot.
   - Dilakukan analisis korelasi dengan parameter lain (misalnya PM10, NO2, CO, O3, dan parameter cuaca).

## Struktur Proyek

```
submission/
├── dashboard/
│   └── app.py                   # Dashboard interaktif Streamlit
├── Proyek_Analisis_Data.ipynb  # Notebook utama analisis eksploratif
├── requirements.txt             # Library Python yang dibutuhkan
├── url.txt                     # (Opsional) URL dashboard jika di-host online
└── README.md              # Dokumentasi proyek
```

## Panduan Menjalankan Proyek

### Menjalankan Notebook

1. Instal dependencies:

```bash
pip install -r requirements.txt
```

2. Jalankan Jupyter Notebook:

```bash
jupyter notebook Proyek_Analisis_Data.ipynb
```

### Menjalankan Dashboard Interaktif (Streamlit)

1. Jalankan perintah berikut di terminal pada direktori proyek:

```bash
streamlit run dashboard/app.py
```

2. Dashboard akan otomatis terbuka di browser, biasanya pada alamat <http://localhost:8501>.

## Dependencies Utama

- pandas
- numpy
- matplotlib
- seaborn
- streamlit

Instal semua dependencies sekaligus menggunakan perintah berikut:

```bash
pip install -r requirements.txt
```

## Insight dari Analisis

- **Tren PM2.5:**
  - Konsentrasi PM2.5 menunjukkan pola musiman dengan nilai tinggi pada periode tertentu (misalnya musim dingin), dipengaruhi kondisi cuaca dan aktivitas manusia.

- **Perbedaan Antar Stasiun:**
  - Terdapat perbedaan signifikan kualitas udara antar lokasi yang dipengaruhi aktivitas industri lokal, lalu lintas kendaraan, serta kondisi geografis setempat.
  - Korelasi tinggi antara PM2.5 dengan parameter lain (PM10, CO, NO2) menunjukkan potensi sumber polutan yang serupa.

- **Efektivitas Data Cleaning:**
  - Proses interpolasi missing values dan imputasi outlier dengan median berhasil meningkatkan kualitas data untuk analisis lanjutan.

---

Jika terdapat pertanyaan atau kebutuhan lebih lanjut terkait proyek ini, jangan ragu untuk menghubungi saya.

**Izzuddin Ahmad Afif**

- Email: <izzuddinafif@gmail.com>
- ID Dicoding: izzuddinafif
