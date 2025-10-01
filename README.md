# Movezz

![Status](https://img.shields.io/badge/status-in--development-yellow)
![Build](https://img.shields.io/badge/build-unstable-red)
![Python](https://img.shields.io/badge/python-blue)
![Django](https://img.shields.io/badge/django-5.0-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)


Repositori ini berisi tugas kelompok untuk mata kuliah Pemrograman Berbasis Platform (PBP) Semester 3.

---
## Daftar Anggota Kelompok

- Muhamad Hakim Nizami (2406399485)
- Nadin Ananda (2406351806)
- Heraldo Arman (2406420702)
- Roberto Eugenio Sugiarto (2406355640)
- Amberley Vidya Putri (2406495533)


---
## Deskripsi Proyek

Movezz adalah aplikasi sosial media yang ditujukan untuk para pecinta olahraga, baik itu penggemar sepak bola, pelari, gym, maupun olahraga lainnya. Movezz menyediakan fitur utama seperti feeds beranda untuk berbagi dan melihat aktivitas, profil pengguna, chat dan messaging untuk berkomunikasi antar anggota, serta fitur broadcast untuk mengumumkan informasi penting kepada komunitas.

Movezz hadir sebagai solusi bagi para pecinta olahraga yang ingin terhubung, berbagi pengalaman, dan membangun komunitas secara digital. Aplikasi ini dirancang untuk mengakomodasi berbagai jenis olahraga, mulai dari sepak bola, lari, gym, hingga olahraga rekreasi lainnya. Dengan pendekatan sosial media, Movezz memudahkan pengguna untuk menemukan teman baru yang memiliki minat serupa, serta memperluas jaringan komunitas olahraga mereka.

Fitur feeds beranda memungkinkan pengguna untuk membagikan aktivitas olahraga, pencapaian, tips, atau sekadar update harian kepada komunitas. Setiap pengguna dapat memberikan komentar, menyukai, dan berinteraksi langsung pada postingan, sehingga tercipta suasana yang interaktif dan suportif. Selain itu, pengguna juga dapat mengikuti akun lain untuk mendapatkan update terbaru dari teman atau atlet favorit mereka.

Profil pengguna di Movezz menampilkan informasi pribadi, riwayat aktivitas, serta statistik olahraga yang telah dilakukan. Pengguna dapat menyesuaikan profil sesuai preferensi, menambahkan foto, bio, dan mengatur privasi akun. Fitur ini membantu pengguna untuk membangun identitas digital sebagai bagian dari komunitas olahraga yang aktif dan inspiratif. (tentatif)

Untuk mendukung komunikasi antar anggota, Movezz menyediakan fitur chat dan messaging yang memungkinkan percakapan pribadi. Fitur ini sangat berguna untuk mengatur jadwal latihan bersama, berdiskusi tentang teknik olahraga, atau sekadar berbincang santai. Selain itu, terdapat fitur broadcast yang seseorang untuk mengirimkan pengumuman penting secara massal kepada seluruh anggota.

Dengan berbagai fitur yang terintegrasi, Movezz bertujuan menjadi platform utama bagi para pecinta olahraga di Indonesia. Aplikasi ini tidak hanya memfasilitasi interaksi sosial, tetapi juga mendorong gaya hidup sehat, kolaborasi, dan semangat sportivitas di kalangan penggunanya. Melalui Movezz, diharapkan tercipta ekosistem olahraga digital yang inklusif, inspiratif, dan saling mendukung.

---
## Cara Menjalankan

1. **Clone repositori ini:**
    ```bash
    git clone https://github.com/E1PBP/movezz.git
    ```
2. **Masuk ke direktori proyek:**
    ```bash
    cd movezz
    ```
3. **Buat dan aktifkan virtual environment (opsional tapi direkomendasikan):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    ```
4. **Install dependencies yang dibutuhkan:**
    ```bash
    pip install -r requirements.txt
    ```
5. **Atur environment variable dengan membuat file `.env` di root folder:**
    ```env
    DB_NAME=
    DB_HOST=
    DB_PORT=
    DB_USER=
    DB_PASSWORD=
    SCHEMA=
    PRODUCTION=False
    ```
6. **Jalankan migrasi database:**
    ```bash
    python manage.py migrate
    ```
7. **Jalankan server pengembangan Django:**
    ```bash
    python manage.py runserver
    ```

Akses aplikasi di `http://localhost:8000/`.

---
## Struktur Folder
```
.
├── .env / .env.example / .env.production   # File konfigurasi environment
├── .github/workflows/deploy.yml            # Workflow CI/CD GitHub Actions
├── .gitignore                              # Daftar file/folder yang diabaikan git
├── auth_module/                            # Modul autentikasi pengguna
├── broadcast_module/                       # Modul fitur broadcast
├── common/                                 # Utilitas dan manajemen data umum
├── db.sqlite3                              # Database SQLite (default)
├── feeds_module/                           # Modul fitur feeds
├── LICENSE                                 # Lisensi proyek
├── manage.py                               # Entrypoint manajemen Django
├── marketplace_module/                     # Modul fitur marketplace
├── message_module/                         # Modul fitur pesan/chat
├── movezz/                                 # Konfigurasi utama Django project
├── profile_module/                         # Modul profil pengguna
├── README.md                               # Dokumentasi proyek
├── requirements.txt                        # Daftar dependencies Python
├── static/                                 # File statis (CSS, JS, gambar)
└── templates/                              # Template HTML Django
```

**Keterangan:**
- Setiap folder modul (`*_module`) berisi fitur utama aplikasi.
- Folder `movezz/` berisi pengaturan dan routing utama Django.
- Folder `static/` dan `templates/` menyimpan aset frontend.
- File `.env` dan variannya untuk konfigurasi environment.
- File `manage.py` digunakan untuk menjalankan perintah Django.
- Folder `common/` berisi utilitas dan script manajemen data.
- File dan folder lain mendukung pengembangan, deployment, dan dokumentasi.


---
## Tech Stack

- **Backend:** [Django](https://www.djangoproject.com/) (Python)
- **Frontend:** [Tailwind CSS](https://tailwindcss.com/), [DaisyUI](https://daisyui.com/)
- **Real-time Communication:** [Python Channels](https://channels.readthedocs.io/en/stable/)
- **Database:** [PostgreSQL](https://www.postgresql.org/)
- **Deployment & CI/CD:** [GitHub Actions](https://github.com/features/actions)