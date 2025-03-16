from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Используем переменные окружения для безопасности
BOT_TOKEN = os.getenv("BOT_TOKEN", "7549920153:AAHpX2lw00IZeiCkPoA6hlZCXWgLIq0pFNs")
CHAT_ID = os.getenv("CHAT_ID", "-1002371749711")

# Функция отправки сообщений в Telegram
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    response = requests.post(url, json=payload)
    return response.status_code

@app.route('/postback', methods=['POST'])
def postback():
    try:
        data = request.json  # Получаем JSON

        # Проверяем, что utm_content = honey
        utm_content = data.get("_utm_content", "").lower()
        if utm_content == "honey":
            campname = data.get("campname", "UnknownCampaign")
            webname = data.get("webname", "UnknownWeb")

            if "revenue" in data:
                revenue = data.get("revenue", "0")
                click = data.get("click", "N/A")
                message = f"💰 NEW DEPOSIT! 💰\n🏆 Campaign: {campname}\n🍯 UTM: {utm_content}\n🌐 Website: {webname}\n💸 Revenue: {revenue}\n🎯 Click ID: {click} 🚀🔥"
            else:
                message = f"🆕 NEW REGISTRATION! 🆕\n🏆 Campaign: {campname}\n🍯 UTM: {utm_content}\n🌐 Website: {webname}\n✅ Status: REG 🚀🎉"

            send_message(message)  # Отправляем сообщение в Telegram

        return jsonify({"status": "ok"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
