import asyncio
from quart import Quart, request, jsonify
from quart_cors import cors
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

# --- Настройки ---
API_ID = 26595249  # Укажи свой API ID
API_HASH = "9480dce5299fb30b4e520242dd6d87d8"  # Укажи свой API Hash
SESSION_NAME = "session"  # Файл сессии для сохранения входа

app = Quart(__name__)
app = cors(app, allow_origin="*")

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@app.post("/send_phone")
async def send_phone():
    try:
        data = await request.json
        phone_number = data.get("phone")

        if not phone_number:
            return jsonify({"success": False, "error": "Номер телефона обязателен"}), 400

        await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(phone_number)

        return jsonify({"success": True, "message": "Код отправлен"}), 200

    except Exception as e:
        print("Ошибка на сервере:", str(e))  # Лог ошибки в терминал
        return jsonify({"success": False, "error": str(e)}), 500

@app.post("/send_code")
async def send_code():
    try:
        data = await request.json
        phone_number = data.get("phone")
        code = data.get("code")

        if not phone_number or not code:
            return jsonify({"success": False, "error": "Номер и код обязательны"}), 400

        await client.connect()
        if not await client.is_user_authorized():
            await client.sign_in(phone_number, code)

        return jsonify({"success": True, "message": "Вход выполнен"}), 200

    except SessionPasswordNeededError:
        return jsonify({"success": False, "error": "Нужен пароль 2FA"}), 401
    except Exception as e:
        print("Ошибка на сервере:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    print("🚀 Сервер запущен на http://127.0.0.1:5701")
    asyncio.run(app.run(host="127.0.0.1", port=5701, debug=True))

