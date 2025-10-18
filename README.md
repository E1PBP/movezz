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
- Status pesan (terkirim, dibaca), dan notifikasi real-time (dengan polling)

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

## Link DB Diagram 

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

## Struktur Folder Proyek Django

```
.
├── .env / .env.example / .env.production    # Konfigurasi environment (lokal, example, dan production)
├── .github/
│   └── workflows/
│       └── deploy.yml                       # Workflow GitHub Actions untuk CI/CD (deployment otomatis)
├── .gitignore                               # Daftar file/folder yang diabaikan oleh Git
│
├── auth_module/                             # Modul autentikasi dan manajemen user
│   ├── models.py                            # Model user (jika extend dari default User)
│   ├── forms.py                             # Form login/registrasi
│   ├── views.py / urls.py                   # Endpoint login, logout, register
│   └── admin.py                             # Integrasi dengan Django Admin
│
├── broadcast_module/                        # Modul untuk fitur broadcast/event
│   ├── models.py                            # Model event dan gambar event
│   ├── migrations/                          # Skema database dan revisi
│   └── views.py / urls.py                   # Logika tampilan (CRUD event, dsb.)
│
├── common/                                  # Modul utilitas global dan shared components
│   ├── choices.py                           # Enum/choices global untuk model
│   ├── cloudinary_signals.py                # Integrasi sinyal Cloudinary untuk file upload
│   ├── utils/
│   │   ├── seed_helpers.py                  # Helper untuk seed data
│   │   └── validator_image.py               # Validator ukuran/gambar Cloudinary
│   ├── management/
│   │   └── command/seed_data.py             # Custom command untuk populate data awal
│   └── models.py                            # Model umum yang digunakan lintas modul
│
├── feeds_module/                            # Modul untuk fitur postingan/feeds pengguna
│   ├── models.py                            # Model postingan dan gambar
│   ├── templates/main.html                  # Template tampilan feed utama
│   └── views.py / urls.py                   # Endpoint feed (list, create, dsb.)
│
├── marketplace_module/                      # Modul marketplace (jual/beli listing)
│   ├── models.py                            # Model listing dan gambar
│   ├── forms.py                             # Form untuk tambah/edit listing
│   └── views.py / urls.py                   # Endpoint marketplace
│
├── message_module/                          # Modul pesan/chat antar pengguna
│   ├── models.py                            # Model percakapan dan pesan
│   ├── consumers.py                         # WebSocket consumer untuk real-time chat
│   └── views.py / urls.py                   # Endpoint API/chat room
│
├── profile_module/                          # Modul profil pengguna
│   ├── models.py                            # Model profil dan avatar (Cloudinary)
│   └── views.py / urls.py                   # Tampilan profil, edit profil, dsb.
│
├── movezz/                                  # Folder utama proyek Django
│   ├── settings.py                          # Konfigurasi utama Django (DB, Apps, Static, dsb.)
│   ├── urls.py                              # Routing global untuk seluruh modul
│   ├── asgi.py / wsgi.py                    # Entrypoint server (ASGI/WGSI)
│   └── __init__.py                          # Menandakan package Python
│
├── static/                                  # File statis yang dikembangkan (belum dikompilasi)
│   ├── css/global.css                       # Gaya global aplikasi
│   ├── js/index.js                          # Script interaktif global
│   └── images/logo.svg / logo-text.svg      # Aset logo dan ikon
│
├── staticfiles/                             # Hasil collectstatic (dikompilasi untuk deployment)
│   ├── admin/                               # File bawaan Django admin
│   ├── cloudinary/                          # Aset Cloudinary JS/HTML
│   └── ...                                  # CSS, JS, dan images hasil build
│
├── templates/                               # Template HTML global
│   ├── base.html                            # Template dasar (extends untuk semua halaman)
│   ├── navbar.html / footer.html            # Komponen layout umum
│   ├── 404.html / 500.html                  # Template error handler
│
├── CONTRIBUTING.MD                          # Panduan kontribusi untuk developer lain
├── LICENSE                                  # Informasi lisensi proyek
├── manage.py                                # Entrypoint manajemen Django
├── requirements.txt                         # Daftar dependensi Python (pip install -r)
├── README.md                                # Dokumentasi utama proyek
```

---

### Penjelasan Tambahan

#### Environment Configuration

* **`.env`** → konfigurasi lokal.
* **`.env.example`** → template contoh `.env` untuk developer lain.
* **`.env.production`** → environment khusus deployment.

#### Modularisasi Django

Struktur proyek ini menggunakan **pendekatan modular per fitur**, di mana setiap fitur (auth, message, feeds, marketplace, broadcast, profile) berdiri sebagai **app Django terpisah**, memiliki:

* `models.py` → struktur data
* `views.py` → logika tampilan atau API
* `urls.py` → routing internal
* `forms.py` → validasi input/form pengguna
* `admin.py` → integrasi dengan panel admin

#### Folder `common/`

Berfungsi sebagai **shared module** untuk kode yang digunakan lintas fitur:

* Validator, signal, dan helper.
* Command management untuk seed data awal (`python manage.py seed_data`).

#### Folder `static/` dan `templates/`

* **`static/`** menyimpan aset lokal selama pengembangan.
* **`staticfiles/`** berisi hasil `collectstatic`, digunakan pada server produksi.
* **`templates/`** berisi file HTML utama dan komponen layout seperti navbar/footer.

#### Deployment

Workflow CI/CD terdapat di:

```
.github/workflows/deploy.yml
```

yang mengatur proses otomatis build, collectstatic, dan deploy ke [pws](https://pbp.cs.ui.ac.id/web).

---

## Tech Stack

- **Backend:** [Django](https://www.djangoproject.com/) (Python)
- **Frontend:** [Tailwind CSS](https://tailwindcss.com/), [DaisyUI](https://daisyui.com/)
- **Database:** [PostgreSQL](https://www.postgresql.org/)
- **Deployment & CI/CD:** [GitHub Actions](https://github.com/features/actions)
- **Storage** (image): [Cloudinary](https://cloudinary.com)
