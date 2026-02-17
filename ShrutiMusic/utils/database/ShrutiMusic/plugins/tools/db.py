import json
import os

DB_FILE = "abuse_db.json"

def _read_db():
    if not os.path.exists(DB_FILE):
        return {"enabled_chats": [], "whitelists": {}}
    with open(DB_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return {"enabled_chats": [], "whitelists": {}}

def _write_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

async def is_abuse_enabled(chat_id: int) -> bool:
    data = _read_db()
    return str(chat_id) in data.get("enabled_chats", [])

async def set_abuse_status(chat_id: int, status: bool):
    data = _read_db()
    chats = data.get("enabled_chats", [])
    if status and str(chat_id) not in chats:
        chats.append(str(chat_id))
    elif not status and str(chat_id) in chats:
        chats.remove(str(chat_id))
    data["enabled_chats"] = chats
    _write_db(data)

async def add_whitelist(chat_id: int, user_id: int):
    data = _read_db()
    whitelists = data.get("whitelists", {})
    chat_str = str(chat_id)
    if chat_str not in whitelists:
        whitelists[chat_str] = []
    if user_id not in whitelists[chat_str]:
        whitelists[chat_str].append(user_id)
    data["whitelists"] = whitelists
    _write_db(data)

async def remove_whitelist(chat_id: int, user_id: int):
    data = _read_db()
    whitelists = data.get("whitelists", {})
    chat_str = str(chat_id)
    if chat_str in whitelists and user_id in whitelists[chat_str]:
        whitelists[chat_str].remove(user_id)
    data["whitelists"] = whitelists
    _write_db(data)

async def get_whitelisted_users(chat_id: int):
    data = _read_db()
    return data.get("whitelists", {}).get(str(chat_id), [])

async def is_user_whitelisted(chat_id: int, user_id: int) -> bool:
    users = await get_whitelisted_users(chat_id)
    return user_id in users
  
