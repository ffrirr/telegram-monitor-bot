## 📦 Odoo Docker Log Monitor with Telegram Bot

Skrip Python untuk memantau log **Odoo** (berjalan di Docker Compose) secara **realtime**, mendeteksi pesan **error** dan **warning**, serta mengirimkannya ke **Telegram Bot**. Juga mendukung perintah dari Telegram untuk:

* 🔁 Me-restart service Odoo
* 🕵️ Mengambil log error/warning dari 1 jam terakhir

---

### 🚀 Fitur

* 🧠 Monitor log `docker compose logs -f` (live)
* 🚨 Kirim notifikasi otomatis ke Telegram saat ada error/warning
* ⏳ Perintah `/log` dari Telegram untuk mengambil log error 1 jam terakhir
* 🔄 Perintah `/restart` dari Telegram untuk restart service Odoo

---

### 🛠️ Instalasi

1. **Clone repo ini**

```bash
git clone https://github.com/ffrirr/telegram-monitor-bot.git
cd <docker folder>
```

2. **Edit konfigurasi**

Edit bagian berikut pada `main.py`:

```python
BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
CHAT_ID = 'YOUR_TELEGRAM_CHAT_ID'
ODOO_SERVICE_NAME = 'web'  # sesuaikan dengan nama service Odoo kamu di docker-compose
DOCKER_COMPOSE_DIR = '/path/to/your/docker-compose-folder'
```

Untuk mendapatkan `CHAT_ID`, kirim pesan ke bot, lalu akses:
`https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`

---

### ▶️ Menjalankan

```bash
python3 <file_name>.py
```

> Gunakan `tmux`, `screen`, atau jadikan script ini sebagai service jika ingin tetap berjalan di background.

---

### 🧪 Perintah Telegram

| Perintah   | Fungsi                                 |
| ---------- | -------------------------------------- |
| `/log`     | Ambil log error/warning 1 jam terakhir |
| `/restart` | Restart Odoo Docker service            |

---

### 💡 Tips

* Pastikan bot hanya digunakan oleh Anda (validasi `CHAT_ID`)
* Jika digunakan di server production, sebaiknya gunakan `.env` untuk menyimpan token rahasia
* Anda bisa memodifikasi `log pattern` atau menambahkan level lain seperti `info`, `critical`, dll

---

### 📄 Lisensi

MIT License © \[Your Name]

---

Jika kamu ingin saya sekalian buatkan file `requirements.txt` atau struktur folder repo-nya, tinggal beri tahu.
