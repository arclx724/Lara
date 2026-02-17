import re
import html
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus, ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ShrutiMusic import app
from ShrutiMusic.utils.database import (
    is_abuse_enabled,
    set_abuse_status,
    add_whitelist,
    remove_whitelist,
    get_whitelisted_users,
    is_user_whitelisted
)

# --- Abusive Words List ---
ABUSIVE_WORDS = [
    "aand", "rascal", "aandu", "aad", "ass", "asshole", "b.c", "b.c.", "b.k.l", "b.s.d.k", 
    "babbe", "babbey", "bahenchod", "bahenchodd", "bakchod", "bakchodi", "bakchodd", 
    "bastard", "bc", "behench*d", "behenchod", "behenchodd", "behenka", "betichod", 
    "bevakoof", "bevda", "bevdey", "bevkoof", "bewakoof", "bewday", "bewkoof", "bewkuf", 
    "bhadua", "bhaduaa", "bhadva", "bhadvaa", "bhadwa", "bhadwaa", "bhadwe", "bhadwes", 
    "bhench0d", "bhenchod", "bhenchodd", "bhosada", "bhosda", "bhosdaa", "bhosadchod", 
    "bhosadchodal", "bhosdike", "bhosdiki", "bhosdiwala", "bhosdiwale", "bhonsdike", 
    "bitch", "bkl", "blowjob", "boobs", "boor", "bsdk", "bube", "bubey", "bullshit", 
    "bur", "burchodi", "burr", "buur", "buurr", "ch*tiya", "charsi", "chhakka", 
    "chhenal", "chhi", "chhin", "chhod", "chinaal", "chinal", "chipkali", "chod", 
    "chodd", "chodai", "chodna", "chodne", "choodai", "chooche", "choochi", "choot", 
    "chootia", "chudai", "chudakkad", "chudne", "chudney", "chudwa", "chudwaa", 
    "chudwaane", "chudwane", "chuchi", "chut", "chutad", "chute", "chuteya", "chutia", 
    "chutiya", "chutiyapa", "chutiye", "chuttad", "chutya", "cock", "cunt", "dalaal", 
    "dalal", "dalle", "dalley", "dalli", "dick", "dickhead", "doggy", "fattu", 
    "fuck", "fucker", "fucking", "g@ndu", "gaand", "gaandfat", "gaandmasti", 
    "gaandmar", "gaandmara", "gaandu", "gadha", "gadhe", "gadhalund", "gand", 
    "gandfat", "gandfut", "gandi", "gandiya", "gandiye", "gandu", "gandve", "gay", 
    "goo", "gote", "gotey", "gotte", "gu", "hag", "haggu", "hagne", "hagney", 
    "haraami", "haraamjaada", "haraamjaade", "haraamkhor", "haraamzaade", 
    "haraamzyaada", "harami", "haramjada", "haramkhor", "haramzyada", "hijra", 
    "jhaant", "jhaat", "jhaatu", "jhat", "jhatu", "kamin", "kamina", "kamine", 
    "kaminey", "kanjar", "kanjari", "kutta", "kutte", "kuttey", "kutti", "kuttia", 
    "kutiya", "kuttiya", "l*da", "l@da", "lauda", "laude", "laudey", "laura", 
    "lavda", "lavde", "lawda", "lesbian", "ling", "loda", "lode", "lodu", "lora", 
    "loru", "launda", "lounde", "loundey", "laundi", "laundiya", "lulli", "lund", 
    "lundchus", "m.c", "m.c.", "maar", "madarchod", "madarchodd", "madarchood", 
    "madarchoot", "madarchut", "madarxhod", "maderchod", "madherchod", "madherchood", 
    "Madharchod", "Madharchood", "mamme", "mammey", "maro", "marunga", "mc", "mf", 
    "mkc", "moot", "mootne", "mooth", "motherfucker", "mut", "mutne", "muth", 
    "mutthal", "nude", "nudes", "nalayak", "nikamma", "nipple", "nunni", "nunnu", 
    "paaji", "paji", "penis", "pesaab", "pesab", "peshaab", "peshab", "pilla", 
    "pillay", "pille", "pilley", "pisaab", "pisab", "pkmkb", "porn", "porno", 
    "pornography", "porns", "porkistan", "pussy", "raand", "rand", "randi", 
    "randibaaz", "randwa", "randy", "ramdi", "rape", "rapist", "saala", "saale", 
    "saali", "sex", "sexting", "sexy", "shit", "slut", "suar", "suwar", "tatte", 
    "tatti", "tatty", "terimaaki", "terimaki", "tmkb", "tmkc", "tits", "ullu", 
    "vagina", "whore", "xxx", "zandu"
]

ABUSE_PATTERN = re.compile(r'\b(' + '|'.join(map(re.escape, ABUSIVE_WORDS)) + r')\b', re.IGNORECASE)

# --- Helpers ---

async def has_change_info_rights(chat_id, user_id, app):
    """Check if user is Owner OR Admin with 'Change Group Info' rights."""
    try:
        member = await app.get_chat_member(chat_id, user_id)
        if member.status == ChatMemberStatus.OWNER:
            return True
        if member.status == ChatMemberStatus.ADMINISTRATOR:
            return getattr(member.privileges, "can_change_info", False)
        return False
    except:
        return False

async def get_target_user(client, message):
    """Extract user from reply, username, or ID."""
    if message.reply_to_message:
        return message.reply_to_message.from_user
    
    if len(message.command) > 1:
        target = message.text.split(None, 1)[1]
        try:
            user = await client.get_users(target)
            return user
        except:
            return None
    return None

