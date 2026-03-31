# Panduan Setup Environment & Inisialisasi Project

Dokumen ini berisi langkah-langkah teknis untuk menyiapkan lingkungan pengembangan (development environment) menggunakan Python.

---

## 1. Setup Virtual Environment (venv)
Gunakan *virtual environment* untuk mengisolasi dependensi agar tidak bentrok dengan library sistem.

### Windows
```bash
# Membuat environment
python -m venv venv

# Aktivasi
.\venv\Scripts\activate

Ciri Berhasil: Akan muncul teks (venv) di sebelah kiri command prompt kamu, seperti ini:
(venv) C:\Users\NamaKamu\Project>

#Install library
pip flask

#Testing development di web
flask --app main run