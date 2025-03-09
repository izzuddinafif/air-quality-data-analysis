# Proyek Analisis Data: Analisis Kualitas Udara (PM2.5)

Proyek ini merupakan analisis data eksploratif terhadap dataset kualitas udara yang memuat informasi tentang konsentrasi PM2.5 dan parameter terkait (PM10, SO2, NO2, CO, O3, TEMP, PRES, DEWP, RAIN, WSPM) dari berbagai stasiun monitoring. Tujuan utama analisis ini adalah:

1. **Tren Konsentrasi PM2.5:**  
   Menjawab pertanyaan bisnis “Bagaimana tren konsentrasi PM2.5 di masing-masing stasiun dari waktu ke waktu?” melalui visualisasi time series dan agregasi musiman (misalnya rata-rata bulanan).

2. **Perbedaan Kualitas Udara Antar Stasiun:**  
   Menjawab pertanyaan “Apakah terdapat perbedaan signifikan dalam kualitas udara antar stasiun, dan faktor apa yang mungkin menyebabkannya?” dengan membandingkan distribusi nilai PM2.5 antar stasiun serta melakukan analisis korelasi antara PM2.5 dengan parameter lain.

Proyek ini mencakup seluruh proses analisis data, mulai dari pembersihan data (data cleaning) hingga visualisasi dan eksplorasi untuk menarik insight yang mendalam.

---

## Struktur Proyek

```
submission/
├── dashboard/
│   └── app.py                # Kode dashboard Streamlit
├── csv/                     # Folder berisi dataset CSV (misal: PRSA_Data_*.csv)
├── Proyek_Analisis_Data.ipynb  # Notebook Jupyter yang mendokumentasikan proses analisis
├── README.md                 # Dokumentasi ini
├── requirements.txt          # Daftar dependencies yang digunakan
└── url.txt                   # (Opsional) Tautan untuk dashboard (jika di-deploy secara online)
```

---

## Cara Menjalankan Proyek

### 1. Menjalankan Notebook Analisis Data

- Pastikan Anda telah menginstall Jupyter Notebook atau JupyterLab.
- Buka file `Proyek_Analisis_Data.ipynb` untuk melihat proses analisis data mulai dari data wrangling hingga eksplorasi dan visualisasi.

### 2. Menjalankan Dashboard dengan Streamlit

- Pastikan Anda telah menginstall Streamlit dan semua library yang tercantum pada `requirements.txt`.
- Buka terminal atau command prompt, arahkan ke direktori proyek, kemudian jalankan perintah berikut:

  ```bash
  streamlit run dashboard/app.py
  ```

- Dashboard akan terbuka di browser (biasanya di <http://localhost:8501>). Dashboard ini menyajikan visualisasi interaktif untuk menjawab pertanyaan bisnis seputar tren PM2.5 dan perbandingan kualitas udara antar stasiun.

---

## Dependencies

Pastikan Anda menginstall semua dependencies yang dibutuhkan. Anda dapat menginstallnya menggunakan perintah:

```bash
pip install -r requirements.txt
```

Dependencies yang digunakan antara lain:

- pandas
- numpy
- matplotlib
- seaborn
- streamlit

---

## Insight Utama dari Analisis

1. **Tren Waktu dan Musiman:**  
   Visualisasi time series dan agregasi bulanan mengungkapkan pola fluktuasi PM2.5, termasuk potensi tren naik/turun dan pengaruh musiman.

2. **Perbedaan Antar Stasiun:**  
   Boxplot perbandingan antar stasiun menunjukkan adanya variasi dalam kualitas udara, di mana beberapa stasiun consistently menunjukkan nilai PM2.5 yang lebih tinggi. Analisis korelasi juga mengungkap faktor-faktor yang mungkin mempengaruhi perbedaan ini.

3. **Pembersihan Data Efektif:**  
   Proses imputasi missing (dengan interpolasi) dan penanganan outlier (dengan imputasi menggunakan median) membuat data lebih representatif, sehingga analisis lebih lanjut menjadi lebih akurat.

---

## Catatan

- Proyek ini merupakan bagian dari latihan analisis data dan ditujukan untuk memberikan gambaran lengkap mengenai seluruh proses analisis data, dari pengumpulan, pembersihan, eksplorasi, hingga pembuatan dashboard interaktif.
- Jika Anda memiliki pertanyaan atau membutuhkan penjelasan lebih lanjut, silakan hubungi saya.
