import logging
from pyrogram import Client, emoji, filters
from pyrogram.errors.exceptions.bad_request_400 import QueryIdInvalid
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultCachedDocument, InlineQuery
from database.ia_filterdb import get_search_results
from utils import is_subscribed, get_size, temp, get_settings, save_group_settings
from info import CACHE_TIME, AUTH_USERS, AUTH_CHANNEL, CUSTOM_FILE_CAPTION, REQ_CHANNEL
from googletrans import Translator
from database.connections_mdb import active_connection
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent
)


logger = logging.getLogger(__name__)
cache_time = 0 if AUTH_USERS or AUTH_CHANNEL else CACHE_TIME

async def inline_users(query: InlineQuery):
    if AUTH_USERS:
        if query.from_user and query.from_user.id in AUTH_USERS:
            return True
        else:
            return False
    if query.from_user and query.from_user.id not in temp.BANNED_USERS:
        return True
    return False

@Client.on_inline_query()
async def answer(bot, query):
    """Show search results for given inline query"""
    chat_id = await active_connection(str(query.from_user.id))    
    if not await inline_users(query):
        await query.answer(results=[],
                           cache_time=0,
                           switch_pm_text='Ithu Paid Feature',
                           switch_pm_parameter="hehe")
        return

    if (AUTH_CHANNEL or REQ_CHANNEL) and not await is_subscribed(bot, query):
        await query.answer(results=[],
                           cache_time=0,
                           switch_pm_text='You have to Join Our Channel to use the Bot',
                           switch_pm_parameter="Join")
        return

    results = []
    if '|' in query.query:
        string, file_type = query.query.split('|', maxsplit=1)
        string = string.strip()
        file_type = file_type.strip().lower()
    else:
        string = query.query.strip()
        file_type = None

    offset = int(query.offset or 0)
    reply_markup = get_reply_markup(query=string)
    files, next_offset, total = await get_search_results(
                                                  chat_id,
                                                  string,
                                                  file_type=file_type,
                                                  max_results=10,
                                                  offset=offset)

    for file in files:
        title=file.file_name
        size=get_size(file.file_size)
        settings = await get_settings(chat_id)
        FILE_CAPTION = settings["caption"]
        f_caption=file.caption
        if settings["caption"]:
            try:
                f_caption=FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
                f_caption=f_caption
        if f_caption is None:
            f_caption = f"{file.file_name}"
        results.append(
            InlineQueryResultCachedDocument(
                title=file.file_name,
                document_file_id=file.file_id,
                caption=f_caption,
                description=f'Size: {get_size(file.file_size)}\nType: {file.file_type}',
                reply_markup=reply_markup))

    if results:
        switch_pm_text = f"{emoji.FILE_FOLDER} Results - {total}"
        if string:
            switch_pm_text += f" for {string}"
        try:
            await query.answer(results=results,
                           is_personal = True,
                           cache_time=cache_time,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="start",
                           next_offset=str(next_offset))
        except QueryIdInvalid:
            pass
        except Exception as e:
            logging.exception(str(e))
    else:
        switch_pm_text = f'{emoji.CROSS_MARK} No results'
        if string:
            switch_pm_text += f' for "{string}"'

        await query.answer(results=[],
                           is_personal = True,
                           cache_time=cache_time,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="okay")


def get_reply_markup(query):
    buttons = [
        [
            InlineKeyboardButton('Search Again', switch_inline_query_current_chat=query)
        ]
        ]
    return InlineKeyboardMarkup(buttons)


@Client.on_inline_query()
async def inline(_, query: InlineQuery):
        string = query.query.lower()
        if string == "":
        	METHOD=  [ InlineQueryResultArticle( title="How To Use", input_message_content=InputTextMessageContent("Ex ; ```@Googletranslateitbot how to use # hi```"),description="{Text} # {language code} ",thumb_url="https://tg-link.herokuapp.com/dl/0/AgADh60xG50-wFc.jpg")]
        	await query.answer( results=METHOD,  cache_time=2, switch_pm_text="Using Method",switch_pm_parameter="start" )
        else:
        	splitit = string.split("#")        	     	
        try:
        		cd = splitit[1].lower().replace(" ", "")
        		text = splitit[0]
        except:
        	METHOD=  [ InlineQueryResultArticle( title="How To Use", input_message_content=InputTextMessageContent("Ex ; ```@Googletranslateitbot how to use # hi```"),description="{Text}#{language code} ",thumb_url="https://tg-link.herokuapp.com/dl/0/AgADh60xG50-wFc.jpg")]
        	await query.answer( results=METHOD,  cache_time=2, switch_pm_text="Using Method",switch_pm_parameter="start" )
        	return
        try:
        	translator = Translator()
        	translation = translator.translate(text,dest = cd)
        except:
        	return
        TRTEXT=  [ InlineQueryResultArticle( title=f"Translated from {translation.src} To {translation.dest}", input_message_content=InputTextMessageContent(translation.text),description=f'{translation.text}',thumb_url="https://tg-link.herokuapp.com/dl/0/AgADh60xG50-wFc.jpg")]
        try:
        	await query.answer(results=TRTEXT ,  cache_time=2, switch_pm_text="Google Translater",switch_pm_parameter="start")
        except:
        	return

