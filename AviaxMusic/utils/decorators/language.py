from AviaxMusic.misc import SUDOERS
from AviaxMusic.utils.database import get_lang, is_maintenance
from strings import get_string


def language(mystic):
    async def wrapper(_, message, **kwargs):
        # Check if the bot is in maintenance mode
        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    text=f"{app.mention} ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ, ᴠɪsɪᴛ <a href={SUPPORT_GROUP}>sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ</a> ғᴏʀ ᴋɴᴏᴡɪɴɢ ᴛʜᴇ ʀᴇᴀsᴏɴ.",
                    disable_web_page_preview=True,
                )
        try:
            await message.delete()
        except:
            pass

        try:
            # Get language for the chat
            language = await get_lang(message.chat.id)
            language = get_string(language)
        except:
            # Default to English if no language is set
            language = get_string("en")
        return await mystic(_, message, language)

    return wrapper


def languageCB(mystic):
    async def wrapper(_, CallbackQuery, **kwargs):
        # Check if the bot is in maintenance mode
        if await is_maintenance() is False:
            if CallbackQuery.from_user.id not in SUDOERS:
                return await CallbackQuery.answer(
                    f"{app.mention} ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ, ᴠɪsɪᴛ sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ ғᴏʀ ᴋɴᴏᴡɪɴɢ ᴛʜᴇ ʀᴇᴀsᴏɴ.",
                    show_alert=True,
                )
        try:
            # Get language for the chat
            language = await get_lang(CallbackQuery.message.chat.id)
            language = get_string(language)
        except:
            # Default to English if no language is set
            language = get_string("en")
        return await mystic(_, CallbackQuery, language)

    return wrapper


def LanguageStart(mystic):
    async def wrapper(_, message, **kwargs):
        try:
            # Get language for the chat
            language = await get_lang(message.chat.id)
            language = get_string(language)
        except:
            # Default to English if no language is set
            language = get_string("en")
        
        # Execute the wrapped function with the selected language
        return await mystic(_, message, language)

    return wrapper
    
