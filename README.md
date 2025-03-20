# Proyek Analisis Data: Kualitas Udara (PM2.5)

Proyek ini bertujuan untuk melakukan analisis eksploratif pada dataset kualitas udara dengan fokus pada parameter **PM2.5**. Analisis dilakukan untuk memahami tren kualitas udara dari waktu ke waktu, mengidentifikasi faktor-faktor penyebab perbedaan kualitas udara antar lokasi, serta menyajikan **dashboard interaktif** yang memudahkan eksplorasi data.

---

## **Tujuan Proyek**

1. **Menganalisis Tren PM2.5 di Masing-Masing Stasiun**  
   - Menggunakan visualisasi *time series* dan agregasi musiman (rata-rata bulanan) untuk mengidentifikasi pola dan fluktuasi konsentrasi PM2.5.

2. **Menemukan Faktor Penyebab Perbedaan Kualitas Udara Antar Stasiun**  
   - Memanfaatkan *boxplot* untuk membandingkan distribusi PM2.5 di setiap stasiun.  
   - Menganalisis korelasi PM2.5 dengan parameter lain (*PM10, NO2, CO, O3*, dan faktor cuaca) guna melihat sumber polusi yang potensial.

---

## **Struktur Proyek**

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

### **Penjelasan File**

1. **dashboard/app.py**  
   - File utama untuk menjalankan **dashboard interaktif Streamlit** yang memungkinkan eksplorasi data kualitas udara secara visual.

2. **Proyek_Analisis_Data.ipynb**  
   - Notebook utama yang memuat **EDA (Exploratory Data Analysis)**, **data cleaning**, serta **analisis mendalam** terkait PM2.5.

3. **requirements.txt**  
   - Berisi daftar **library Python** yang diperlukan untuk menjalankan proyek.

4. **url.txt**  
   - Jika proyek dideploy online, file ini akan menyimpan **URL dashboard**.

---

## **Panduan Menjalankan Proyek**

### **1️⃣ Menjalankan Notebook**

1. **Instal dependensi** dengan menjalankan perintah berikut di terminal:  

   ```
   pip install -r requirements.txt
   ```

2. **Jalankan Jupyter Notebook** untuk melakukan eksplorasi dataset:  

   ```
   jupyter notebook Proyek_Analisis_Data.ipynb
   ```

3. **Eksplorasi Notebook**  
   - Notebook ini memuat tahapan **EDA**, proses **data cleaning** (interpolasi missing values, imputasi outlier), serta **analisis lanjutan** untuk menjawab pertanyaan bisnis terkait kualitas udara.

### **2️⃣ Menjalankan Dashboard Streamlit**

1. **Jalankan perintah berikut di terminal** dalam direktori proyek:  

   ```
   streamlit run dashboard/app.py
   ```

2. **Akses Dashboard**  
   - Secara default, dashboard akan terbuka di browser di alamat:  
     **[http://localhost:8501](http://localhost:8501)**
   - **Fitur utama** dashboard:  
     ✅ Pemilihan **stasiun** secara interaktif  
     ✅ **Visualisasi tren** PM2.5 berdasarkan waktu  
     ✅ **Perbandingan distribusi PM2.5** antar stasiun  
     ✅ **Matriks korelasi** dengan faktor lingkungan

---

## **Dependencies Utama**

- **pandas** (manipulasi data)  
- **numpy** (operasi numerik)  
- **matplotlib & seaborn** (visualisasi data statis)  
- **streamlit** (dashboard interaktif)  
- **plotly** (visualisasi interaktif)

> **Cara install dependencies**:  
>
> ```
> pip install -r requirements.txt
> ```

---

## **Insight dari Analisis**

- **Tren PM2.5**  
  - Konsentrasi PM2.5 menunjukkan **pola musiman**, dengan peningkatan signifikan pada **musim dingin** dan penurunan pada **musim panas**.  
  - Hal ini diduga dipengaruhi oleh **suhu udara, kelembapan, curah hujan**, serta **aktivitas manusia** seperti pembakaran bahan bakar.

- **Perbedaan Antar Stasiun**  
  - Distribusi PM2.5 antar stasiun **bervariasi signifikan**.  
  - Beberapa stasiun memiliki **median PM2.5 yang tinggi**, mengindikasikan adanya **sumber polusi lokal**, seperti **aktivitas industri atau kepadatan lalu lintas**.  
  - Korelasi tinggi antara **PM2.5 dan polutan lain (PM10, NO2, CO)** menunjukkan kemungkinan besar bahwa sumber emisi polusi berasal dari aktivitas yang serupa.

- **Efektivitas Data Cleaning**  
  - **Interpolasi missing values** dan **imputasi outlier** dengan median berhasil **mengurangi bias pada perhitungan rata-rata PM2.5**.  
  - Data yang telah dibersihkan kini **lebih siap** untuk analisis tren dan korelasi.

---

## **Kesimpulan**

✅ **Tren musiman menunjukkan peningkatan PM2.5 pada musim dingin**, mengindikasikan faktor lingkungan dan aktivitas pemanasan sebagai penyebab.  
✅ **Perbedaan konsentrasi PM2.5 antar stasiun menunjukkan adanya sumber polusi lokal**, terutama di area industri dan perkotaan.  
✅ **Korelasi tinggi antara PM2.5 dan PM10, CO, NO2** menunjukkan bahwa sumber emisi utama berasal dari transportasi dan industri.  
✅ **Kecepatan angin memiliki korelasi negatif dengan PM2.5**, yang berarti angin membantu mengurangi polusi udara.  

---

## **Rekomendasi**

📌 **Pengawasan ketat pada periode puncak PM2.5**, terutama **musim dingin**, untuk mengurangi dampak polusi udara.  
📌 **Kebijakan pengurangan emisi kendaraan dan industri** di daerah dengan konsentrasi PM2.5 tinggi.  
📌 **Peningkatan penghijauan dan pengaturan zona industri** untuk membantu mengurangi polusi di area dengan kualitas udara buruk.  
📌 **Sistem peringatan dini** berbasis faktor lingkungan seperti kecepatan angin dan kelembapan, agar bisa memprediksi lonjakan polusi udara.  

---

## **Kontak**

Jika Anda memiliki pertanyaan atau ingin berdiskusi lebih lanjut, silakan hubungi:

- **Nama**: Izzuddin Ahmad Afif  
- **Email**: [izzuddinafif@gmail.com](mailto:izzuddinafif@gmail.com)  
- **ID Dicoding**: izzuddinafif  

Terima kasih telah mengunjungi proyek ini! Semoga analisis dan **dashboard** yang disediakan dapat membantu memahami dinamika kualitas udara dan menjadi acuan bagi tindakan atau kebijakan lebih lanjut.
