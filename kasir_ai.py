import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import warnings

warnings.filterwarnings("ignore")

# KONFIGURASI
TARGET_PENJUALAN = 20
MIN_MARGIN = 10  # persen
SKALA_TREND = ['Menurun', 'Stabil', 'Meningkat']
SKALA_SKOR = ['Rendah', 'Sedang', 'Tinggi']

# MUAT DATA PENJUALAN
try:
    df = pd.read_csv("data/data_penjualan.csv", parse_dates=['tanggal'])
except FileNotFoundError:
    print("❌ File data_penjualan.csv tidak ditemukan.")
    exit()

# FUNGSI PEMBANTU
def hitung_margin(beli, jual):
    if jual == 0: return 0
    return (jual - beli) / jual * 100

def evaluasi_tren(mingguan):
    if len(mingguan) < 2:
        return 'Stabil'
    model = LinearRegression()
    X = np.array(range(len(mingguan))).reshape(-1, 1)
    y = mingguan.values.reshape(-1, 1)
    model.fit(X, y)
    slope = model.coef_[0][0]
    if slope > 1:
        return 'Meningkat'
    elif slope < -1:
        return 'Menurun'
    return 'Stabil'

def beri_skor(margin, prediksi, stok):
    skor = 0
    if margin >= MIN_MARGIN:
        skor += 1
    if prediksi <= stok * 0.3:
        skor += 1
    if stok > 5:
        skor += 1
    return SKALA_SKOR[min(skor, len(SKALA_SKOR) - 1)]

# FUNGSI MODEL AI
def model_prediksi_ai(X, y, next_index):
    if len(X) < 3:
        return None  # tidak cukup data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)
    x_pred = scaler.transform([[next_index]])
    return int(model.predict(x_pred)[0])

# PROSES TIAP BARANG
for barang_id in df['id_barang'].unique():
    data_barang = df[df['id_barang'] == barang_id].copy()
    info = data_barang.iloc[0]

    # Penjualan mingguan
    data_barang['minggu_ke'] = data_barang['tanggal'].dt.isocalendar().week
    mingguan = data_barang.groupby('minggu_ke')['jumlah'].sum()
    rata2_mingguan = mingguan.mean()

    margin = hitung_margin(info['harga_beli'], info['harga_jual'])
    trend = evaluasi_tren(mingguan)

    # Prediksi penjualan minggu depan dengan AI
    prediksi = None
    try:
        minggu_ke = mingguan.index.values
        jumlah = mingguan.values
        X = np.array(minggu_ke).reshape(-1, 1)
        y = jumlah
        prediksi = model_prediksi_ai(X, y, next_index=max(minggu_ke) + 1)
    except Exception as e:
        print(f"[⚠️ AI Error] Prediksi gagal untuk {info['nama_barang']}: {e}")

    # Fallback prediksi jika model gagal
    if prediksi is None or prediksi < 0:
        prediksi = int(rata2_mingguan * 1.5)

    skor_promosi = beri_skor(margin, prediksi, info['stok'])

    # Kriteria barang rentan atau pernah dipromosikan (dummy check)
    kategori_rentan = info['kategori'].lower() in ['makanan', 'makanan cepat saji', 'sayuran']

    # Rekomendasi Promosi
    if skor_promosi in ['Tinggi', 'Sedang'] and trend in ['Menurun', 'Stabil'] and kategori_rentan:
        diskon_opt = min(margin, 20)
        harga_promo = int(info['harga_jual'] * (1 - diskon_opt / 100))
        hari_terbaik = data_barang['tanggal'].dt.day_name().mode()[0]

        print("\n==============================")
        print("📦 REKOMENDASI PROMOSI BARANG")
        print("==============================")
        print(f"ID Barang       : {barang_id}")
        print(f"Nama            : {info['nama_barang']}")
        print(f"Kategori        : {info['kategori']}")
        print(f"Stok Saat Ini   : {info['stok']} pcs")
        print(f"Margin Kotor    : {margin:.1f}%")
        print(f"Tren Penjualan  : {trend}")
        print(f"Prediksi Minggu Depan: {prediksi} pcs")
        print(f"Skor Promosi    : {skor_promosi}")
        print(f"🟢 DISKON OPTIMAL : {diskon_opt:.0f}% → Harga Promo: Rp{harga_promo}")
        print(f"📅 Hari Terbaik Promo: {hari_terbaik}")
    else:
        print(f"\n🔴 Barang '{info['nama_barang']}' *tidak layak dipromosikan* saat ini.")
        print(f"ℹ️ Alasan: Tren: {trend}, Margin: {margin:.1f}%, Prediksi: {prediksi} pcs, Stok: {info['stok']}")