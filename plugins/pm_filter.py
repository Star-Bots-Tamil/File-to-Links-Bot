import asyncio
import re
import ast
import math
import random
lock = asyncio.Lock()

from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
import pyrogram
from info import ADMINS, AUTH_CHANNEL, AUTH_USERS, SUPPORT_CHAT_ID, CUSTOM_FILE_CAPTION, MSG_ALRT, PICS, AUTH_GROUPS, P_TTI_SHOW_OFF, GRP_LNK, CHNL_LNK, NOR_IMG, LOG_CHANNEL, SPELL_IMG, MAX_B_TN, IMDB, \
    SINGLE_BUTTON, SPELL_CHECK_REPLY, IMDB_TEMPLATE, NO_RESULTS_MSG, IS_VERIFY, HOW_TO_VERIFY, REQ_CHANNEL, DOWNLOAD_TEXT_URL, DOWNLOAD_TEXT_NAME, LANGUAGES, SEASONS, OWNER_ID
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import get_size, is_subscribed, temp, get_settings, save_user_settings, get_shortlink
from database.database import db
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        await query.message.delete()
        await query.answer("Closed Current Process...!")

    elif query.data == "start":
        buttons = [[
                    InlineKeyboardButton('⤬ Aᴅᴅ Mᴇ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ ⤬', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
                ],[
                    InlineKeyboardButton('♚ Bᴏᴛ Oᴡɴᴇʀ', callback_data="owner_info"),
                    InlineKeyboardButton('⌬ Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url=GRP_LNK)
                ],[
                    InlineKeyboardButton('〄 Hᴇʟᴘ', callback_data='help'),
                    InlineKeyboardButton('⍟ Aʙᴏᴜᴛ', callback_data='about'),
                    InlineKeyboardButton('Iɴʟɪɴᴇ Sᴇᴀʀᴄʜ ☌', switch_inline_query_current_chat='')
                ],[
                    InlineKeyboardButton('✇ Jᴏɪɴ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ ✇', url=CHNL_LNK)
                  ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        await query.answer(MSG_ALRT)
    
    elif query.data == "help":
        buttons = [[
            InlineKeyboardButton('📊 Status', callback_data='stats'),            
            ],[
            InlineKeyboardButton('Custom to Your Bot 🤖', callback_data='stats'),            
            ],[
            InlineKeyboardButton('Filters', callback_data='filters'),
            InlineKeyboardButton('Group Manage', callback_data='group_manege'),
            InlineKeyboardButton('Connections', callback_data='coct')
            ],[                       
            InlineKeyboardButton('IMDB', callback_data='template'),
            InlineKeyboardButton('Your Info', callback_data='extra'),
            InlineKeyboardButton('Json', callback_data='son')
            ],[           
            InlineKeyboardButton('Font', callback_data='font'),
            InlineKeyboardButton('Share Text', callback_data='sharetxt'),           
            InlineKeyboardButton('Text 2 Speech', callback_data='ttss')
            ],[
            InlineKeyboardButton('Graph', callback_data='graph'),
            InlineKeyboardButton("File Store", callback_data='newdata'),
            InlineKeyboardButton('Sticker ID', callback_data='stickerid')                                   
            ],[                               
            InlineKeyboardButton('Purge', callback_data='purges'),
            InlineKeyboardButton('Ping', callback_data='pings'),
            InlineKeyboardButton('Short Link', callback_data='short')
            ],[
            InlineKeyboardButton('Password', callback_data='password'),
            InlineKeyboardButton("Paste", callback_data='pastes'),
            InlineKeyboardButton('YT-DL', callback_data='ytdl')
            ],[
            InlineKeyboardButton('Country Info', callback_data='country'),
            InlineKeyboardButton('Translate', callback_data='translate'),
            InlineKeyboardButton('File Store', callback_data='store_file')
            ],[
            InlineKeyboardButton('🏠 Home 🏠', callback_data='start')           
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS), script.HELP_TXT.format(query.from_user.mention), enums.ParseMode.HTML),
            reply_markup=reply_markup
            #parse_mode=enums.ParseMode.HTML
        )
    
    elif query.data == "stats":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='help'),
            InlineKeyboardButton('⟲ Rᴇғʀᴇsʜ', callback_data='rfrsh')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        users = await db.total_users_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        if query.from_user.id in ADMINS:
            await query.message.edit_text(script.STATUS_TXT.format(users, monsize, free), enums.ParseMode.HTML), reply_markup=reply_markup)
        else:
            await query.answer("Your Not Administrator ⚠️", show_alert=True)

    elif query.data == "rfrsh":
        await query.answer("Fetching MongoDb DataBase")
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='help'),
            InlineKeyboardButton('⟲ Rᴇғʀᴇsʜ', callback_data='rfrsh')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        users = await db.total_users_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        if query.from_user.id in ADMINS:
            await query.message.edit_text(script.STATUS_TXT.format(users, monsize, free), enums.ParseMode.HTML), reply_markup=reply_markup)
        else:
            await query.answer("Your Not Administrator ⚠️", show_alert=True)
    elif query.data == "refresh":
        await query.answer("Fetching MongoDb DataBase")
        buttons = [[
            InlineKeyboardButton('🌀 Refresh', callback_data='refresh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        users = await db.total_users_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        if query.from_user.id in ADMINS:
            await query.message.edit_text(script.STATUS_TXT.format(users, monsize, free), enums.ParseMode.HTML), reply_markup=reply_markup)
        else:
            await query.answer("Your Not Administrator ⚠️", show_alert=True)
