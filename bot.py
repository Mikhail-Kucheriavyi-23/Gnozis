import os
import logging
import requests
from flask import Flask, request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
ALLOWED_USER_ID = os.environ.get("ALLOWED_USER_ID")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Gnozis AI Engineering Agent is running!", 200

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    json_data = request.get_json()
    if not json_data:
        return "OK", 200

    logger.info(f"Received update: {json_data}")

    message = json_data.get("message") or json_data.get("edited_message")
    if not message:
        return "OK", 200

    chat_id = message["chat"]["id"]
    user_id = str(message["from"]["id"])
    text = message.get("text")

    if ALLOWED_USER_ID and user_id != str(ALLOWED_USER_ID):
        return "OK", 200

    if not text:
        return "OK", 200

    send_telegram_message(chat_id, "🔄 Запрос принят. Обрабатываю через OpenRouter...")
    ai_response = query_openrouter(text)
    send_telegram_message(chat_id, ai_response)

    return "OK", 200

def query_openrouter(prompt: str) -> str:
    if not OPENROUTER_API_KEY:
        return "❌ Ошибка: не задан OPENROUTER_API_KEY."
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://github.com/Mikhail-Kucheriavyi-23/Gnozis",
        "X-Title": "Gnozis AI Bot"
    }
    payload = {
        "model": "anthropic/claude-3.5-sonnet",
        "messages": [
            {"role": "system", "content": "You are Gnozis, an advanced AI engineering agent."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"❌ Ошибка OpenRouter: {response.status_code}"
    except Exception as e:
        return f"❌ Ошибка соединения: {str(e)}"

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}, timeout=10)
    except Exception as e:
        logger.error(f"Failed: {e}")

def main():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()