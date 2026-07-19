<div align="center">
  <h1 style="color: #4CAF50;">🚀 Arlen-Spam-OTP</h1>
</div>

> **⚠️ PERINGATAN: Untuk Tujuan Edukasi dan Pengujian Keamanan Saja ⚠️**
>
> Penggunaan tools ini untuk spam, gangguan, atau aktivitas ilegal lainnya adalah **TANGGUNG JAWAB PENGGUNA**. Penulis tidak bertanggung jawab atas penyalahgunaan. Gunakan hanya pada sistem yang Anda miliki atau dengan izin tegas.

---

## 📌 Fitur

| Fitur | Deskripsi |
| :--- | :--- |
| 📨 **Kirim OTP** | Mengirimkan permintaan OTP (One-Time Password) ke berbagai API layanan. |
| 🎯 **Total Api** | Mendukung **20+** target API. |
| 🎨 **UI Menarik** | Antarmuka teks berwarna dengan animasi di terminal. |
| 🔄 **Single Round** | Mode satu kali kirim ke semua API secara berurutan. |
| ♾️ **Infinite Loop** | Mode pengiriman berulang terus-menerus dengan jeda 60 detik. |
| 📱 **Lintas Platform** | Mendukung eksekusi di Termux (Android) dan lingkungan terminal lainnya. |

---

## 📋 Persyaratan (Prerequisites)

Pastikan sistem Anda telah memenuhi persyaratan berikut sebelum menggunakan tools ini:

*   **Python 3.7+**
*   **pip** (Python package installer)
*   Koneksi internet yang stabil

---

## 🔧 Instalasi (Windows / Linux)

Ikuti langkah-langkah berikut untuk menginstal dan menjalankan tools ini di lingkungan desktop/server:

1. **Clone Repository**
   ```bash
   git clone https://github.com/danzzzzgantengbgt/Arlen-Spam-OTP.git
   cd Arlen-Spam-OTP
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan Tools**
   ```bash
   python main.py
   ```

---

## 🐧 Instalasi di Termux (Android)

Bagi pengguna Android, Anda dapat menjalankan tools ini menggunakan emulator terminal Termux:

1. **Update & Install Packages**
   ```bash
   pkg update && pkg upgrade
   pkg install python git
   ```

2. **Clone Repository**
   ```bash
   git clone https://github.com/danzzzzgantengbgt/Arlen-Spam-OTP.git
   cd Arlen-Spam-OTP
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan Tools**
   ```bash
   python main.py
   ```

---

## 🎮 Cara Penggunaan

1. Setelah menjalankan `python main.py`, Anda akan melihat menu utama pada terminal.
2. Pilih mode eksekusi yang diinginkan:
   *   **Single Round:** Mengirim OTP satu kali ke semua daftar API.
   *   **Infinite Loop:** Mengirim OTP secara berulang dengan jeda (delay) 60 detik di setiap perulangan.
3. Masukkan nomor telepon target saat diminta. **Format yang diterima:**
   *   `08xxxxxxxxxx` *(contoh: 081234567890)*
   *   `628xxxxxxxxxx` *(contoh: 6281234567890)*
   *   `+628xxxxxxxxxx` *(contoh: +6281234567890)*
4. Tunggu hingga proses selesai atau tekan `CTRL + C` untuk menghentikan program secara paksa.

---

## 📂 Struktur File

Berikut adalah penjelasan mengenai struktur direktori pada repository ini:

| Nama File / Folder | Deskripsi |
| :--- | :--- |
| `main.py` | Entry point dan antarmuka utama CLI |
| `main_engine.py` | Mesin/core logika pengiriman OTP |
| `handlers.py` | Fungsi handler untuk melakukan *request* ke setiap target API |
| `targets.py` | Konfigurasi dan daftar URL target API |
| `utils.py` | Fungsi utilitas tambahan (misalnya untuk memformat nomor telepon) |
| `useragents.py` | Daftar *User-Agent* acak untuk merotasi request |
| `requirements.txt`| Daftar pustaka/dependensi Python yang dibutuhkan |
| `README.md` | Dokumentasi utama repository ini |

---

## ⚠️ Disclaimer & Catatan Hukum

1. **Penggunaan:** Tools ini dibuat semata-mata untuk tujuan edukasi dan pengujian keamanan pada sistem Anda sendiri.
2. **Tanggung Jawab:** Pengguna sepenuhnya bertanggung jawab atas setiap konsekuensi hukum yang timbul dari penggunaan tools ini.
3. **Larangan:** Dilarang keras menggunakan tools ini untuk:
   *   Mengganggu atau merusak layanan milik orang lain.
   *   Melakukan tindakan yang melanggar hukum di yurisdiksi Anda.
   *   Melakukan spamming atau pelecehan.
4. **Dukungan API:** Tools ini bergantung pada API pihak ketiga yang bersifat dinamis. API tersebut dapat berubah atau dinonaktifkan oleh pemilik layanan sewaktu-waktu.
5. **Kode Etik:** Pengguna diharapkan menggunakan tools ini secara bijak, etis, dan bertanggung jawab.

---

## Opsn Source 

Script ini open source atau sumber terbuka,jadi kamu bebas memodifikasi atau mengambil api yang tersedia asalkan mematuhi syarat dan ketentuan 

---

## 📜 Lisensi

Proyek ini dilisensikan di bawah **MIT License**.

---

<br>
<div align="center">
  <b>Dibuat oleh: Aldan</b><br>
  <i>Versi: 1.0.0</i>
</div>
