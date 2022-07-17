from config import Config
from database import Database
import asyncio
import re

cfg = Config()
db = Database()

@cfg.parser.on_message()
async def pre_handler(client, message):
    await asyncio.sleep(cfg.delay)
    handle = True
    try:
        response = await cfg.parser.get_messages(message.sender_chat['id'], message.message_id)
        if response.empty:
            handle = False
    except:
        pass
    if handle:
        await main_handler(message)

async def main_handler(message):
    if not message.sender_chat == None:
        for chat_message in await db.get_node_id(message.sender_chat['id']):
            if not message.text == None:
                message_text = message.text
                for word in await db.get_ignore(chat_message[0]):
                    if word[0] in message_text:
                        if word[1]:
                            return
                        elif word[2] == None:
                            if word[0] == "@":
                                message_text = re.sub(r"@[^,\s]+,?", "", message.text)
                            elif 'http://' == word[0] or 'https://' == word[0]:
                                message_text = re.sub(r"https?://[^,\s]+,?", "", message.text)
                            else:
                                message_text = message.text.replace(word[0], '')
                        else:
                            if word[0] == "@":
                                message_text = re.sub(r"@[^,\s]+,?", word[2], message.text)
                            elif 'http://' == word[0] or 'https://' == word[0]:
                                message_text = re.sub(r"https?://[^,\s]+,?", word[2], message.text)
                            else:
                                message_text = message.text.replace(word[0], word[2])
                for recipient in await db.get_recipients(chat_message[0]):
                    if not message.reply_to_message == None:
                        reply_id = await db.get_reply_id(
                            from_id=message.sender_chat['id'], 
                            to_id=recipient[0], 
                            from_word_id=message.reply_to_message.message_id)
                        print(type(recipient[0]))
                        new_message = await cfg.parser.send_message(int(recipient[0]), message_text, reply_to_message_id=reply_id)
                    else:
                        new_message = await cfg.parser.send_message(int(recipient[0]), message_text)
                    await db.add_history(
                        from_id = message.sender_chat['id'],
                        to_id = recipient[0],
                        from_word_id = message.message_id,
                        to_word_id = new_message.message_id,
                    )
            elif message.media == 'photo':
                caption_text = message.caption
                for word in await db.get_ignore(chat_message[0]):
                    if word[0] in caption_text:
                        if word[1]:
                            return
                        elif word[2] == None:
                            if word[0] == "@":
                                caption_text = re.sub(r"@[^,\s]+,?", "", message.caption)
                            elif 'http://' == word[0] or 'https://' == word[0]:
                                caption_text = re.sub(r"https?://[^,\s]+,?", "", message.caption)
                            else:
                                caption_text = message.caption.replace(word[0], '')
                        else:
                            if word[0] == "@":
                                caption_text = re.sub(r"@[^,\s]+,?", word[2], message.caption)
                            elif 'http://' == word[0] or 'https://' == word[0]:
                                caption_text = re.sub(r"https?://[^,\s]+,?", word[2], message.caption)
                            else:
                                caption_text = message.caption.replace(word[0], word[2])
                for recipient in await db.get_recipients(chat_message[0]):
                    if not message.reply_to_message == None:
                        reply_id = await db.get_reply_id(
                            from_id=message.sender_chat['id'], 
                            to_id=recipient[0], 
                            from_word_id=message.reply_to_message.message_id)
                        new_message = await cfg.parser.send_photo(recipient[0], message.photo.file_id, caption=caption_text, reply_to_message_id=reply_id)
                    else:
                        new_message = await cfg.parser.send_photo(recipient[0], message.photo.file_id, caption=caption_text)
                    await db.add_history(
                        from_id = message.sender_chat['id'],
                        to_id = recipient[0],
                        from_word_id = message.message_id,
                        to_word_id = new_message.message_id,
                    )
            elif message.media == 'audio':
                caption_text = message.caption
                for word in await db.get_ignore(chat_message[0]):
                    if word[0] in caption_text:
                        if word[1]:
                            return
                        elif word[2] == None:
                            if word[0] == "@":
                                caption_text = re.sub(r"@[^,\s]+,?", "", message.caption)
                            elif 'http://' == word[0] or 'https://' == word[0]:
                                caption_text = re.sub(r"https?://[^,\s]+,?", "", message.caption)
                            else:
                                caption_text = message.caption.replace(word[0], '')
                        else:
                            if word[0] == "@":
                                caption_text = re.sub(r"@[^,\s]+,?", word[2], message.caption)
                            elif 'http://' == word[0] or 'https://' == word[0]:
                                caption_text = re.sub(r"https?://[^,\s]+,?", word[2], message.caption)
                            else:
                                caption_text = message.caption.replace(word[0], word[2])
                for recipient in await db.get_recipients(chat_message[0]):
                    if not message.reply_to_message == None:
                        reply_id = await db.get_reply_id(
                            from_id=message.sender_chat['id'], 
                            to_id=recipient[0], 
                            from_word_id=message.reply_to_message.message_id)
                        new_message = await cfg.parser.send_audio(recipient[0], message.audio.file_id, caption=caption_text, reply_to_message_id=reply_id)
                    else:
                        new_message = await cfg.parser.send_audio(recipient[0], message.audio.file_id, caption=caption_text)
                    await db.add_history(
                        from_id = message.sender_chat['id'],
                        to_id = recipient[0],
                        from_word_id = message.message_id,
                        to_word_id = new_message.message_id,
                    )
            elif message.media == 'document':
                caption_text = message.caption
                for word in await db.get_ignore(chat_message[0]):
                    if word[0] in caption_text:
                        if word[1]:
                            return
                        elif word[2] == None:
                            if word[0] == "@":
                                caption_text = re.sub(r"@[^,\s]+,?", "", message.caption)
                            elif 'http://' == word[0] or 'https://' == word[0]:
                                caption_text = re.sub(r"https?://[^,\s]+,?", "", message.caption)
                            else:
                                caption_text = message.caption.replace(word[0], '')
                        else:
                            if word[0] == "@":
                                caption_text = re.sub(r"@[^,\s]+,?", word[2], message.caption)
                            elif 'http://' == word[0] or 'https://' == word[0]:
                                caption_text = re.sub(r"https?://[^,\s]+,?", word[2], message.caption)
                            else:
                                caption_text = message.caption.replace(word[0], word[2])
                for recipient in await db.get_recipients(chat_message[0]):
                    if not message.reply_to_message == None:
                        reply_id = await db.get_reply_id(
                            from_id=message.sender_chat['id'], 
                            to_id=recipient[0], 
                            from_word_id=message.reply_to_message.message_id)
                        new_message = await cfg.parser.send_document(recipient[0], message.document.file_id, caption=caption_text, reply_to_message_id=reply_id)
                    else:
                        new_message = await cfg.parser.send_document(recipient[0], message.document.file_id, caption=caption_text)
                    await db.add_history(
                        from_id = message.sender_chat['id'],
                        to_id = recipient[0],
                        from_word_id = message.message_id,
                        to_word_id = new_message.message_id,
                    )
            elif message.media == 'video_note':
                caption_text = message.caption
                for word in await db.get_ignore(chat_message[0]):
                    if word[0] in caption_text:
                        if word[1]:
                            return
                        elif word[2] == None:
                            if word[0] == "@":
                                caption_text = re.sub(r"@[^,\s]+,?", "", message.caption)
                            elif 'http://' == word[0] or 'https://' == word[0]:
                                caption_text = re.sub(r"https?://[^,\s]+,?", "", message.caption)
                            else:
                                caption_text = message.caption.replace(word[0], '')
                        else:
                            if word[0] == "@":
                                caption_text = re.sub(r"@[^,\s]+,?", word[2], message.caption)
                            elif 'http://' == word[0] or 'https://' == word[0]:
                                caption_text = re.sub(r"https?://[^,\s]+,?", word[2], message.caption)
                            else:
                                caption_text = message.caption.replace(word[0], word[2])
                for recipient in await db.get_recipients(chat_message[0]):
                    if not message.reply_to_message == None:
                        reply_id = await db.get_reply_id(
                            from_id=message.sender_chat['id'], 
                            to_id=recipient[0], 
                            from_word_id=message.reply_to_message.message_id)
                        new_message = await cfg.parser.send_video_note(recipient[0], message.video_note.file_id, caption=caption_text, reply_to_message_id=reply_id)
                    else:
                        new_message = await cfg.parser.send_video_note(recipient[0], message.video_note.file_id, caption=caption_text)
                    await db.add_history(
                        from_id = message.sender_chat['id'],
                        to_id = recipient[0],
                        from_word_id = message.message_id,
                        to_word_id = new_message.message_id,
                    )
            elif message.media == 'sticker':
                caption_text = message.caption
                for word in await db.get_ignore(chat_message[0]):
                    if word[0] in caption_text:
                        if word[1]:
                            return
                        elif word[2] == None:
                            if word[0] == "@":
                                caption_text = re.sub(r"@[^,\s]+,?", "", message.caption)
                            elif 'http://' == word[0] or 'https://' == word[0]:
                                caption_text = re.sub(r"https?://[^,\s]+,?", "", message.caption)
                            else:
                                caption_text = message.caption.replace(word[0], '')
                        else:
                            if word[0] == "@":
                                caption_text = re.sub(r"@[^,\s]+,?", word[2], message.caption)
                            elif 'http://' == word[0] or 'https://' == word[0]:
                                caption_text = re.sub(r"https?://[^,\s]+,?", word[2], message.caption)
                            else:
                                caption_text = message.caption.replace(word[0], word[2])
                for recipient in await db.get_recipients(chat_message[0]):
                    if not message.reply_to_message == None:
                        reply_id = await db.get_reply_id(
                            from_id=message.sender_chat['id'], 
                            to_id=recipient[0], 
                            from_word_id=message.reply_to_message.message_id)
                        new_message = await cfg.parser.send_sticker(recipient[0], message.sticker.file_id, caption=caption_text, reply_to_message_id=reply_id)
                    else:
                        new_message = await cfg.parser.send_sticker(recipient[0], message.sticker.file_id, caption=caption_text)
                    await db.add_history(
                        from_id = message.sender_chat['id'],
                        to_id = recipient[0],
                        from_word_id = message.message_id,
                        to_word_id = new_message.message_id,
                    )
            elif message.media == 'animation':
                caption_text = message.caption
                for word in await db.get_ignore(chat_message[0]):
                    if word[0] in caption_text:
                        if word[1]:
                            return
                        elif word[2] == None:
                            if word[0] == "@":
                                caption_text = re.sub(r"@[^,\s]+,?", "", message.caption)
                            elif 'http://' == word[0] or 'https://' == word[0]:
                                caption_text = re.sub(r"https?://[^,\s]+,?", "", message.caption)
                            else:
                                caption_text = message.caption.replace(word[0], '')
                        else:
                            if word[0] == "@":
                                caption_text = re.sub(r"@[^,\s]+,?", word[2], message.caption)
                            elif 'http://' == word[0] or 'https://' == word[0]:
                                caption_text = re.sub(r"https?://[^,\s]+,?", word[2], message.caption)
                            else:
                                caption_text = message.caption.replace(word[0], word[2])
                for recipient in await db.get_recipients(chat_message[0]):
                    if not message.reply_to_message == None:
                        reply_id = await db.get_reply_id(
                            from_id=message.sender_chat['id'], 
                            to_id=recipient[0], 
                            from_word_id=message.reply_to_message.message_id)
                        new_message = await cfg.parser.send_animation(recipient[0], message.animation.file_id, caption=caption_text, reply_to_message_id=reply_id)
                    else:
                        new_message = await cfg.parser.send_animation(recipient[0], message.animation.file_id, caption=caption_text)
                    await db.add_history(
                        from_id = message.sender_chat['id'],
                        to_id = recipient[0],
                        from_word_id = message.message_id,
                        to_word_id = new_message.message_id,
                    )
            elif message.media == 'voice':
                caption_text = message.caption
                for word in await db.get_ignore(chat_message[0]):
                    if word[0] in caption_text:
                        if word[1]:
                            return
                        elif word[2] == None:
                            if word[0] == "@":
                                caption_text = re.sub(r"@[^,\s]+,?", "", message.caption)
                            elif 'http://' == word[0] or 'https://' == word[0]:
                                caption_text = re.sub(r"https?://[^,\s]+,?", "", message.caption)
                            else:
                                caption_text = message.caption.replace(word[0], '')
                        else:
                            if word[0] == "@":
                                caption_text = re.sub(r"@[^,\s]+,?", word[2], message.caption)
                            elif 'http://' == word[0] or 'https://' == word[0]:
                                caption_text = re.sub(r"https?://[^,\s]+,?", word[2], message.caption)
                            else:
                                caption_text = message.caption.replace(word[0], word[2])
                for recipient in await db.get_recipients(chat_message[0]):
                    if not message.reply_to_message == None:
                        reply_id = await db.get_reply_id(
                            from_id=message.sender_chat['id'], 
                            to_id=recipient[0], 
                            from_word_id=message.reply_to_message.message_id)
                        new_message = await cfg.parser.send_voice(recipient[0], message.voice.file_id, caption=caption_text, reply_to_message_id=reply_id)
                    else:
                        new_message = await cfg.parser.send_voice(recipient[0], message.voice.file_id, caption=caption_text)
                    await db.add_history(
                        from_id = message.sender_chat['id'],
                        to_id = recipient[0],
                        from_word_id = message.message_id,
                        to_word_id = new_message.message_id,
                    )
            elif message.media == 'video':
                caption_text = message.caption
                for word in await db.get_ignore(chat_message[0]):
                    if word[0] in caption_text:
                        if word[1]:
                            return
                        elif word[2] == None:
                            if word[0] == "@":
                                caption_text = re.sub(r"@[^,\s]+,?", "", message.caption)
                            elif 'http://' == word[0] or 'https://' == word[0]:
                                caption_text = re.sub(r"https?://[^,\s]+,?", "", message.caption)
                            else:
                                caption_text = message.caption.replace(word[0], '')
                        else:
                            if word[0] == "@":
                                caption_text = re.sub(r"@[^,\s]+,?", word[2], message.caption)
                            elif 'http://' == word[0] or 'https://' == word[0]:
                                caption_text = re.sub(r"https?://[^,\s]+,?", word[2], message.caption)
                            else:
                                caption_text = message.caption.replace(word[0], word[2])
                for recipient in await db.get_recipients(chat_message[0]):
                    if not message.reply_to_message == None:
                        reply_id = await db.get_reply_id(
                            from_id=message.sender_chat['id'], 
                            to_id=recipient[0], 
                            from_word_id=message.reply_to_message.message_id)
                        new_message = await cfg.parser.send_video(recipient[0], message.video.file_id, caption=caption_text, reply_to_message_id=reply_id)
                    else:
                        new_message = await cfg.parser.send_video(recipient[0], message.video.file_id, caption=caption_text)
                    await db.add_history(
                        from_id = message.sender_chat['id'],
                        to_id = recipient[0],
                        from_word_id = message.message_id,
                        to_word_id = new_message.message_id,
                    )

if __name__ == "__main__":
    cfg.parser.run()