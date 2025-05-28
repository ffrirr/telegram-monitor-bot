import subprocess
import requests
import threading
import time
import re

# Konfigurasi Telegram & Docker
BOT_TOKEN = '<bot-token>'
CHAT_ID = '<chat-id>'
ODOO_SERVICE_NAME = 'web'  # sesuaikan nama service Odoo kamu
DOCKER_COMPOSE_DIR = '/home/feri/Testing/odoo18'  # sesuaikan direktori docker-compose.yml

def send_telegram_message(text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': text}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

def monitor_log():
    cmd = ['docker', 'compose', 'logs', '-f', ODOO_SERVICE_NAME]
    process = subprocess.Popen(
        cmd,
        cwd=DOCKER_COMPOSE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True,
    )

    timestamp_pattern = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}")
    log_block = []
    capture = False
    emoji = "⚠️"

    for line in process.stdout:
        if " | " in line:
            _, content = line.split(" | ", 1)
        else:
            content = line

        content = content.strip()

        if "error" in content.lower():
            emoji = "🚨"
            capture = True
            log_block = [content + "\n"]
        elif "warning" in content.lower():
            emoji = "⚠️"
            capture = True
            log_block = [content + "\n"]
        elif capture:
            if timestamp_pattern.match(content):
                message = "".join(log_block).strip()
                send_telegram_message(f"{emoji} Odoo Log Error:\n{message}")

                # Mulai blok baru jika baris berikutnya juga error/warning
                capture = False
                log_block = []
                if "error" in content.lower():
                    emoji = "🚨"
                    capture = True
                    log_block = [content + "\n"]
                elif "warning" in content.lower():
                    emoji = "⚠️"
                    capture = True
                    log_block = [content + "\n"]
            else:
                log_block.append(content + "\n")

    if capture and log_block:
        message = "".join(log_block).strip()
        send_telegram_message(f"{emoji} Odoo Log Error:\n{message}")

def check_last_hour_logs():
    cmd = ['docker', 'compose', 'logs', '--since', '1h', ODOO_SERVICE_NAME]
    try:
        result = subprocess.run(cmd, cwd=DOCKER_COMPOSE_DIR, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        lines = result.stdout.splitlines()

        timestamp_pattern = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}")
        log_block = []
        capture = False
        emoji = "⚠️"

        for line in lines:
            if " | " in line:
                _, content = line.split(" | ", 1)
            else:
                content = line

            content = content.strip()

            if "error" in content.lower():
                emoji = "🚨"
                capture = True
                log_block = [content + "\n"]
            elif "warning" in content.lower():
                emoji = "⚠️"
                capture = True
                log_block = [content + "\n"]
            elif capture:
                if timestamp_pattern.match(content):
                    message = "".join(log_block).strip()
                    send_telegram_message(f"{emoji} Odoo Log Error (last 1h):\n{message}")
                    capture = False
                    log_block = []
                    if "error" in content.lower():
                        emoji = "🚨"
                        capture = True
                        log_block = [content + "\n"]
                    elif "warning" in content.lower():
                        emoji = "⚠️"
                        capture = True
                        log_block = [content + "\n"]
                else:
                    log_block.append(content + "\n")

        if capture and log_block:
            message = "".join(log_block).strip()
            send_telegram_message(f"{emoji} Odoo Log Error (last 1h):\n{message}")

    except Exception as e:
        send_telegram_message(f"❌ Gagal ambil log sejam terakhir: {e}")

def telegram_command_listener():
    last_update_id = None
    while True:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        if last_update_id:
            url += f"?offset={last_update_id + 1}"
        try:
            res = requests.get(url).json()
            for update in res.get("result", []):
                last_update_id = update["update_id"]
                message = update.get("message", {}).get("text", "")
                chat = update.get("message", {}).get("chat", {})
                if str(chat.get("id")) == CHAT_ID:
                    if message.strip() == "/restart":
                        send_telegram_message("🔁 Restarting Odoo...")
                        subprocess.run(['docker', 'compose', 'restart', ODOO_SERVICE_NAME], cwd=DOCKER_COMPOSE_DIR)
                        send_telegram_message("✅ Odoo restarted.")
                    elif message.strip() == "/log":
                        send_telegram_message("🕵️‍♂️ Mengambil log error/warning 1 jam terakhir...")
                        check_last_hour_logs()
        except Exception as e:
            print(f"Telegram listener error: {e}")
        time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=monitor_log, daemon=True).start()
    telegram_command_listener()
