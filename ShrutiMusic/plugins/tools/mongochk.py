import re
from pymongo import MongoClient
from pyrogram import filters
from pyrogram.types import Message
from ShrutiMusic import app
from ShrutiMusic.misc import SUDOERS # SECURITY PATCH: Import SUDOERS

mongo_url_pattern = re.compile(r"mongodb(?:\+srv)?:\/\/[^\s]+")

@app.on_message(filters.command("mongochk") & SUDOERS) # SECURITY PATCH: Restricted to Sudoers
async def mongo_command(client, message: Message):
    if len(message.command) < 2:
        await message.reply(
            "ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ʏᴏᴜʀ ᴍᴏɴɢᴏᴅʙ ᴜʀʟ ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ  /mongochk your_mongodb_url"
        )
        return

    mongo_url = message.command[1]
    if re.match(mongo_url_pattern, mongo_url):
        msg = await message.reply("⏳ ᴄʜᴇᴄᴋɪɴɢ ᴍᴏɴɢᴏᴅʙ ᴄᴏɴɴᴇᴄᴛɪᴏɴ...")
        try:
            # Attempt to connect to the MongoDB instance
            m_client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
            m_client.server_info()  # Will cause an exception if connection fails
            await msg.edit_text("ᴍᴏɴɢᴏᴅʙ ᴜʀʟ ɪs ᴠᴀʟɪᴅ ᴀɴᴅ ᴄᴏɴɴᴇᴄᴛɪᴏɴ sᴜᴄᴇssғᴜʟ ✅")
        except Exception as e:
            await msg.edit_text(f"❌ ғᴀɪʟᴇᴅ ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ᴍᴏɴɢᴏᴅʙ: {e}")
    else:
        await message.reply("❌ ᴜᴘs! ʏᴏᴜʀ ᴍᴏɴɢᴏᴅʙ ғᴏʀᴍᴀᴛ ɪs ɪɴᴠᴀʟɪᴅ")

__MODULE__ = "Mᴏɴɢᴏᴅʙ"
__HELP__ = """
**ᴍᴏɴɢᴏᴅʙ ᴄʜᴇᴄᴋᴇʀ:**

• `/mongochk [mongo_url]`: Cʜᴇᴄᴋs ᴛʜᴇ ᴠᴀʟɪᴅɪᴛʏ ᴏғ ᴀ ᴍᴏɴɢᴏᴅʙ URL ᴀɴᴅ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴛᴏ ᴛʜᴇ ᴍᴏɴɢᴏᴅʙ ɪɴsᴛᴀɴᴄᴇ.
"""
