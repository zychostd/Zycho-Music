from Music import app
from Music.MusicUtilities.database.chats import add_served_chat

chat_watcher_group = 10

@app.on_message(group=chat_watcher_group)
async def chat_watcher_func(_, message):
    chat_id = message.chat.id
    if not chat_id:
        return
    await add_served_chat(chat_id)