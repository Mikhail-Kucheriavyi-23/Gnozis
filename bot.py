import os
import asyncio
import logging
from flask import Flask, request

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Чтение переменных окружения
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
ALLOWED_USER_ID = os.environ.get("ALLOWED_USER_ID")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Gnozis AI Engineering Agent is running!", 200

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    # Обработка входящих вебхуков от Telegram
    json_data = request.get_json()
    if json_data:
        logger.info(f"Received update: {json_data}")
    return "OK", 200

def main():
    logger.info("Starting Gnozis bot service...")
    
    # Безопасная инициализация цикла событий для Python 3.14+
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    # Запуск Flask-сервера на порту, который требует Render (по умолчанию 10000)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()