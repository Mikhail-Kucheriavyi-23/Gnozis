import os
import subprocess
import requests
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8965809828:AAH3M55TU9y-fKuzang10cD6dyM7OtKhfTM")
ALLOWED_USER_ID = int(os.getenv("ALLOWED_USER_ID", "753475334"))
PATH_TO_REPO = "."

# В облаке OmniRoute должен указывать на внешний API (или ваш облачный роутер)
OMNIROUTE_URL = os.getenv("OMNIROUTE_URL", "https://api.openai.com/v1/chat/completions")
OMNIROUTE_KEY = os.getenv("OMNIROUTE_KEY", "ваш-облачный-ключ")

app_flask = Flask(__name__)
telegram_app = None

def read_project_state():
    state_path = os.path.join(PATH_TO_REPO, "STATE.md")
    if os.path.exists(state_path):
        with open(state_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Статус не описан."

async def handle_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return

    user_prompt = update.message.text
    await update.message.reply_text("🔄 Запрос принят. Обрабатываю...")

    current_state = read_project_state()

    system_instruction = f"""
Ты — главный ИИ-инженер проекта «Гнозис». 
ТЕКУЩИЙ СТАТУС ПРОЕКТА:
----------------
{current_state}
----------------
Инструкции:
1. Выполни задачу пользователя.
2. Если концепция меняется, укажи новый статус в тегах [STATE_UPDATE]Текст статуса[/STATE_UPDATE].
3. Пиши чистый код.
"""

    payload = {
        "model": "gpt-4o-mini", # Укажите актуальную модель
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt}
        ]
    }
    headers = {
        "Authorization": f"Bearer {OMNIROUTE_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(OMNIROUTE_URL, json=payload, headers=headers, timeout=60)
        res_data = response.json()
        ai_response = res_data["choices"][0]["message"]["content"]

        if "[STATE_UPDATE]" in ai_response and "[/STATE_UPDATE]" in ai_response:
            start = ai_response.find("[STATE_UPDATE]") + len("[STATE_UPDATE]")
            end = ai_response.find("[/STATE_UPDATE]")
            new_state_content = ai_response[start:end].strip()
            
            with open("STATE.md", "w", encoding="utf-8") as f:
                f.write(new_state_content)
                
            ai_response = ai_response.replace(ai_response[ai_response.find("[STATE_UPDATE]"):ai_response.find("[/STATE_UPDATE]")+len("[/STATE_UPDATE]")], "").strip()

        with open("latest_patch.md", "w", encoding="utf-8") as f:
            f.write(ai_response)

        await update.message.reply_text("✅ Готово! Ответ сгенерирован.")

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

@app_flask.route("/", methods=["GET"])
def index():
    return "Gnozis Bot is running!", 200

@app_flask.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)
    return "OK", 200

async def main():
    global telegram_app
    telegram_app = Application.builder().token(TELEGRAM_TOKEN).build()
    telegram_app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_prompt))
    
    await telegram_app.initialize()
    
    # Автоматическая установка вебхука при старте Render
    render_url = os.getenv("RENDER_EXTERNAL_URL")
    if render_url:
        webhook_url = f"{render_url}/{TELEGRAM_TOKEN}"
        await telegram_app.bot.set_webhook(url=webhook_url)
        print(f"Webhook установлен: {webhook_url}")

    await telegram_app.start()

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)