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

## Deskripsi Proyek

Movezz adalah aplikasi sosial media yang ditujukan untuk para pecinta olahraga, baik itu penggemar sepak bola, pelari, gym, maupun olahraga lainnya. Movezz menyediakan fitur utama seperti feeds beranda untuk berbagi dan melihat aktivitas, profil pengguna, chat dan messaging untuk berkomunikasi antar anggota, serta fitur broadcast untuk mengumumkan informasi penting kepada komunitas.

Movezz hadir sebagai solusi bagi para pecinta olahraga yang ingin terhubung, berbagi pengalaman, dan membangun komunitas secara digital. Aplikasi ini dirancang untuk mengakomodasi berbagai jenis olahraga, mulai dari sepak bola, lari, gym, hingga olahraga rekreasi lainnya. Dengan pendekatan sosial media, Movezz memudahkan pengguna untuk menemukan teman baru yang memiliki minat serupa, serta memperluas jaringan komunitas olahraga mereka.

Fitur feeds beranda memungkinkan pengguna untuk membagikan aktivitas olahraga, pencapaian, tips, atau sekadar update harian kepada komunitas. Setiap pengguna dapat memberikan komentar, menyukai, dan berinteraksi langsung pada postingan, sehingga tercipta suasana yang interaktif dan suportif. Selain itu, pengguna juga dapat mengikuti akun lain untuk mendapatkan update terbaru dari teman atau atlet favorit mereka.

Profil pengguna di Movezz menampilkan informasi pribadi, riwayat aktivitas, serta statistik olahraga yang telah dilakukan. Pengguna dapat menyesuaikan profil sesuai preferensi, menambahkan foto, bio, dan mengatur privasi akun. Fitur ini membantu pengguna untuk membangun identitas digital sebagai bagian dari komunitas olahraga yang aktif dan inspiratif. (tentatif)

Untuk mendukung komunikasi antar anggota, Movezz menyediakan fitur chat dan messaging yang memungkinkan percakapan pribadi. Fitur ini sangat berguna untuk mengatur jadwal latihan bersama, berdiskusi tentang teknik olahraga, atau sekadar berbincang santai. Selain itu, terdapat fitur broadcast yang seseorang untuk mengirimkan pengumuman penting secara massal kepada seluruh anggota.

Dengan berbagai fitur yang terintegrasi, Movezz bertujuan menjadi platform utama bagi para pecinta olahraga di Indonesia. Aplikasi ini tidak hanya memfasilitasi interaksi sosial, tetapi juga mendorong gaya hidup sehat, kolaborasi, dan semangat sportivitas di kalangan penggunanya. Melalui Movezz, diharapkan tercipta ekosistem olahraga digital yang inklusif, inspiratif, dan saling mendukung.

## Daftar Module

### 1. **Feeds (Timeline & Posting)**

**PIC** : Muhammad Hakim Nizami (2406399485)

Menjadi pusat aktivitas pengguna di mana mereka dapat membagikan momen olahraga, tips, atau highlight pertandingan. Fitur-fitur:

- Buat posting (teks, foto atau highlight pertandingan)
- Tag olahraga (mis. futsal, lari, basket), lokasi, dan mention pengguna
- Gunakan hashtag & kategori event (latihan, sparring, turnamen)
- Like, comment, dan share posting
- Feed utama berisi posting dari pengguna yang di-follow + rekomendasi olahraga populer
- Infinite scroll & lazy media loading
- Atur visibilitas posting (publik, followers, close friends) Simpan posting sebagai draft & jadwalkan publikasi **(opsional)**

### 2. **Profile (Aktivitas & Jaringan)**

**PIC** : Nadin Ananda (2406351806)

Profil yang menampilkan identitas olahraga dan aktivitas pengguna dalam komunitas Fitur-fitur:

- Halaman profil: bio, olahraga favorit, statistik latihan
- Postingan pengguna
- Sistem following/followers
- Status real-time “Sedang Berolahraga <jenis olahraga>” **(opsional)**
- Badges & level pencapaian
- Tabs marketplace & event broadcast pribadi

### 3. **Messaging (Pesan & Grup)**

**PIC** : Heraldo Arman (2406420702)

Fitur komunikasi antar pengguna, baik personal maupun grup komunitas olahraga. Fitur-fitur:

- Chat 1-on-1 & grup **(opsional)** (tim, komunitas, penyelenggara event)
- Kirim gambar **(opsional)**
- Bagikan posting feed langsung ke chat **(opsional)**
- Pesan permintaan untuk non-followers
- Status pesan (terkirim, dibaca), dan notifikasi real-time (via Django Channels)

### 4. **Marketplace (Perlengkapan & Barang Olahraga)**

**PIC** : Amberley Vidya Putri (2406495533)

Tempat jual-beli alat, perlengkapan, dan barang olahraga baru atau bekas antar pengguna.

Fitur-fitur:

- Buat listing barang: foto, kategori olahraga, kondisi, deskripsi, harga, lokasi
- Filter & sort berdasarkan olahraga, harga, kondisi, lokasi
- Wishlist, follow penjual, dan chat langsung dari listing
- Status barang: aktif, reserved, terjual
- Rating & ulasan transaksi

### 5. **Broadcast (Siaran & Event Publik)**

**PIC** : Roberto Eugenio Sugiarto (2406355640)

Modul untuk menyiarkan kegiatan olahraga publik, seperti fun run, sparring, atau turnamen kecil. Fitur-fitur:

- Buat event siaran: judul, olahraga, lokasi, waktu, kapasitas, level, biaya
- Pendaftaran peserta (join/leave, waitlist otomatis)
- Mode siaran:
  - Live ticker (skor/point real-time) **(opsional)**
- Halaman event publik: daftar peserta, scoreboard, bracket turnamen
- Atur visibilitas event (publik, link privat, komunitas tertentu)

### 6. **Authentication (Register and Login)**

**PIC** : All member

Modul untuk melakukan autentikasi seperti mendaftar akun dan login.

- Mendaftarkan akun baru ke aplikasi
- Login ke aplikasi

## Link sumber dataset

Note: Mungkin tidak semuanya digunakan

- https://www.kaggle.com/datasets/hasyimabdillah/workoutexercises-images
- https://www.kaggle.com/datasets/omarxadel/fitness-exercises-dataset
- https://universe.roboflow.com/search?q=class%3Aexercise
- https://www.kaggle.com/datasets/rishikeshkonapure/sports-image-dataset
- https://www.kaggle.com/datasets/gpiosenka/sports-classification
- https://www.kaggle.com/datasets/sarthakkapaliya/instagram-caption-data
- https://huggingface.co/datasets/kkcosmos/instagram-images-with-captions
- https://huggingface.co/datasets/Waterfront/social-media-captions

## Jenis pengguna website

Feeds -
User [.....]
Admin [...]

Profile -
User [.....]
Admin [...]

Messaging -
User [.....]
Admin [...]

Marketplace -
User [.....]
Admin [...]

Broadcast -
User [.....]
Admin [...]

Auth -
User [.....]
Admin [...]

## Link PWS

https://muhamad-hakim41-movezz.pbp.cs.ui.ac.id/

## Link Design Figma

https://www.figma.com/design/x4q0GDfJB0dQ2ZXl8uuXDZ/Design-Movezz?node-id=0-1&t=62HMu5tm1V2KTkKk-1

## Link DB Diagram (May Change In The Future)

https://dbdiagram.io/d/Movezz-68db9fa4d2b621e4228f0778
https://dbdiagram.io/d/movezz-2-68e696cad2b621e422e8abc6

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
- **Storage** (image): [Supabase](https://supabase.com/)