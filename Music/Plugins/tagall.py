import asyncio

from pyrogram import filters

from pyrogram import Client
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import Chat, Message, User

from Music import app, OWNER
from Music.config import OWNER_ID
from Music.MusicUtilities.helpers.administrator import adminsOnly

spam_chats = []

def get_text(message: Message) -> [None, str]:
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None

@app.on_message(filters.command("all") & ~filters.edited & ~filters.bot)
async def tagall(client, message):
    permission = "can_manage_voice_chats"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    sh = get_text(message)
    if not sh:
        sh = "Hi!"
    string = ""
    limit = 1
    icm = client.iter_chat_members(message.chat.id)
    spam_chats.append(message.chat.id)
    async for member in icm:
        if not message.chat.id in spam_chats:
            break
        tag = member.user.mention + " "
        msg = f"**{sh}**\n\n{string}"
        if limit <= 5:
            string += f"{tag}"
            msg = f"**{sh}**\n\n{string}"
            limit += 1
        else:
            try:
                await client.send_message(message.chat.id, text=msg)
                limit = 1
                string = ""
                msg = f"**{sh}**\n\n{string}"
                await asyncio.sleep(2)
            except FloodWait as e:
                x = 2
                await asyncio.sleep(e.x)
            except TimeoutError:
                continue



@app.on_message(filters.command("cancel") & ~filters.edited & ~filters.bot)
async def tagall(client, message):
    permission = "can_manage_voice_chats"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    if not message.chat.id in spam_chats:
        return await message.reply("Tidak Ada Proses Tag...")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("Proses Tag Berhenti.")
