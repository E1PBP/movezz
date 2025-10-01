
# Contributing to Movezz 

## 📌 Cara Berkontribusi

1. **Clone repo ini**  
   Klik tombol `Clone` di kanan atas halaman repo ini.
 
   ```bash
    git clone https://github.com/E1PBP/movezz.git
   cd movezz
    ```

3. **Buat branch baru**
   Gunakan nama branch yang deskriptif:

   ```bash
   git checkout -b feature/your-name
   ```

   > Format branch:
   >
   > * `feature/<fitur>` → untuk fitur baru
   > * `fix/<bug>` → untuk perbaikan bug

4. **Setup environment (Django)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # di Linux/Mac
   venv\Scripts\activate     # di Windows
   pip install -r requirements.txt
   python manage.py migrate
   ```

5. **Jalankan project**

   ```bash
   python manage.py runserver
   ```

6. **Commit perubahan**
   Gunakan pesan commit yang jelas dan konsisten:

   ```bash
   git commit -m "feat: add user role model"
   ```

   > Prefix commit yang disarankan:
   >
   > * `feat:` → fitur baru
   > * `fix:` → perbaikan bug
   > * `docs:` → update dokumentasi
   > * `style:` → formatting (tidak mengubah logika)
   > * `refactor:` → refactor kode
   > * `test:` → menambah/memperbaiki testing

7. **Push ke GitHub & buat Pull Request (PR)**

   ```bash
   git push origin feature/add-user-role
   ```

   Lalu buka GitHub dan buat PR ke branch `master`.

---

## 🧪 Testing

Sebelum submit PR, jalankan test untuk memastikan tidak ada yang rusak:

```bash
python manage.py test
```

Tambahkan test baru jika kamu menambah fitur baru.

---

## ✨ Pedoman Kontribusi

* Jaga kualitas kode (ikuti [PEP8](https://peps.python.org/pep-0008/) untuk Python).
* Selalu update dokumentasi bila ada fitur/endpoint baru.
* Jangan commit **file sensitif** (misalnya `.env`, credential).
* Diskusikan dulu di *Issues* sebelum membuat perubahan besar.

---

## 📜 Lisensi

Dengan berkontribusi, kamu setuju bahwa kontribusi kamu akan dirilis di bawah lisensi **MIT** dari proyek ini.

---

