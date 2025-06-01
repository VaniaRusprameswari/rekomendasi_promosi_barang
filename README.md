# 💡 Kasir Pintar: Asisten Promosi Barang Berbasis Data Penjualan
Proyek ini adalah aplikasi Python berbasis AI sederhana yang menganalisis data penjualan mingguan dan memberikan rekomendasi promosi barang berdasarkan margin keuntungan, tren penjualan, prediksi permintaan, dan stok barang.

## 🚀 Fitur Utama
- 📊 **Prediksi Penjualan** menggunakan algoritma *Random Forest Regressor*
- 📈 **Evaluasi Tren Penjualan Mingguan** (Menurun / Stabil / Meningkat)
- 💰 **Penghitungan Margin Kotor** secara otomatis
- 🧮 **Skoring Kelayakan Promosi** berdasarkan margin, prediksi, dan stok
- ✅ **Rekomendasi Diskon Optimal** dan **Hari Terbaik Promosi**
- ❌ **Penyaringan Otomatis Barang Tidak Layak Promosi**

## 📌 Logika Rekomendasi Promosi
Sebuah barang direkomendasikan untuk dipromosikan jika memenuhi semua kriteria berikut:
1. **Kategori Rentan**: Termasuk kategori makanan, makanan cepat saji, atau sayuran
2. **Skor Promosi Sedang atau Tinggi**
3. **Tren Penjualan Menurun atau Stabil**
Barang yang tidak memenuhi akan diberikan penjelasan singkat alasan penolakannya.

## 🛠️ Cara Menjalankan
1. Pastikan Python 3 sudah terinstal
2. Instal dependensi: pip install pandas numpy scikit-learn
3. Jalankan program: python kasir_ai.py

## 🧠 Teknologi yang Digunakan
- Python 3
- Pandas
- NumPy
- Scikit-Learn (Linear Regression)

## 👩‍💻 Kontributor
Nama: VANIA RUSPRAMESWARI
NIM: 23050974073
Mata Pelajaran: Kecerdasan Buatan (AI)
