# Copyright (c) 2025 Nand Yaduwanshi <NoxxOP>
# Location: Supaul, Bihar
#
# All rights reserved.
#
# This code is the intellectual property of Nand Yaduwanshi.
# You are not allowed to copy, modify, redistribute, or use this
# code for commercial or personal projects without explicit permission.
#
# Allowed:
# - Forking for personal learning
# - Submitting improvements via pull requests
#
# Not Allowed:
# - Claiming this code as your own
# - Re-uploading without credit or permission
# - Selling or using commercially
#
# Contact for permissions:
# Email: badboy809075@gmail.com


from .assistantdatabase import *
from .memorydatabase import *
from .mongodatabase import *
from .database import *

# --- ANTI-ABUSE DATABASE FUNCTIONS ---
from typing import List

abusedb = mongodb.abuse_db
whitelistdb = mongodb.whitelist_db

async def is_abuse_enabled(chat_id: int) -> bool:
    chat = await abusedb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return chat.get("status", False)

async def set_abuse_status(chat_id: int, status: bool):
    if status:
        await abusedb.update_one({"chat_id": chat_id}, {"$set": {"status": True}}, upsert=True)
    else:
        await abusedb.delete_one({"chat_id": chat_id})

async def add_whitelist(chat_id: int, user_id: int):
    await whitelistdb.update_one(
        {"chat_id": chat_id}, 
        {"$addToSet": {"whitelisted_users": user_id}}, 
        upsert=True
    )

async def remove_whitelist(chat_id: int, user_id: int):
    await whitelistdb.update_one(
        {"chat_id": chat_id}, 
        {"$pull": {"whitelisted_users": user_id}}
    )

async def get_whitelisted_users(chat_id: int) -> List[int]:
    chat = await whitelistdb.find_one({"chat_id": chat_id})
    if not chat:
        return []
    return chat.get("whitelisted_users", [])

async def is_user_whitelisted(chat_id: int, user_id: int) -> bool:
    users = await get_whitelisted_users(chat_id)
    return user_id in users
  
# ©️ Copyright Reserved - @NoxxOP  Nand Yaduwanshi

# ===========================================
# ©️ 2025 Nand Yaduwanshi (aka @NoxxOP)
# 🔗 GitHub : https://github.com/NoxxOP/ShrutiMusic
# 📢 Telegram Channel : https://t.me/ShrutiBots
# ===========================================


# ❤️ Love From ShrutiBots 
