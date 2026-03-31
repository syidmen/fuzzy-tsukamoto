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

## 1. Gunakan Branching (Jangan Push ke Main!)
Jangan pernah melakukan `git push` langsung ke branch `main`. Selalu buat branch baru untuk setiap fitur atau perbaikan.

* **Main Branch:** Hanya untuk kode yang sudah stabil dan siap jalan.
* **Feature Branch:** Untuk ngoding fitur baru (contoh: `feat-login`, `feat-api-flask`).
* **Fix Branch:** Untuk benerin bug (contoh: `fix-styling`, `fix-route-error`).

**Cara membuat branch di terminal:**
```bash
git checkout -b nama-fitur-baru