# ================= COMMANDS =================

@app.on_message(filters.command("abuse") & filters.group)
async def toggle_abuse(client, message):
    if not await has_change_info_rights(message.chat.id, message.from_user.id, app):
        return await message.reply_text("❌ Only admins with **'Change Group Info'** rights can use this command.")

    if len(message.command) == 1:
        text = (
            "<b>🛡 Abuse Filter Commands:</b>\n\n"
            "• <code>/abuse on</code> or <code>enable</code> - Enable filter\n"
            "• <code>/abuse off</code> or <code>disable</code> - Disable filter\n"
            "• <code>/authabuse</code> - Whitelist a user (Reply/Username/ID)\n"
            "• <code>/unauthabuse</code> - Remove from whitelist\n"
            "• <code>/authlistabuse</code> - See whitelisted users"
        )
        return await message.reply_text(text, parse_mode=ParseMode.HTML)

    arg = message.command[1].lower()
    if arg in ["on", "enable", "yes"]:
        await set_abuse_status(message.chat.id, True)
        await message.reply_text("🛡 Abuse protection is now <b>Enabled ✅</b>", parse_mode=ParseMode.HTML)
    elif arg in ["off", "disable", "no"]:
        await set_abuse_status(message.chat.id, False)
        await message.reply_text("🛡 Abuse protection is now <b>Disabled ❌</b>", parse_mode=ParseMode.HTML)
    else:
        await message.reply_text("❌ Invalid command. Use <code>/abuse on</code> or <code>/abuse off</code>.", parse_mode=ParseMode.HTML)


@app.on_message(filters.command(["authabuse", "abuseauth"]) & filters.group)
async def auth_user(client, message):
    if not await has_change_info_rights(message.chat.id, message.from_user.id, app):
        return await message.reply_text("❌ Only admins with **'Change Group Info'** rights can use this command.")

    target = await get_target_user(client, message)
    if not target:
        return await message.reply_text("⚠️ Target not found! \nUse: <code>/authabuse @username</code> or <code>User ID</code> or <b>Reply</b> to a message.", parse_mode=ParseMode.HTML)

    await add_whitelist(message.chat.id, target.id)
    await message.reply_text(f"✅ {target.mention} has been whitelisted from the abuse filter.", parse_mode=ParseMode.HTML)


@app.on_message(filters.command(["unauthabuse", "unauth"]) & filters.group)
async def unauth_user(client, message):
    if not await has_change_info_rights(message.chat.id, message.from_user.id, app):
        return await message.reply_text("❌ Only admins with **'Change Group Info'** rights can use this command.")

    target = await get_target_user(client, message)
    if not target:
        return await message.reply_text("⚠️ Target not found! \nUse: <code>/unauthabuse @username</code> or <code>User ID</code> or <b>Reply</b> to a message.", parse_mode=ParseMode.HTML)

    await remove_whitelist(message.chat.id, target.id)
    await message.reply_text(f"🚫 {target.mention} has been removed from the whitelist.", parse_mode=ParseMode.HTML)


@app.on_message(filters.command("authlistabuse") & filters.group)
async def auth_list(client, message):
    if not await has_change_info_rights(message.chat.id, message.from_user.id, app):
        return await message.reply_text("❌ Only admins with **'Change Group Info'** rights can use this command.")

    users = await get_whitelisted_users(message.chat.id)
    if not users:
        return await message.reply_text("📂 Whitelist is empty.")
    
    text = "📋 <b>Whitelisted Users:</b>\n\n"
    for uid in users:
        try:
            u = await app.get_users(uid)
            text += f"• {u.mention}\n"
        except:
            text += f"• ID: <code>{uid}</code>\n"
    await message.reply_text(text, parse_mode=ParseMode.HTML)


# --- MAIN WATCHER ---
@app.on_message(filters.group & ~filters.bot, group=10)
async def abuse_watcher(client, message):
    text = message.text or message.caption
    if not text:
        return

    if not await is_abuse_enabled(message.chat.id):
        return

    if await is_user_whitelisted(message.chat.id, message.from_user.id):
        return

    if ABUSE_PATTERN.search(text):
        safe_text = html.escape(text)
        # Using correct <spoiler> tag for Pyrogram's HTML Parser
        censored_text = ABUSE_PATTERN.sub(lambda m: f"<spoiler>{m.group(0)}</spoiler>", safe_text)
        
        try:
            await message.delete()
            
            bot_username = (await app.get_me()).username
            buttons = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("➕ Add Me", url=f"https://t.me/{bot_username}?startgroup=true"),
                    InlineKeyboardButton("📢 Updates", url="https://t.me/robokaty")
                ]
            ])

            clean_name = html.escape(message.from_user.first_name)
            user_link = f"<a href='tg://user?id={message.from_user.id}'>{clean_name}</a>"

            warning_text = (
                f"🚫 Hey {user_link}, your message was removed.\n\n"
                f"🔍 <b>Censored:</b>\n{censored_text}\n\n"
                f"Please keep the chat respectful."
            )

            sent = await message.reply_text(
                warning_text,
                reply_markup=buttons,
                disable_web_page_preview=True,
                parse_mode=ParseMode.HTML
            )
            await asyncio.sleep(60)
            await sent.delete()
        except Exception as e:
            print(f"Error deleting abuse: {e}")
            
