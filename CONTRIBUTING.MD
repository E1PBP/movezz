# Contributing to Movezz

## 📌 Cara Berkontribusi

1. **Clone repo ini**  
   Klik tombol `Clone` di kanan atas halaman repo ini.

   ```bash
   git clone https://github.com/E1PBP/movezz.git
   cd movezz
   ```

2. **Buat branch baru**
   Gunakan nama branch yang deskriptif:

   ```bash
   git checkout -b feature/<fitur>
   ```

   > Format branch:
   >
   > - `feature/<fitur>` → untuk fitur baru
   > - `fix/<bug>` → untuk perbaikan bug

3. **Setup environment (Django)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # di Linux/Mac
   venv\Scripts\activate     # di Windows
   pip install -r requirements.txt
   python manage.py migrate
   ```

4. **Jalankan project**

   ```bash
   python manage.py runserver
   ```

5. **Commit perubahan**
   Gunakan pesan commit yang jelas dan konsisten:

   ```bash
   git commit -m "feat: add user role model"
   ```

   > Prefix commit yang disarankan:
   >
   > - `feat:` → fitur baru
   > - `fix:` → perbaikan bug
   > - `docs:` → update dokumentasi
   > - `style:` → formatting (tidak mengubah logika)
   > - `refactor:` → refactor kode
   > - `test:` → menambah/memperbaiki testing

6. **Push ke GitHub & buat Pull Request (PR)**

   ```bash
   git push origin feature/add-user-role
   ```

   Lalu buka GitHub dan buat PR ke branch `master`.

---

## 🧪 Testing

Sebelum submit PR, jalankan test untuk memastikan tidak ada yang rusak:

```bash
coverage run manage.py test
coverage report
```

Tambahkan test baru jika kamu menambah fitur baru.

---

## ✨ Pedoman Kontribusi

- Jaga kualitas kode (ikuti [PEP8](https://peps.python.org/pep-0008/) untuk Python).
- Selalu update dokumentasi bila ada fitur/endpoint baru.
- Jangan commit **file sensitif** (misalnya `.env`, credential).
- Diskusikan dulu di _Issues_ sebelum membuat perubahan besar.

---

## Beberapa Sumber yang Membantu

- Lucide icon untuk penggunaan icon [https://lucide.dev/guide/packages/lucide](https://lucide.dev/guide/packages/lucide)
- Tailwind CSS untuk styling [https://tailwindcss.com/docs/styling-with-utility-classes](https://tailwindcss.com/docs/styling-with-utility-classes)
- Daisy UI untuk styling [https://daisyui.com/](https://daisyui.com/)
- Media management di Django (intinya manajemen gambar) [https://docs.djangoproject.com/en/5.2/topics/files/](https://docs.djangoproject.com/en/5.2/topics/files/)

---

## Panduan GitHub Copilot Untuk Para Vibecoder

Proyek ini menggunakan **custom Copilot instruction** yang berada di:

```
.github/copilot-instructions.md
```

File ini berfungsi sebagai **panduan AI** agar GitHub Copilot memberikan saran kode yang **konsisten** dengan gaya dan arsitektur proyek Movezz.

Instruksi tersebut mencakup:

- Gaya penulisan dan arsitektur Django
- Konvensi styling dengan **TailwindCSS v4** dan **DaisyUI v5**
- Praktik terbaik dalam testing, dokumentasi, dan struktur modul
- Cara berinteraksi dengan Copilot Chat agar hasilnya lebih relevan

---

### ⚙️ Cara Kerja Custom Instructions

| Mode Copilot                       | Apakah Menggunakan `.github/copilot-instructions.md`? | Keterangan                                               |
| ---------------------------------- | ----------------------------------------------------- | -------------------------------------------------------- |
| **Copilot Chat (sidebar)**         | ✅ Ya                                                 | Seluruh konteks dari file instruksi digunakan            |
| **Inline Chat (Ctrl + I)**         | ✅ Ya                                                 | Menggunakan mesin Chat Copilot dengan konteks proyek     |
| **Inline Suggestion (ghost text)** | ❌ Tidak                                              | Menggunakan model dasar Copilot tanpa instruksi tambahan |

---

### 💡 Tips Penggunaan untuk Kontributor

1. **Pastikan file ini ada di folder `.github/` di root project.**
   Contoh:

   ```
   movezz/
   ├── .github/
   │   └── copilot-instructions.md
   ├── feeds_module/
   ├── manage.py
   └── ...
   ```

2. **Buka file `.github/copilot-instructions.md` di tab VS Code** saat bekerja.
   Copilot akan lebih mudah menangkap konteks proyek jika file instruksi terbuka.

3. **Gunakan `Ctrl + I` (Inline Chat)** untuk memanggil Copilot di dalam editor, lalu beri prompt yang jelas.
   Contoh:

   ```python
   # Buat model Django untuk postingan olahraga dengan relasi ke pengguna
   ```

4. **Reload VS Code atau restart Copilot Chat** setelah kamu menambah atau mengubah file instruksi.

5. **Cek apakah instruksi aktif** dengan mengetik di Copilot Chat:

   ```
   what instructions are active?
   ```

---

### 📘 Dokumentasi Resmi

Untuk penjelasan lebih lengkap tentang _Custom Instructions_ di VS Code, kunjungi dokumentasi resmi:
👉 [https://code.visualstudio.com/docs/copilot/customization/custom-instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)


---

## 📜 Lisensi

Dengan berkontribusi, kamu setuju bahwa kontribusi kamu akan dirilis di bawah lisensi **MIT** dari proyek ini.

---
