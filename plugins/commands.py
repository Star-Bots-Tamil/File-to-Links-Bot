import os
import logging
import random
import asyncio
import time
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid
from plugins.extract import extract_time, extract_user                               
from plugins.extract import extract_time, extract_user 
from info import ADMINS
from Script import script
from time import time, sleep
from pyrogram import Client, filters, enums 
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired, UserAdminInvalid
from utils import get_settings, is_subscribed, save_user_settings, temp
from urllib.parse import quote
from plugins.keyboard import ikb
from pyrogram.file_id import FileId
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os, asyncio, aiofiles, aiofiles.os, datetime, traceback,random, string, time, logging
logger = logging.getLogger(__name__)
from random import choice
import os
import math
import time
import requests
from pyrogram import Client, filters, enums
from database.database import db
from info import *
import re
import json
import base64
import datetime
import time
from utils import broadcast_messages
import asyncio
import re, asyncio, time, shutil, psutil, os, sys
import os
import aiohttp
import requests
from pyrogram.handlers import MessageHandler
from pyshorteners import Shortener
from utils import humanbytes
logger = logging.getLogger(__name__)
from asyncio.exceptions import TimeoutError
from telethon.sync import TelegramClient
from stream.utils.human_readable import humanbytes
from urllib.parse import quote_plus
from stream.utils.file_properties import get_name, get_hash, get_media_file_size
import os, requests, asyncio, math, time, wget
from io import BytesIO

#=====================================================

HEROKU_API_KEY = (os.environ.get("HEROKU_API_KEY", "7f5531d8-e346-4eef-98be-13c69630c7bd"))
ERROR_MESSAGE = "**Oops! An Exception Occurred! \n\nError : {}**"
ADMIN = int(os.environ.get("ADMIN", "1391556668"))

#=====================================================

BATCH_FILES = {}

async def get_channel_shortlink(link):
    url = 'https://tnshort.net/api'
    params = {'api': "d03a53149bf186ac74d58ff80d916f7a79ae5745", 'url': link}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
            data = await response.json()
            return data["shortenedUrl"]

async def get_channel_shortlinkk(url):
    if True:
        shortzy = Shortzy(SHORTLINK_API, SHORTLINK_URL)
        try:
            url = await shortzy.convert(url)
        except Exception as e:
            url = await shortzy.get_quick_link(url)

    return url

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
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
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        await asyncio.sleep(2) # 😢 https://github.com/EvamariaTG/EvaMaria/blob/master/plugins/p_ttishow.py#L17 😬 wait a bit, before checking.
        if not await db.get_chat(message.chat.id):
            total=await client.get_chat_members_count(message.chat.id)
            await client.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, "Unknown"))       
            await db.add_chat(message.chat.id, message.chat.title)
        return 
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))
    if len(message.command) != 2:
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
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
    if (AUTH_CHANNEL or REQ_CHANNEL) and not await is_subscribed(client, message):
        try:
            invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
            invite_link3 = await client.create_chat_invite_link(int(REQ_CHANNEL))
        except ChatAdminRequired:
            logger.error("Mᴀᴋᴇ sᴜʀᴇ Bᴏᴛ ɪs ᴀᴅᴍɪɴ ɪɴ Fᴏʀᴄᴇsᴜʙ ᴄʜᴀɴɴᴇʟ")
            return
        btn = [
            [
                InlineKeyboardButton(
                    "❆ Jᴏɪɴ Oᴜʀ Bᴀᴄᴋ-Uᴘ Cʜᴀɴɴᴇʟ ❆", url=invite_link.invite_link
                )
            ],
            [
                InlineKeyboardButton(
                    "❆ Jᴏɪɴ Oᴜʀ Cʜᴀɴɴᴇʟ ❆", url=CHNL_LNK
                )
	    ],
            [
                InlineKeyboardButton(
                    "❆ Jᴏɪɴ Oᴜʀ Cʜᴀɴɴᴇʟ ❆", url="https://t.me/+YeduZ6Ztq2YwNTdl"
                )
	    ]		
        ]

        if message.command[1] != "subscribe":
            try:
                kk, file_id = message.command[1].split("_", 1)
                pre = 'checksubp' if kk == 'filep' else 'checksub' 
                btn.append([InlineKeyboardButton("↻ Tʀʏ Aɢᴀɪɴ", callback_data=f"{pre}#{file_id}")])
            except (IndexError, ValueError):
                btn.append([InlineKeyboardButton("↻ Tʀʏ Aɢᴀɪɴ", url=f"https://t.me/{temp.U_NAME}?start={message.command[1]}")])
        await client.send_message(
            chat_id=message.from_user.id,
            text="**Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ɪɴ ᴏᴜʀ Bᴀᴄᴋ-ᴜᴘ ᴄʜᴀɴɴᴇʟ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ sᴏ ʏᴏᴜ ᴅᴏɴ'ᴛ ɢᴇᴛ ᴛʜᴇ ᴍᴏᴠɪᴇ ғɪʟᴇ...\n\nIғ ʏᴏᴜ ᴡᴀɴᴛ ᴛʜᴇ ᴍᴏᴠɪᴇ ғɪʟᴇ, ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ '❆ Jᴏɪɴ Oᴜʀ Bᴀᴄᴋ-Uᴘ Cʜᴀɴɴᴇʟ ❆' ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴀɴᴅ ᴊᴏɪɴ ᴏᴜʀ ʙᴀᴄᴋ-ᴜᴘ ᴄʜᴀɴɴᴇʟ, ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ '↻ Tʀʏ Aɢᴀɪɴ' ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ...\n\nTʜᴇɴ ʏᴏᴜ ᴡɪʟʟ ɢᴇᴛ ᴛʜᴇ ᴍᴏᴠɪᴇ ғɪʟᴇs...**",
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode=enums.ParseMode.MARKDOWN
            )
        return
    if len(message.command) == 2 and message.command[1] in ["subscribe", "error", "okay", "help"]:
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
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
    data = message.command[1]
    try:
        pre, file_id = data.split('_', 1)
    except:
        file_id = data
        pre = ""
    if data.split("-", 1)[0] == "BATCH":
        sts = await message.reply("<b>Pʟᴇᴀsᴇ ᴡᴀɪᴛ...</b>")
        file_id = data.split("-", 1)[1]
        msgs = BATCH_FILES.get(file_id)
        if not msgs:
            file = await client.download_media(file_id)
            try: 
                with open(file) as file_data:
                    msgs=json.loads(file_data.read())
            except:
                await sts.edit("Fᴀɪʟᴇᴅ")
                return await client.send_message(LOG_CHANNEL, "Uɴᴀʙʟᴇ Tᴏ Oᴘᴇɴ Fɪʟᴇ.")
            os.remove(file)
            BATCH_FILES[file_id] = msgs
        for msg in msgs:
            title = msg.get("title")
            size=get_size(int(msg.get("size", 0)))
            grp_id = await active_connection(str(message.from_user.id))
            settings = await get_settings(grp_id)
            FILE_CAPTION = settings["caption"]
            f_caption=msg.get("caption", "")
            if settings["caption"]:
                try:
                    f_caption=FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
                except Exception as e:
                    logger.exception(e)
                    f_caption=f_caption
            if f_caption is None:
                f_caption = f"{title}"
            try:
                feck=await client.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=msg.get("file_id"),
                    caption=f_caption+f"\n\n<b>Note :- This File Will be Deleted in {round(FILE_DELETE_TIMER/60)} Minutes. So Forward to Your Saved Messages.</b>",
                    protect_content=msg.get('protect', False),
                    reply_markup=InlineKeyboardMarkup(
                        [
                         [
                          InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url=await get_group(grp_id)),
                          InlineKeyboardButton('Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ', url=await get_channel(grp_id))
                       ],[
                          InlineKeyboardButton("Bᴏᴛ Oᴡɴᴇʀ", url=await get_admin(grp_id))
                         ]
                        ]
                    )
                )
                await asyncio.sleep(FILE_DELETE_TIMER)
                await feck.delete()
            except FloodWait as e:
                await asyncio.sleep(e.x)
                logger.warning(f"Floodwait of {e.x} sec.")
                feck=await client.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=msg.get("file_id"),
                    caption=f_caption+f"\n\n<b>Note :- This File Will be Deleted in {round(FILE_DELETE_TIMER/60)} Minutes. So Forward to Your Saved Messages.</b>",
                    protect_content=msg.get('protect', False),
                    reply_markup=InlineKeyboardMarkup(
                        [
                         [
                          InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url=await get_group(grp_id)),
                          InlineKeyboardButton('Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ', url=await get_channel(grp_id))
                       ],[
                          InlineKeyboardButton("Bᴏᴛ Oᴡɴᴇʀ", url=await get_admin(grp_id))
                         ]
                        ]
                    )
                )
                await asyncio.sleep(FILE_DELETE_TIMER)
                await feck.delete()
            except Exception as e:
                logger.warning(e, exc_info=True)
                continue
            await asyncio.sleep(1) 
        await sts.delete()
        return
    elif data.split("-", 1)[0] == "DSTORE":
        sts = await message.reply("<b>Pʟᴇᴀsᴇ ᴡᴀɪᴛ...</b>")
        b_string = data.split("-", 1)[1]
        decoded = (base64.urlsafe_b64decode(b_string + "=" * (-len(b_string) % 4))).decode("ascii")
        try:
            f_msg_id, l_msg_id, f_chat_id, protect = decoded.split("_", 3)
        except:
            f_msg_id, l_msg_id, f_chat_id = decoded.split("_", 2)
            protect = "/pbatch" if PROTECT_CONTENT else "batch"
        diff = int(l_msg_id) - int(f_msg_id)
        async for msg in client.iter_messages(int(f_chat_id), int(l_msg_id), int(f_msg_id)):
            if msg.media:
                media = getattr(msg, msg.media.value)
                grp_id = await active_connection(str(message.from_user.id))
                settings = await get_settings(grp_id)
                FILE_CAPTION = settings["caption"]
                if settings["caption"]:
                    try:
                        f_caption=FILE_CAPTION.format(file_name=getattr(media, 'file_name', ''), file_size=getattr(media, 'file_size', ''), file_caption=getattr(msg, 'caption', ''))
                    except Exception as e:
                        logger.exception(e)
                        f_caption = getattr(msg, 'caption', '')
                else:
                    media = getattr(msg, msg.media.value)
                    file_name = getattr(media, 'file_name', '')
                    f_caption = getattr(msg, 'caption', file_name)
                try:
                    await msg.copy(message.chat.id, caption=f_caption, protect_content=True if protect == "/pbatch" else False)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(message.chat.id, caption=f_caption, protect_content=True if protect == "/pbatch" else False)
                except Exception as e:
                    logger.exception(e)
                    continue
            elif msg.empty:
                continue
            else:
                try:
                    await msg.copy(message.chat.id, protect_content=True if protect == "/pbatch" else False)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(message.chat.id, protect_content=True if protect == "/pbatch" else False)
                except Exception as e:
                    logger.exception(e)
                    continue
            await asyncio.sleep(1) 
        return await sts.delete()

    elif data.split("-", 1)[0] == "verify":
        userid = data.split("-", 2)[1]
        token = data.split("-", 3)[2]
        fileid = data.split("-", 3)[3]
        if str(message.from_user.id) != str(userid):
            return await message.reply_text(
                text="<b>Iɴᴠᴀʟɪᴅ ʟɪɴᴋ ᴏʀ Exᴘɪʀᴇᴅ ʟɪɴᴋ !</b>",
                protect_content=True if PROTECT_CONTENT else False
            )
        is_valid = await check_token(client, userid, token)
        if is_valid == True:
            if fileid == "send_all":
                btn = [[
                    InlineKeyboardButton("Gᴇᴛ Fɪʟᴇ", callback_data=f"checksub#send_all")
                ]]
                await verify_user(client, userid, token)
                await message.reply_text(
                    text=f"<b>Hᴇʏ {message.from_user.mention}, Yᴏᴜ ᴀʀᴇ sᴜᴄᴄᴇssғᴜʟʟʏ ᴠᴇʀɪғɪᴇᴅ !\nNᴏᴡ ʏᴏᴜ ʜᴀᴠᴇ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss ғᴏʀ ᴀʟʟ ᴍᴏᴠɪᴇs ᴛɪʟʟ ᴛʜᴇ ɴᴇxᴛ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴡʜɪᴄʜ ɪs ᴀғᴛᴇʀ 12 ʜᴏᴜʀs ғʀᴏᴍ ɴᴏᴡ.</b>",
                    protect_content=True if PROTECT_CONTENT else False,
                    reply_markup=InlineKeyboardMarkup(btn)
                )
                return
            btn = [[
                InlineKeyboardButton("Get File", url=f"https://telegram.me/{temp.U_NAME}?start=files_{fileid}")
            ]]
            await message.reply_text(
                text=f"<b>Hᴇʏ {message.from_user.mention}, Yᴏᴜ ᴀʀᴇ sᴜᴄᴄᴇssғᴜʟʟʏ ᴠᴇʀɪғɪᴇᴅ !\nNᴏᴡ ʏᴏᴜ ʜᴀᴠᴇ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss ғᴏʀ ᴀʟʟ ᴍᴏᴠɪᴇs ᴛɪʟʟ ᴛʜᴇ ɴᴇxᴛ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴡʜɪᴄʜ ɪs ᴀғᴛᴇʀ 12 ʜᴏᴜʀs ғʀᴏᴍ ɴᴏᴡ.</b>",
                protect_content=True if PROTECT_CONTENT else False,
                reply_markup=InlineKeyboardMarkup(btn)
            )
            await verify_user(client, userid, token)
            return
        else:
            return await message.reply_text(
                text="<b>Iɴᴠᴀʟɪᴅ ʟɪɴᴋ ᴏʀ Exᴘɪʀᴇᴅ ʟɪɴᴋ !</b>",
                protect_content=True if PROTECT_CONTENT else False
            )

    files_ = await get_file_details(file_id)           
    if not files_:
        pre, file_id = ((base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))).decode("ascii")).split("_", 1)
        try:
            if IS_VERIFY and not await check_verification(client, message.from_user.id):
                btn = [[
                    InlineKeyboardButton("Vᴇʀɪғʏ", url=await get_token(client, message.from_user.id, f"https://telegram.me/{temp.U_NAME}?start=", file_id)),
                    InlineKeyboardButton("Hᴏᴡ Tᴏ Vᴇʀɪғʏ", url=HOW_TO_VERIFY)
                ]]
                await message.reply_text(
                    text="<b>Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴠᴇʀɪғɪᴇᴅ!\nKɪɴᴅʟʏ ᴠᴇʀɪғʏ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ Sᴏ ᴛʜᴀᴛ ʏᴏᴜ ᴄᴀɴ ɢᴇᴛ ᴀᴄᴄᴇss ᴛᴏ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏᴠɪᴇs ᴜɴᴛɪʟ 12 ʜᴏᴜʀs ғʀᴏᴍ ɴᴏᴡ !</b>",
                    protect_content=True if PROTECT_CONTENT else False,
                    reply_markup=InlineKeyboardMarkup(btn)
                )
                return
            msg = await client.send_cached_media(
                chat_id=message.from_user.id,
                file_id=file_id,
                protect_content=True if pre == 'filep' else False,
                reply_markup=InlineKeyboardMarkup(
                    [
                     [
                      InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url=await get_group(grp_id)),
                      InlineKeyboardButton('Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ', url=await get_channel(grp_id))
                   ],[
                      InlineKeyboardButton("Bᴏᴛ Oᴡɴᴇʀ", url=await get_admin(grp_id))
                     ]
                    ]
                )
            )
            filetype = msg.media
            file = getattr(msg, filetype.value)
            title = file.file_name
            size=get_size(file.file_size)
            grp_id = await active_connection(str(message.from_user.id))
            settings = await get_settings(grp_id)
            FILE_CAPTION = settings["caption"]
            f_caption = f"<code>{title}</code>"
            if settings["caption"]:
                try:
                    f_caption=FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
                except:
                    return
            await msg.edit_caption(f_caption)
            return
        except:
            pass
        return await message.reply('Nᴏ sᴜᴄʜ ғɪʟᴇ ᴇxɪsᴛ.')
    files = files_[0]
    title = files.file_name
    size=get_size(files.file_size)
    grp_id = await active_connection(str(message.from_user.id))
    settings = await get_settings(grp_id)
    FILE_CAPTION = settings["caption"]
    f_caption=files.caption
    if settings["caption"]:
        try:
            f_caption=FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
        except Exception as e:
            logger.exception(e)
            f_caption=f_caption
    if f_caption is None:
        f_caption = f"{files.file_name}"
    if IS_VERIFY and not await check_verification(client, message.from_user.id):
        btn = [[
            InlineKeyboardButton("Vᴇʀɪғʏ", url=await get_token(client, message.from_user.id, f"https://telegram.me/{temp.U_NAME}?start=", file_id)),
            InlineKeyboardButton("Hᴏᴡ Tᴏ Vᴇʀɪғʏ", url=HOW_TO_VERIFY)
        ]]
        await message.reply_text(
            text="<b>Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴠᴇʀɪғɪᴇᴅ!\nKɪɴᴅʟʏ ᴠᴇʀɪғʏ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ Sᴏ ᴛʜᴀᴛ ʏᴏᴜ ᴄᴀɴ ɢᴇᴛ ᴀᴄᴄᴇss ᴛᴏ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏᴠɪᴇs ᴜɴᴛɪʟ 12 ʜᴏᴜʀs ғʀᴏᴍ ɴᴏᴡ !</b>",
            protect_content=True if PROTECT_CONTENT else False,
            reply_markup=InlineKeyboardMarkup(btn)
        )
        return
    feck=await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=file_id,
        caption=f_caption+f"\n\n<b>Note :- This File Will be Deleted in {round(FILE_DELETE_TIMER/60)} Minutes. So Forward to Your Saved Messages.</b>",
        protect_content=True if pre == 'filep' else False,
        reply_markup=InlineKeyboardMarkup(
            [
             [
              InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url=await get_group(grp_id)),
              InlineKeyboardButton('Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ', url=await get_channel(grp_id))
           ],[
              InlineKeyboardButton("Bᴏᴛ Oᴡɴᴇʀ", url=await get_admin(grp_id))
             ]
            ]
        )
    )
    await asyncio.sleep(FILE_DELETE_TIMER)
    await feck.delete()
                
@Client.on_message(filters.command('settings'))
async def settings(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"Yᴏᴜ ᴀʀᴇ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ. Usᴇ /connect {message.chat.id} ɪɴ PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Mᴀᴋᴇ sᴜʀᴇ I'ᴍ ᴘʀᴇsᴇɴᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ !", quote=True)
                return
        else:
            await message.reply_text("I'ᴍ ɴᴏᴛ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ ᴀɴʏ ɢʀᴏᴜᴘs !", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return
    
    settings = await get_settings(grp_id)

    try:
        if settings['max_btn']:
            settings = await get_settings(grp_id)
    except KeyError:
        await save_group_settings(grp_id, 'max_btn', False)
        settings = await get_settings(grp_id)
    if 'is_shortlink' not in settings.keys():
        await save_group_settings(grp_id, 'is_shortlink', False)
    else:
        pass

    if settings is not None:
        buttons = [
            [
                InlineKeyboardButton(
                    'Fɪʟᴛᴇʀ Bᴜᴛᴛᴏɴ',
                    callback_data=f'setgs#button#{settings["button"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'Sɪɴɢʟᴇ' if settings["button"] else 'Dᴏᴜʙʟᴇ',
                    callback_data=f'setgs#button#{settings["button"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Fɪʟᴇ Sᴇɴᴅ Mᴏᴅᴇ',
                    callback_data=f'setgs#botpm#{settings["botpm"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'Mᴀɴᴜᴀʟ Sᴛᴀʀᴛ' if settings["botpm"] else 'Aᴜᴛᴏ Sᴇɴᴅ',
                    callback_data=f'setgs#botpm#{settings["botpm"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Pʀᴏᴛᴇᴄᴛ Cᴏɴᴛᴇɴᴛ',
                    callback_data=f'setgs#file_secure#{settings["file_secure"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✔ Oɴ' if settings["file_secure"] else '✘ Oғғ',
                    callback_data=f'setgs#file_secure#{settings["file_secure"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Iᴍᴅʙ',
                    callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✔ Oɴ' if settings["imdb"] else '✘ Oғғ',
                    callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Sᴘᴇʟʟ Cʜᴇᴄᴋ',
                    callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✔ Oɴ' if settings["spell_check"] else '✘ Oғғ',
                    callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Wᴇʟᴄᴏᴍᴇ Msɢ',
                    callback_data=f'setgs#welcome#{settings["welcome"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✔ Oɴ' if settings["welcome"] else '✘ Oғғ',
                    callback_data=f'setgs#welcome#{settings["welcome"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Aᴜᴛᴏ-Dᴇʟᴇᴛᴇ',
                    callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '10 Mɪɴs' if settings["auto_delete"] else '✘ Oғғ',
                    callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Aᴜᴛᴏ-Fɪʟᴛᴇʀ',
                    callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✔ Oɴ' if settings["auto_ffilter"] else '✘ Oғғ',
                    callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Mᴀx Bᴜᴛᴛᴏɴs',
                    callback_data=f'setgs#max_btn#{settings["max_btn"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '10' if settings["max_btn"] else f'{MAX_B_TN}',
                    callback_data=f'setgs#max_btn#{settings["max_btn"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'SʜᴏʀᴛLɪɴᴋ',
                    callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✔ Oɴ' if settings["is_shortlink"] else '✘ Oғғ',
                    callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{grp_id}',
                ),
            ],
        ]

        btn = [[
                InlineKeyboardButton("Oᴘᴇɴ Hᴇʀᴇ ↓", callback_data=f"opnsetgrp#{grp_id}"),
                InlineKeyboardButton("Oᴘᴇɴ Iɴ PM ⇲", callback_data=f"opnsetpm#{grp_id}")
              ]]

        reply_markup = InlineKeyboardMarkup(buttons)
        if chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            await message.reply_text(
                text="<b>Dᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴏᴘᴇɴ sᴇᴛᴛɪɴɢs ʜᴇʀᴇ ?</b>",
                reply_markup=InlineKeyboardMarkup(btn),
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML,
                reply_to_message_id=message.id
            )
        else:
            await message.reply_text(
                text=f"<b>Cʜᴀɴɢᴇ Yᴏᴜʀ Sᴇᴛᴛɪɴɢs Fᴏʀ {title} As Yᴏᴜʀ Wɪsʜ ⚙</b>",
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML,
                reply_to_message_id=message.id
            )

@Client.on_message(filters.command(["help"]) & filters.private, group=1)
async def help(client, message):
        buttons = [[
            InlineKeyboardButton('📊 Status', callback_data='stats'),            
            ],[
            InlineKeyboardButton('Manuel Filter', callback_data='manuelfilter'),
            InlineKeyboardButton('Auto Filter', callback_data='autofilter'),
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
            InlineKeyboardButton('Mute', callback_data='restric'),
            InlineKeyboardButton('Kick', callback_data='zombies'),
            InlineKeyboardButton('Pin', callback_data='pin')
            ],[
            InlineKeyboardButton('Password', callback_data='password'),
            InlineKeyboardButton("Paste", callback_data='pastes'),
            InlineKeyboardButton('YT-DL', callback_data='ytdl')
            ],[
            InlineKeyboardButton('🏠 Home 🏠', callback_data='start')           
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.HELP_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

@Client.on_message(filters.command(["about"]) & filters.private, group=1)
async def about(client, message):
        buttons = [[
            InlineKeyboardButton('Source Code', callback_data='source')
            ],[		
            InlineKeyboardButton('🏠 Home 🏠', callback_data='start'),
            InlineKeyboardButton('😎 Help', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.ABOUT_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

@Client.on_message(filters.command("group_broadcast") & filters.user(ADMINS) & filters.reply)
async def grp_brodcst(bot, message):
    chats = await db.get_all_chats()
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text='<b>Broadcasting Your Messages to Connected Groups 😁...</b>'
    )
    start_time = time.time()
    total_chats = await db.total_chat_count()
    done = 0
    failed =0

    success = 0
    async for chat in chats:
        pti, sh = await broadcast_messages(int(chat['id']), b_msg)
        if pti:
            success += 1
        elif pti == False:
            if sh == "Blocked":
                blocked+=1
            elif sh == "Deleted":
                deleted += 1
            elif sh == "Error":
                failed += 1
        done += 1
        await asyncio.sleep(2)
        if not done % 20:
            await sts.edit(f"<b>Broadcast in Progress :-\n\nTotal Chats {total_chats}\nCompleted :- {done} / {total_chats}\nSuccess :- {success}\nFailed :- {failed}</b>")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.edit(f"<b>Broadcast Completed :-\nCompleted in {time_taken} Seconds.\n\nTotal Chats {total_chats}\nCompleted :- {done} / {total_chats}\nSuccess :- {success}\nFailed :- {failed}</b>")


@Client.on_message(filters.command('channels') & filters.user(ADMINS))
async def channel_info(bot, message):
           
    """Send Basic Information of Channel"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Unexpected type of CHANNELS")

    text = '<b>📑 Indexed Channels/Groups</b>\n'
    for Channel in Channels :
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n<b>Total : {len(CHANNELS)}</b>'

    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)

@Client.on_message(filters.command('logs') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send Log File 📂"""
    file = 'StarMoviesBot.log'
    caption = '#Logs'
    try:
        await message.reply_document(
            file,
            caption=caption,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Get Web URL", callback_data='webmi')]])
	)
    except Exception as e:
        await message.reply(str(e))

@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("<b>🗑️ Deleting...</b>", quote=True)
    else:
        await message.reply('<b>Reply to File 📂 with /delete which You Want to Delete</b>', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('<b>This is not Supported File Format</b>')
        return
    
    file_id, file_ref = unpack_new_file_id(media.file_id)

    result = await Media.collection.delete_one({
        '_id': file_id,
    })
    if result.deleted_count:
        await msg.edit('<b>File 📂 Successfully Deleted</b>')
    else:
        file_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
        result = await Media.collection.delete_many({
            'file_name': file_name,
            'file_size': media.file_size,
            'mime_type': media.mime_type
            })
        if result.deleted_count:
            await msg.edit('<b>File 📂 Successfully Deleted</b>')
        else:
            # files indexed before  
            # have original file name.
            result = await Media.collection.delete_many({
                'file_name': media.file_name,
                'file_size': media.file_size,
                'mime_type': media.mime_type
            })
            if result.deleted_count:
                await msg.edit('<b>File 📂 Successfully Deleted</b>')
            else:
                await msg.edit('<b>File 📂 Not Found in Databas</b>')


@Client.on_message(filters.command('deleteall') & filters.user(ADMINS))
async def delete_all_index(bot, message):
    await message.reply_text(
        '<b>This Process Will Delete All The Files From Your Database.\nDo You Want to Continue This...??</b>',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⚡ Yes ⚡", callback_data="autofilter_delete"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⛔ Cancel ⛔", callback_data="close_data"
                    )
                ],
            ]
        ),
        quote=True,
    )


@Client.on_callback_query(filters.regex(r'^autofilter_delete'))
async def delete_all_index_confirm(bot, message):
    await Media.collection.drop()
    await message.answer('Please Share & Support Us')
    await message.message.edit('<b>Succesfully Deleted All The Indexed Files.</b>')

@Client.on_message(filters.channel & (filters.document | filters.video)  & ~filters.forwarded, group=-1)
async def channel_receive_handler(bot, broadcast):
    if int(broadcast.chat.id) in BANNED_CHANNELS:
        await bot.leave_chat(broadcast.chat.id)
        return
    try:
#        user_id = message.from_user.id
#        username =  message.from_user.mention
        channel_name = broadcast.chat.title
        channel_id = broadcast.chat.id
        log_msg = await broadcast.forward(
            chat_id=LOG_CHANNEL,
        )
        fileName = get_name(log_msg)
        filesize = humanbytes(get_media_file_size(log_msg))
        star_stream = f"{URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        star_download = f"{URL}download/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        shortened_link = await get_channel_shortlinkk(star_stream)
        await log_msg.reply_text(
            text=f"**⚡ Link Generated Successfully..!\n\nFile Name :- {fileName} \n\nFile Size :- {filesize}\n\nChannel Name :- {channel_name}\n\nChannel ID :-** `{channel_id}`",
            quote=True,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Download Link", url=star_download),  # we download Link
                                                InlineKeyboardButton('Watch Online', url=star_stream)]])  # web stream Link
        )
        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            message_id=broadcast.id,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📥 Fast Download Link", url=shortened_link)]])  # web stream Link
        )
    except FloodWait as w:
        print(f"Sleeping for {str(w.x)}s")
        await asyncio.sleep(w.x)
        await bot.send_message(chat_id=FILES_CHANNEL,
                             text=f"Got Floodwait Of {str(w.x)}s From {broadcast.chat.title}\n\n**Channel Id :-** `{str(broadcast.chat.id)}`",
                             disable_web_page_preview=True)
    except Exception as e:
        await bot.send_message(chat_id=FILES_CHANNEL, text=f"**#ERROR_TRACKEBACK:** `{e}`", disable_web_page_preview=True)
        print(f"Can't Edit Boardcast Message!\nError:  **Give me Edit Permission in Updates and Log Channel!{e}**")

@Client.on_message(filters.command('set_template'))
async def save_template(client, message):
    sts = await message.reply("<b>Checking New Template</b>")
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"<b>You are Anonymous Admin. Use /connect {message.chat.id} in PM</b>")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("<b>Make Sure I'm Present in Your Group!</b>", quote=True)
                return
        else:
            await message.reply_text("<b>I'm not Connected to any Groups!</b>", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    if len(message.command) < 2:
        return await sts.edit("**No Input!!**")
    template = message.text.split(" ", 1)[1]
    await save_group_settings(grp_id, 'template', template)
    await sts.edit(f"<b>Successfully Upgraded Your Template For {title} to\n\n{template}</b>")

@Client.on_message(filters.command('get_template'))
async def get_template(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    settings = await get_settings(grp_id)
    template = settings["template"]
    await message.reply_text(f"<b>IMDB Template for {title}\n\nYour Current IMDB Template\n\n</b>{template}")

@Client.on_message(filters.command('set_shortlink'))
async def set_shortlink(bot, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text(f"<b>Hey {message.from_user.mention}, This command only works on groups !</b>")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    data = message.text
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return await message.reply_text("<b>You don't have access to use this command !</b>")
    else:
        pass
    try:
        command, shortlink_url, api = data.split(" ")
    except:
        return await message.reply_text("<b>Command Incomplete :(\n\nGive me a shortlink and api along with the command !\n\nFormat: <code>/set_shortner tnshort.net d03a53149bf186ac74d58ff80d916f7a79ae5745</code></b>")
    reply = await message.reply_text("<b>Please Wait...</b>")
    await save_group_settings(grpid, 'shortlink', shortlink_url)
    await save_group_settings(grpid, 'shortlink_api', api)
    await save_group_settings(grpid, 'is_shortlink', True)
    await reply.edit_text(f"<b>Successfully added Shortlink API for {title}.\n\nCurrent Shortlink Website: <code>{shortlink_url}</code>\nCurrent API: <code>{api}</code></b>")

@Client.on_message(filters.command("get_shortlink"))
async def showshortlink(bot, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text(f"<b>Hey {message.from_user.mention}, This Command Only Works in Group\n\nTry this command in your own group, if you are using me in your group</b>")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    chat_id=message.chat.id
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    settings = await get_settings(chat_id) #fetching settings for group
    if 'shortlink' in settings.keys():
        su = settings['shortlink']
        sa = settings['shortlink_api']
    else:
        return await message.reply_text("<b>Shortener Url Not Connected\n\nYou can Connect Using /shortlink command</b>")
    if 'tutorial' in settings.keys():
        st = settings['tutorial']
    else:
        return await message.reply_text("<b>Tutorial Link Not Connected\n\nYou can Connect Using /set_tutorial command</b>")
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return await message.reply_text("<b>Tʜɪs ᴄᴏᴍᴍᴀɴᴅ Wᴏʀᴋs Oɴʟʏ Fᴏʀ ᴛʜɪs Gʀᴏᴜᴘ Oᴡɴᴇʀ/Aᴅᴍɪɴ\n\nTʀʏ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪɴ ʏᴏᴜʀ Oᴡɴ Gʀᴏᴜᴘ, Iғ Yᴏᴜ Aʀᴇ Usɪɴɢ Mᴇ Iɴ Yᴏᴜʀ Gʀᴏᴜᴘ</b>")
    else:
        if settings["is_shortlink"]:
            return await message.reply_text(f"<b>Shortlink Website: <code>{su}</code>\n\nApi: <code>{sa}</code>\n\nTutorial: <code>{st}</code></b>")
        elif settings["is_tutorial"]:
            return await message.reply_text(f"<b>Tutorial: <code>{st}</code></b>")
        else:
            return await message.reply_text("Shortlink Not Connected")

@Client.on_message(filters.command("set_tutorial"))
async def set_tutorial_link(client, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        await message.reply_text("<b>Please use this command in your group to set tutorial link.</b>")
        return
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return 
    
    userid = message.from_user.id
    user = await client.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        await message.reply_text("<b>You don't have access to use this command!</b>")
        return
    else:
        pass
    if len(message.command) == 1:
        return await message.reply("<b>Give me a tutorial link along with this command\n\nCommand Usage: /set_tutorial your tutorial link</b>")
    elif len(message.command) == 2:
        reply = await message.reply_text("<b>Please Wait...</b>")
        tutorial = message.command[1]
        await save_group_settings(grpid, 'tutorial', tutorial)
        await save_group_settings(grpid, 'is_tutorial', True)
        await reply.edit_text(f"<b>Successfully Added Tutorial\n\nHere is your tutorial link for your group {title} - <code>{tutorial}</code></b>")
    else:
        return await message.reply("<b>You entered Incorrect Format\n\nFormat: /set_tutorial your tutorial link</b>")
	    
@Client.on_message(filters.command('get_tutorial'))
async def get_tutorial_link(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    settings = await get_settings(grp_id)
    tutorial = settings["tutorial"]
    await message.reply_text(f"<b>Tutorial for {title}\n\nYour Tutorial Link :- {tutorial}</b>")

@Client.on_message(filters.command('set_caption'))
async def save_caption(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    try:
        caption = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text("<b>__Use this Command to Set the Custom Caption for Your Files. For Setting Your Caption Send Caption in the Format\n`/set_caption`__\n\nFile Caption Keys\n• `{file_name}` :- Replaced by the Filename.\n• `{file_size}` :- Replaced by the Filesize.\n• {file_caption}` :- Replaced by the Captain of Videos.\n\nExample :- `/set_caption <b>File Name :- {file_name}\n\n💾 File Size :- {file_size}\n\n✍🏻 File Caption :- {file_caption}</b>`\n\n⚠️ Note :- You Can Check the Current Caption using /get_caption</b>")
    
    await save_group_settings(grp_id, 'caption', caption)
    await message.reply_text(f"Successfully changed caption for {title} to\n\n{caption}")

@Client.on_message(filters.command('get_caption'))
async def get_caption(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    settings = await get_settings(grp_id)
    caption = settings["caption"]
    await message.reply_text(f"<b>Caption for {title}\n\nYour Caption\n\n</b>{caption}")

@Client.on_message(filters.command('set_welcome'))
async def save_welcome(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    try:
        welcome = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text("Command Incomplete!")
    
    await save_group_settings(grp_id, 'welcome_text', welcome)
    await save_group_settings(grpid, 'welcome', True)	
    await message.reply_text(f"Successfully changed welcome for {title} to\n\n{welcome}")

@Client.on_message(filters.command('get_welcome'))
async def get_welcome(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    settings = await get_settings(grp_id)
    welcome = settings["welcome_text"]
    await message.reply_text(f"<b>Welcome Message for {title}\n\nYour Group's Welcome Message\n\n</b>{welcome}")

@Client.on_message((filters.private | filters.group) & filters.command('set_spellcheck'))
async def setspell(client, message):
    sts = await message.reply("⏳️")
    await asyncio.sleep(0.3)
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f" 𝚈𝙾𝚄𝚁 𝙰𝚁𝙴 𝙰𝙽𝙾𝙽𝚈𝙼𝙾𝚄𝚂 𝙰𝙳𝙼𝙸𝙽. /connect {message.chat.id} 𝙸𝙽 𝙿𝙼")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("𝙼𝙰𝙺𝙴 𝚂𝚄𝚁𝙴 𝙸𝙰𝙼 𝙿𝚁𝙴𝚂𝙴𝙽𝚃 𝙸𝙽 𝚈𝙾𝚄𝚁 𝙶𝚁𝙾𝚄𝙿..!", quote=True)
                return
        else:
            await message.reply_text("𝙸𝙰𝙼 𝙽𝙾𝚃 𝙲𝙾𝙽𝙽𝙴𝙲𝚃𝙴𝙳 𝙰𝙽𝚃 𝙶𝚁𝙾𝚄𝙿..!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    member = await client.get_chat_member(grp_id, userid)
    if (
            member.status != enums.ChatMemberStatus.ADMINISTRATOR
            and member.status != enums.ChatMemberStatus.OWNER
            and userid not in ADMINS
    ):
        return

    if len(message.command) < 2:
        return await sts.edit("𝙷𝙾𝚆 𝚃𝙾 𝚄𝚂𝙴 𝚃𝙷𝙸𝚂 𝙲𝙾𝙼𝙼𝙰𝙽𝙳..!", reply_markup=InlineKeyboardMarkup( [[ InlineKeyboardButton("𝙲𝙻𝙸𝙲𝙺 𝙷𝙴𝚁𝙴", callback_data="spellcheck") ]] ))

    spell_check_text = message.text.split(" ", 1)[1]
    await save_group_settings(grp_id, 'spelltext', spell_check_text)
    await save_group_settings(grpid, 'spell_check', True)
    await sts.edit(f"""𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 𝙲𝙷𝙰𝙽𝙶𝙴𝙳 𝚂𝙴𝚃 𝚂𝙿𝙴𝙻𝙻 𝙲𝙷𝙴𝙲𝙺 𝙵𝙾𝚁 {title} 𝚃𝙾\n\n{spell_check_text}""", reply_markup=InlineKeyboardMarkup( [[ InlineKeyboardButton("× 𝙲𝙻𝙾𝚂𝙴 ×", callback_data="close") ]] ))

@Client.on_message(filters.command("set_channel"))
async def set_channel(bot, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("This Command Work Only in group\n\nTry it in your own group")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return
    else:
        pass
    if len(message.command) == 1:
        return await message.reply("<b>Give me a Channel link along with this command\n\nCommand Usage: /set_channel your channel link</b>")
    elif len(message.command) == 2:
        reply = await message.reply_text("<b>Please Wait...</b>")
        channel = message.command[1]
        await save_group_settings(grpid, 'channel', channel)
        await reply.edit_text(f"<b>Successfully Added Channel\n\nHere is your channel link for your group {title} - <code>{channel}</code></b>")
    else:
        return await message.reply("<b>You entered Incorrect Format\n\nFormat: /set_channel your channel link</b>")

@Client.on_message(filters.command('get_channel'))
async def get_channel_link(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    settings = await get_settings(grp_id)
    channel = settings["channel"]
    await message.reply_text(f"<b>Channel for {title}\n\nYour Channel Link :- {channel}</b>")

@Client.on_message(filters.command("set_group"))
async def set_group(bot, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("This Command Work Only in group\n\nTry it in your own group")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return
    else:
        pass
    if len(message.command) == 1:
        return await message.reply("<b>Give me a group link along with this command\n\nCommand Usage: /set_group your group link</b>")
    elif len(message.command) == 2:
        reply = await message.reply_text("<b>Please Wait...</b>")
        group = message.command[1]
        await save_group_settings(grpid, 'group', group)
        await reply.edit_text(f"<b>Successfully Added group\n\nHere is your group link for your group {title} - <code>{group}</code></b>")
    else:
        return await message.reply("<b>You entered Incorrect Format\n\nFormat: /set_group your group link</b>")

@Client.on_message(filters.command('get_group'))
async def get_group_link(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    settings = await get_settings(grp_id)
    group = settings["group"]
    await message.reply_text(f"<b>group for {title}\n\nYour group Link :- {group}</b>")

@Client.on_message(filters.command("set_rules"))
async def set_rules(bot, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("This Command Work Only in group\n\nTry it in your own group")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return
    else:
        pass
    if len(message.command) == 1:
        return await message.reply("<b>Give me a rules link along with this command\n\nCommand Usage: /set_rules your rules link</b>")
    elif len(message.command) == 2:
        reply = await message.reply_text("<b>Please Wait...</b>")
        rules = message.command[1]
        await save_group_settings(grpid, 'rules', rules)
        await reply.edit_text(f"<b>Successfully Added rules\n\nHere is your rules link for your group {title} - <code>{rules}</code></b>")
    else:
        return await message.reply("<b>You entered Incorrect Format\n\nFormat: /set_rules your rules link</b>")

@Client.on_message(filters.command('get_rules'))
async def get_rules_link(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    settings = await get_settings(grp_id)
    rules = settings["rules"]
    await message.reply_text(f"<b>rules for {title}\n\nYour rules Link :- {rules}</b>")

@Client.on_message(filters.command("set_share"))
async def set_share(bot, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("This Command Work Only in group\n\nTry it in your own group")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return
    else:
        pass
    if len(message.command) == 1:
        return await message.reply("<b>Give me a share link along with this command\n\nCommand Usage: /set_share your share link</b>")
    elif len(message.command) == 2:
        reply = await message.reply_text("<b>Please Wait...</b>")
        share = message.command[1]
        await save_group_settings(grpid, 'share', share)
        await reply.edit_text(f"<b>Successfully Added share\n\nHere is your share link for your group {title} - <code>{share}</code></b>")
    else:
        return await message.reply("<b>You entered Incorrect Format\n\nFormat: /set_share your share link</b>")

@Client.on_message(filters.command('get_share'))
async def get_share_link(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    settings = await get_settings(grp_id)
    share = settings["share"]
    await message.reply_text(f"<b>share for {title}\n\nYour share Link :- {share}</b>")

@Client.on_message(filters.command("set_admin"))
async def set_admin(bot, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("This Command Work Only in group\n\nTry it in your own group")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return
    else:
        pass
    if len(message.command) == 1:
        return await message.reply("<b>Give me a admin link along with this command\n\nCommand Usage: /set_admin your admin link</b>")
    elif len(message.command) == 2:
        reply = await message.reply_text("<b>Please Wait...</b>")
        admin = message.command[1]
        await save_group_settings(grpid, 'admin', admin)
        await reply.edit_text(f"<b>Successfully Added admin\n\nHere is your admin link for your group {title} - <code>{admin}</code></b>")
    else:
        return await message.reply("<b>You entered Incorrect Format\n\nFormat: /set_admin your admin link</b>")

@Client.on_message(filters.command('get_admin'))
async def get_admin_link(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    settings = await get_settings(grp_id)
    admin = settings["admin"]
    await message.reply_text(f"<b>admin for {title}\n\nYour admin Link :- {admin}</b>")

static_data_filter = filters.create(lambda _, __, query: query.data == "onUnMuteRequest")
@Client.on_callback_query(static_data_filter)
async def _onUnMuteRequest(client, cb):
  user_id = cb.from_user.id
  chat_id = cb.message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    channel = chat_db.channel
    chat_member = await client.get_chat_member(chat_id, user_id)
    if chat_member.restricted_by:
      if chat_member.restricted_by.id == (await client.get_me()).id:
          try:
            await client.get_chat_member(channel, user_id)
            await client.unban_chat_member(chat_id, user_id)
            if cb.message.reply_to_message.from_user.id == user_id:
              await cb.message.delete()
          except UserNotParticipant:
            await client.answer_callback_query(cb.id, text="⚠️ Join our 'Channel' and press the '✅ UnMute Me' button again.", show_alert=True)
      else:
        await client.answer_callback_query(cb.id, text="❗ You are muted by admins for other reasons.", show_alert=True)
    else:
      if not (await client.get_chat_member(chat_id, (await client.get_me()).id)).status == 'administrator':
        await client.send_message(chat_id, f"❗ **{cb.from_user.mention} is trying to UnMute himself but i can't unmute him because i am not an admin in this chat add me as admin again.**\n__#Leaving this chat...__")
        await client.leave_chat(chat_id)
      else:
        await client.answer_callback_query(cb.id, text="⚠️ Warning: Don't click the button if you can speak freely.", show_alert=True)

@Client.on_message((filters.text | filters.media) & ~filters.private, group=1)
async def _check_member(client, message):
  chat_id = message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    user_id = message.from_user.id
    if not (await client.get_chat_member(chat_id, user_id)).status in ("administrator", "creator") and not user_id in OWNER:
      channel = chat_db.channel
      if channel.startswith("-"):
          channel_url = await client.export_chat_invite_link(int(channel))
      else:
          channel_url = f"https://t.me/{channel}"
      try:
        await client.get_chat_member(channel, user_id)
      except UserNotParticipant:
        try:
          sent_message = await message.reply_text(
              " {}\n\nYou haven't joined Our Channel.\nPlease join using below button and press the UnMute Me button to unmute yourself.".format(message.from_user.mention, channel, channel),
              disable_web_page_preview=True,
             reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⚠️ Join Our Channel", url=channel_url)
                ],
                [
                    InlineKeyboardButton("✅ UnMute Me", callback_data="onUnMuteRequest")
                ]
            ]
        )
          )
          await client.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False))
        except ChatAdminRequired:
          await sent_message.edit("❗ **I am not an admin here.**\n__Make me admin with ban user permission and add me again.\n#Leaving this chat...__")
          await client.leave_chat(chat_id)
      except ChatAdminRequired:
        await client.send_message(chat_id, text=f"❗ **I am not an admin in [channel]({channel_url})**\n__Make me admin in the channel and add me again.\n#Leaving this chat...__")
        await client.leave_chat(chat_id)

@Client.on_message(filters.command(["get_fsub", "set_fsub"]) & ~filters.private)
async def config(client, message):
  user = await client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status == "creator" or user.user.id in OWNER:
    chat_id = message.chat.id
    if len(message.command) > 1:
      input_str = message.command[1]
      input_str = input_str.replace("@", "")
      if input_str.lower() in ("off", "no", "disable"):
        sql.disapprove(chat_id)
        await message.reply_text("❌ **Force Subscribe is Disabled Successfully.\nYou Can Set Force Subscribers to /set_fsub {channel id} or {channel link}**")
      elif input_str.lower() in ('clear'):
        sent_message = await message.reply_text('**Unmuting all members who are muted by me...**')
        try:
          for chat_member in (await client.get_chat_members(message.chat.id, filter="restricted")):
            if chat_member.restricted_by.id == (await client.get_me()).id:
                await client.unban_chat_member(chat_id, chat_member.user.id)
                time.sleep(1)
          await sent_message.edit('✅ **UnMuted all members who are muted by me.**')
        except ChatAdminRequired:
          await sent_message.edit('❗ **I am not an admin in this chat.**\n__I can\'t unmute members because i am not an admin in this chat make me admin with ban user permission.__')
      else:
        try:
          await client.get_chat_member(input_str, "me")
          sql.add_channel(chat_id, input_str)
          if input_str.startswith("-"):
              channel_url = await client.export_chat_invite_link(int(input_str))
          else:
              channel_url = f"https://t.me/{input_str}"
          await message.reply_text(f"✅ **Force Subscribe is Enabled**\n__Force Subscribe is enabled, all the group members have to subscribe this [channel]({channel_url}) in order to send messages in this group.__", disable_web_page_preview=True)
        except UserNotParticipant:
          await message.reply_text(f"❗ **Not an Admin in the Channel**\n__I am not an admin in the [channel]({channel_url}). Add me as a admin in order to enable ForceSubscribe.__", disable_web_page_preview=True)
        except (UsernameNotOccupied, PeerIdInvalid):
          await message.reply_text(f"❗ **Invalid Channel Username/ID.**")
        except Exception as err:
          await message.reply_text(f"❗ **ERROR:** ```{err}```")
    else:
      if sql.fs_settings(chat_id):
        my_channel = sql.fs_settings(chat_id).channel
        if my_channel.startswith("-"):
            channel_url = await client.export_chat_invite_link(int(input_str))
        else:
            channel_url = f"https://t.me/{my_channel}"
        await message.reply_text(f"✅ **Force Subscribe is enabled in this chat.**\n__For this [Channel]({channel_url})__", disable_web_page_preview=True)
      else:
        await message.reply_text("❌ **Force Subscribe is disabled in this chat.**")
  else:
      await message.reply_text("❗ **Group Creator Required**\n__You have to be the group creator to do that.__")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
    "content-type": "application/json",
}

#Pastebins
async def p_paste(message, extension=None):
    siteurl = "https://pasty.lus.pm/api/v1/pastes"
    data = {"content": message}
    try:
        response = requests.post(url=siteurl, data=json.dumps(data), headers=headers)
    except Exception as e:
        return {"error": str(e)}
    if response.ok:
        response = response.json()
        purl = (
            f"https://pasty.lus.pm/{response['id']}.{extension}"
            if extension
            else f"https://pasty.lus.pm/{response['id']}.txt"
        )
        return {
            "url": purl,
            "raw": f"https://pasty.lus.pm/{response['id']}/raw",
            "bin": "Pasty",
        }
    return {"error": "Unable to reach pasty.lus.pm"}

@Client.on_message(filters.command(["tgpaste", "pasty", "paste"]))
async def pasty(client, message):
    pablo = await message.reply_text("`Please wait...`")
    tex_t = message.text
    if ' ' in message.text:
        message_s = message.text.split(" ", 1)[1]
    elif message.reply_to_message:
        message_s = message.reply_to_message.text
    else:
        await message.reply("sorry no in put. please repy to a text or /paste with text")
    if not tex_t:
        if not message.reply_to_message:
            await pablo.edit("`Only text and documents are supported.`")
            return
        if not message.reply_to_message.text:
            file = await message.reply_to_message.download()
            m_list = open(file, "r").read()
            message_s = m_list
            os.remove(file)
        elif message.reply_to_message.text:
            message_s = message.reply_to_message.text

    ext = "py"
    x = await p_paste(message_s, ext)
    p_link = x["url"]
    p_raw = x["raw"]

    pasted = f"**Successfully Paste to Pasty**\n\n**Link:** • [Click here]({p_link})\n\n**Raw Link:** • [Click here]({p_raw})"
    await pablo.edit(pasted, disable_web_page_preview=True)

@Client.on_message(filters.command("paste1"))
async def paste_func(_, message: Message):
    if not message.reply_to_message:
        return await eor(message, text="Reply To A Message With /paste")
    r = message.reply_to_message

    if not r.text and not r.document:
        return await eor(
            message, text="Only text and documents are supported."
        )

    m = await eor(message, text="Pasting...")

    if r.text:
        content = str(r.text)
    elif r.document:
        if r.document.file_size > 40000:
            return await m.edit("You can only paste files smaller than 40KB.")

        if not pattern.search(r.document.mime_type):
            return await m.edit("Only text files can be pasted.")

        doc = await message.reply_to_message.download()

        async with aiofiles.open(doc, mode="r") as f:
            content = await f.read()

        os.remove(doc)

    link = await paste(content)
    kb = ikb({"Paste Link": link})
    try:
        if m.from_user.is_bot:
            await message.reply_photo(
                photo=link,
                quote=False,
                reply_markup=kb,
            )
        else:
            await message.reply_photo(
                photo=link,
                quote=False,
                caption=f"**Paste Link:** [Here]({link})",
            )
        await m.delete()
    except Exception:
        await m.edit("Here's your paste", reply_markup=kb)
	
@Client.on_message((filters.command(["request", "Request"]) | filters.regex("#request") | filters.regex("#Request")) & filters.group)
async def requests(bot, message):
    if REQST_CHANNEL is None or SUPPORT_CHAT_ID is None: return # Must add REQST_CHANNEL and SUPPORT_CHAT_ID to use this feature
    if message.reply_to_message and SUPPORT_CHAT_ID == message.chat.id:
        chat_id = message.chat.id
        reporter = str(message.from_user.id)
        mention = message.from_user.mention
        success = True
        content = message.reply_to_message.text
        try:
            if REQST_CHANNEL is not None:
                btn = [[
                        InlineKeyboardButton('View Request', url=f"{message.reply_to_message.link}"),
                        InlineKeyboardButton('Show Options', callback_data=f'show_option#{reporter}')
                      ]]
                reported_post = await bot.send_message(chat_id=REQST_CHANNEL, text=f"<b>𝖱𝖾𝗉𝗈𝗋𝗍𝖾𝗋 : {mention} ({reporter})\n\n𝖬𝖾𝗌𝗌𝖺𝗀𝖾 : {content}</b>", reply_markup=InlineKeyboardMarkup(btn))
                success = True
            elif len(content) >= 3:
                for admin in ADMINS:
                    btn = [[
                        InlineKeyboardButton('View Request', url=f"{message.reply_to_message.link}"),
                        InlineKeyboardButton('Show Options', callback_data=f'show_option#{reporter}')
                      ]]
                    reported_post = await bot.send_message(chat_id=admin, text=f"<b>𝖱𝖾𝗉𝗈𝗋𝗍𝖾𝗋 : {mention} ({reporter})\n\n𝖬𝖾𝗌𝗌𝖺𝗀𝖾 : {content}</b>", reply_markup=InlineKeyboardMarkup(btn))
                    success = True
            else:
                if len(content) < 3:
                    await message.reply_text("<b>You must type about your request [Minimum 3 Characters]. Requests can't be empty.</b>")
            if len(content) < 3:
                success = False
        except Exception as e:
            await message.reply_text(f"Error: {e}")
            pass
        
    elif SUPPORT_CHAT_ID == message.chat.id:
        chat_id = message.chat.id
        reporter = str(message.from_user.id)
        mention = message.from_user.mention
        success = True
        content = message.text
        keywords = ["#request", "/request", "#Request", "/Request"]
        for keyword in keywords:
            if keyword in content:
                content = content.replace(keyword, "")
        try:
            if REQST_CHANNEL is not None and len(content) >= 3:
                btn = [[
                        InlineKeyboardButton('View Request', url=f"{message.link}"),
                        InlineKeyboardButton('Show Options', callback_data=f'show_option#{reporter}')
                      ]]
                reported_post = await bot.send_message(chat_id=REQST_CHANNEL, text=f"<b>𝖱𝖾𝗉𝗈𝗋𝗍𝖾𝗋 : {mention} ({reporter})\n\n𝖬𝖾𝗌𝗌𝖺𝗀𝖾 : {content}</b>", reply_markup=InlineKeyboardMarkup(btn))
                success = True
            elif len(content) >= 3:
                for admin in ADMINS:
                    btn = [[
                        InlineKeyboardButton('View Request', url=f"{message.link}"),
                        InlineKeyboardButton('Show Options', callback_data=f'show_option#{reporter}')
                      ]]
                    reported_post = await bot.send_message(chat_id=admin, text=f"<b>𝖱𝖾𝗉𝗈𝗋𝗍𝖾𝗋 : {mention} ({reporter})\n\n𝖬𝖾𝗌𝗌𝖺𝗀𝖾 : {content}</b>", reply_markup=InlineKeyboardMarkup(btn))
                    success = True
            else:
                if len(content) < 3:
                    await message.reply_text("<b>You must type about your request [Minimum 3 Characters]. Requests can't be empty.</b>")
            if len(content) < 3:
                success = False
        except Exception as e:
            await message.reply_text(f"Error: {e}")
            pass

    else:
        success = False
    
    if success:
        '''if isinstance(REQST_CHANNEL, (int, str)):
            channels = [REQST_CHANNEL]
        elif isinstance(REQST_CHANNEL, list):
            channels = REQST_CHANNEL
        for channel in channels:
            chat = await bot.get_chat(channel)
        #chat = int(chat)'''
        link = await bot.create_chat_invite_link(int(REQST_CHANNEL))
        btn = [[
                InlineKeyboardButton('Join Channel', url=link.invite_link),
                InlineKeyboardButton('View Request', url=f"{reported_post.link}")
              ]]
        await message.reply_text("<b>Your request has been added! Please wait for some time.\n\nJoin Channel First & View Request</b>", reply_markup=InlineKeyboardMarkup(btn))

@Client.on_message(filters.command("send") & filters.user(ADMINS))
async def send_msg(bot, message):
    if message.reply_to_message:
        target_id = message.text.split(" ", 1)[1]
        out = "Users Saved In DB Are:\n\n"
        success = False
        try:
            user = await bot.get_users(target_id)
            users = await db.get_all_users()
            async for usr in users:
                out += f"{usr['id']}"
                out += '\n'
            if str(user.id) in str(out):
                await message.reply_to_message.copy(int(user.id))
                success = True
            else:
                success = False
            if success:
                await message.reply_text(f"<b>Your Message has Been Successfully Send to {user.mention}.</b>")
            else:
                await message.reply_text("<b>This User Didn't Started This Bot Yet !</b>")
        except Exception as e:
            await message.reply_text(f"<b>Error :- {e}</b>")
    else:
        await message.reply_text("<b>Use This Command as a Reply to any Message Using the Target Chat ID. For Example :- /send userid</b>")

@Client.on_message(filters.command("deletefiles") & filters.user(ADMINS))
async def deletemultiplefiles(bot, message):
    chat_type = message.chat.type
    if chat_type != enums.ChatType.PRIVATE:
        return await message.reply_text(f"<b>Hello 👋🏻 {message.from_user.mention} ❤️, This command Won't Work in Groups. It Will only Works on My PM !</b>")
    else:
        pass
    try:
        keyword = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text(f"<b>Hey {message.from_user.mention}, Give me a keyword along with the command to delete files.</b>")
    k = await bot.send_message(chat_id=message.chat.id, text=f"<b>Fetching Files for Your Query {keyword} on DB... Please wait...</b>")
    files, next_offset, total = await get_bad_files(keyword)
    await k.edit_text(f"<b>Found {total} Files for Your Query {keyword} !\n\nFile Deletion Process will start in 5 Seconds !</b>")
    await asyncio.sleep(5)
    deleted = 0
    for file in files:
        await k.edit_text(f"<b>Process Started for Deleting Files From DB. Successfully Deleted {str(deleted)} Files From DB for Your Query {keyword} !\n\nPlease wait...</b>")
        file_ids = file.file_id
        file_name = file.file_name
        result = await Media.collection.delete_one({
            '_id': file_ids,
        })
        if result.deleted_count:
            logger.info(f'File Found for Your Query {keyword}! Successfully Deleted {file_name} from Database.')
        deleted += 1
    await k.edit_text(text=f"<b>Process Completed for File Deletion !\n\nSuccessfully Deleted {str(deleted)} Files from Database for your Query {keyword}.</b>")

@Client.on_message(filters.command("send") & filters.user(ADMINS))
async def send_msg(bot, message):
    if message.reply_to_message:
        target_id = message.text.split(" ", 1)[1]
        out = "Users Saved In DB Are:\n\n"
        success = False
        try:
            user = await bot.get_users(target_id)
            users = await db.get_all_users()
            async for usr in users:
                out += f"{usr['id']}"
                out += '\n'
            if str(user.id) in str(out):
                await message.reply_to_message.copy(int(user.id))
                success = True
            else:
                success = False
            if success:
                await message.reply_text(f"<b>Your message has been successfully send to {user.mention}.</b>")
            else:
                await message.reply_text("<b>This user didn't started this bot yet !</b>")
        except Exception as e:
            await message.reply_text(f"<b>Error: {e}</b>")
    else:
        await message.reply_text("<b>Use this command as a reply to any message using the target chat id. For eg: /send userid</b>")

@Client.on_message(filters.command("group_send") & filters.user(ADMINS))
async def send_chatmsg(bot, message):
    if message.reply_to_message:
        target_id = message.text.split(" ", 1)[1]
        out = "Chats Saved In DB Are:\n\n"
        success = False
        try:
            chat = await bot.get_chat(target_id)
            chats = await db.get_all_chats()
            async for cht in chats:
                out += f"{cht['id']}"
                out += '\n'
            if str(chat.id) in str(out):
                await message.reply_to_message.copy(int(chat.id))
                success = True
            else:
                success = False
            if success:
                await message.reply_text(f"<b>Your message has been successfully send to <code>{chat.id}</code>.</b>")
            else:
                await message.reply_text("<b>An Error Occured !</b>")
        except Exception as e:
            await message.reply_text(f"<b>Error :- <code>{e}</code></b>")
    else:
        await message.reply_text("<b>Error𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖨𝗇𝖼𝗈𝗆𝗉𝗅𝖾𝗍𝖾 !</b>")

@Client.on_message(filters.command("deletefiles") & filters.user(ADMINS))
async def deletemultiplefiles(bot, message):
    chat_type = message.chat.type
    if chat_type != enums.ChatType.PRIVATE:
        return await message.reply_text(f"<b>Hey {message.from_user.mention}, This command won't work in groups. It only works on my PM !</b>")
    else:
        pass
    try:
        keyword = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text(f"<b>Hey {message.from_user.mention}, Give me a keyword along with the command to delete files.</b>")
    btn = [[
       InlineKeyboardButton("Yes, Continue !", callback_data=f"killfilesdq#{keyword}")
       ],[
       InlineKeyboardButton("No, Abort operation !", callback_data="close_data")
    ]]
    await message.reply_text(
        text="<b>Are you sure? Do you want to continue?\n\nNote:- This could be a destructive action !</b>",
        reply_markup=InlineKeyboardMarkup(btn),
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.command("graph") & filters.private)
async def telegraph_upload(bot, update):
    replied = update.reply_to_message
    if not replied:
        await update.reply_text("**Reply to a Photo or Video Under 5MB.**")
        return
    file_info = get_file_id(replied)
    if not file_info:
        await update.reply_text("**Not Supported Media!**")
        return
    text = await update.reply_text(text="<b>Downloading to My Server ...</b>", disable_web_page_preview=True)   
    media = await update.reply_to_message.download()   
    await text.edit_text(text="<b>Downloading Completed. Now I am Uploading to graph.org Link...</b>", disable_web_page_preview=True)                                            
    try:
        response = upload_file(media)
    except Exception as error:
        print(error)
        await text.edit_text(text=f"**Error :- {error}**", disable_web_page_preview=True)       
        return    
    try:
        os.remove(media)
    except Exception as error:
        print(error)
        return    
    await text.edit_text(
        text=f"<b>Your Photo or Video Link :-</b>\n\n<b>https://graph.org{response[0]}</b>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton(text="Open Link", url=f"https://graph.org{response[0]}"),
            InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url=https://graph.org{response[0]}")
            ],[
            InlineKeyboardButton(text="✗ Close ✗", callback_data="close")
            ]])
        )
	
@Client.on_message(filters.command("purge") & (filters.group | filters.channel))                   
async def purge(client, message):
    if message.chat.type not in ((enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL)):
        return
    is_admin = await admin_check(message)
    if not is_admin:
        return

    status_message = await message.reply_text("**Processing...**", quote=True)
    await message.delete()
    message_ids = []
    count_del_etion_s = 0

    if message.reply_to_message:
        for a_s_message_id in range(message.reply_to_message.id, message.id):
            message_ids.append(a_s_message_id)
            if len(message_ids) == "100":
                await client.delete_messages(
                    chat_id=message.chat.id,
                    message_ids=message_ids,
                    revoke=True
                )
                count_del_etion_s += len(message_ids)
                message_ids = []
        if len(message_ids) > 0:
            await client.delete_messages(
                chat_id=message.chat.id,
                message_ids=message_ids,
                revoke=True
            )
            count_del_etion_s += len(message_ids)
    await status_message.edit_text(f"**Deleted {count_del_etion_s} Messages**")
    await asyncio.sleep(5)
    await status_message.delete()

# Group Manage

@Client.on_message(filters.command("ban"))
async def ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return 
    user_id, user_first_name = extract_user(message)
    try:
        await message.chat.ban_member(user_id=user_id)
    except Exception as error:
        await message.reply_text(str(error))                    
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(f"**Someone else is dusting off..! \n{user_first_name} \nIs forbidden.**")                              
        else:
            await message.reply_text(f"**Someone else is dusting off..! \n<a href='tg://user?id={user_id}'>{user_first_name}</a> Is forbidden**")                      
            

@Client.on_message(filters.command("tban"))
async def temp_ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return
    if not len(message.command) > 1:
        return
    user_id, user_first_name = extract_user(message)
    until_date_val = extract_time(message.command[1])
    if until_date_val is None:
        return await message.reply_text(text=f"**Invalid time type specified. \nExpected m, h, or d, Got it: {message.command[1][-1]}**")   
    try:
        await message.chat.ban_member(user_id=user_id, until_date=until_date_val)            
    except Exception as error:
        await message.reply_text(str(error))
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(f"**Someone else is dusting off..!\n{user_first_name}\nbanned for {message.command[1]}!**")
        else:
            await message.reply_text(f"**Someone else is dusting off..!\n<a href='tg://user?id={user_id}'>Lavane</a>\n banned for {message.command[1]}!**")
@Client.on_message(filters.group & filters.command('inkick'))
def inkick(client, message):
  user = client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
    if len(message.command) > 1:
      input_str = message.command
      sent_message = message.reply_text(script.START_KICK)
      sleep(20)
      sent_message.delete()
      message.delete()
      count = 0
      for member in client.get_chat_members(message.chat.id):
        if member.user.status in input_str and not member.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
          try:
            client.ban_chat_member(message.chat.id, member.user.id, int(time() + 45))
            count += 1
            sleep(1)
          except (ChatAdminRequired, UserAdminInvalid):
            sent_message.edit(script.ADMIN_REQUIRED)
            client.leave_chat(message.chat.id)
            break
          except FloodWait as e:
            sleep(e.x)
      try:
        sent_message.edit(script.KICKED.format(count))
      except ChatWriteForbidden:
        pass
    else:
      message.reply_text(script.INPUT_REQUIRED)
  else:
    sent_message = message.reply_text(script.CREATOR_REQUIRED)
    sleep(5)
    sent_message.delete()
    message.delete()


@Client.on_message(filters.group & filters.command('dkick'))
def dkick(client, message):
  user = client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
    sent_message = message.reply_text(script.START_KICK)
    sleep(20)
    sent_message.delete()
    message.delete()
    count = 0
    for member in client.get_chat_members(message.chat.id):
      if member.user.is_deleted and not member.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        try:
          client.ban_chat_member(message.chat.id, member.user.id, int(time() + 45))
          count += 1
          sleep(1)
        except (ChatAdminRequired, UserAdminInvalid):
          sent_message.edit(script.ADMIN_REQUIRED)
          client.leave_chat(message.chat.id)
          break
        except FloodWait as e:
          sleep(e.x)
    try:
      sent_message.edit(script.DKICK.format(count))
    except ChatWriteForbidden:
      pass
  else:
    sent_message = message.reply_text(script.CREATOR_REQUIRED)
    sleep(5)
    sent_message.delete()
    message.delete()

  
@Client.on_message((filters.channel | filters.group) & filters.command('instatus'))
def instatus(client, message):
    sent_message = message.reply_text("**Processing...**")
    recently = 0
    within_week = 0
    within_month = 0
    long_time_ago = 0
    deleted_acc = 0
    uncached = 0
    bot = 0
    for member in client.get_chat_members(message.chat.id, limit=int(10000)):
      user = member.user
      if user.is_deleted:
        deleted_acc += 1
      elif user.is_bot:
        bot += 1
      elif user.status == enums.UserStatus.RECENTLY:
        recently += 1
      elif user.status == enums.UserStatus.LAST_WEEK:
        within_week += 1
      elif user.status == enums.UserStatus.LAST_MONTH:
        within_month += 1
      elif user.status == enums.UserStatus.LONG_AGO:
        long_time_ago += 1
      else:
        uncached += 1

    chat_type = message.chat.type
    if chat_type == enums.ChatType.CHANNEL:
         sent_message.edit(f"**{message.chat.title}\nChat Member Status\n\nRecently - {recently}\nWithin Week - {within_week}\nWithin Month - {within_month}\nLong Time Ago - {long_time_ago}\n\nDeleted Account - {deleted_acc}\nBot - {bot}\nUnCached - {uncached}**")            
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        user = client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER, ADMINS):
            sent_message.edit(f"**{message.chat.title}\nChat Member Status\n\nRecently - {recently}\nWithin Week - {within_week}\nWithin Month - {within_month}\nLong Time Ago - {long_time_ago}\n\nDeleted Account - {deleted_acc}\nBot - {bot}\nUnCached - {uncached}**")
        else:
            sent_message.edit("**you are not administrator in this chat**")
	
@Client.on_message(filters.command("mute"))
async def mute_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return
    user_id, user_first_name = extract_user(message)
    try:
        await message.chat.restrict_member(
            user_id=user_id,
            permissions=ChatPermissions(
            )
        )
    except Exception as error:
        await message.reply_text(
            str(error)
        )
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "👍🏻 "
                f"**{user_first_name}**"
                "** Lavender's mouth is shut! **🤐"
            )
        else:
            await message.reply_text(
                "**👍🏻 **"
                f"**<a href='tg://user?id={user_id}'>**"
                "**Of lavender**"
                "**</a>**"
                "** The mouth is closed! 🤐**"
            )


@Client.on_message(filters.command("tmute"))
async def temp_mute_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return

    if not len(message.command) > 1:
        return

    user_id, user_first_name = extract_user(message)

    until_date_val = extract_time(message.command[1])
    if until_date_val is None:
        await message.reply_text(
            (
                "**Invalid time type specified. **"
                "**Expected m, h, or d, Got it: {}**"
            ).format(
                message.command[1][-1]
            )
        )
        return

    try:
        await message.chat.restrict_member(
            user_id=user_id,
            permissions=ChatPermissions(
            ),
            until_date=until_date_val
        )
    except Exception as error:
        await message.reply_text(
            str(error)
        )
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "**Be quiet for a while! 😠**"
                f"**{user_first_name}**"
                f"** muted for {message.command[1]}!**"
            )
        else:
            await message.reply_text(
                "**Be quiet for a while! 😠**"
                f"**<a href='tg://user?id={user_id}'>**"
                "**Of lavender**"
                "**</a>**"
                " **Mouth** "
                f"**muted for {message.command[1]}!**"
            )
	
@Client.on_message(filters.command("pin") & admin_fliter)
async def pin(_, message: Message):
    if not message.reply_to_message:
        return
    await message.reply_to_message.pin()


@Client.on_message(filters.command("unpin") & admin_fliter)             
async def unpin(_, message: Message):
    if not message.reply_to_message:
        return
    await message.reply_to_message.unpin()
	
@Client.on_message(filters.command(["unban", "unmute"]))
async def un_ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return
    user_id, user_first_name = extract_user(message)
    try:
        await message.chat.unban_member(user_id=user_id)
    except Exception as error:
        await message.reply_text(str(error))
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "**Okay, changed ... now **"
                f"**{user_first_name} To **"
                "** You can join the group!**"
            )
        else:
            await message.reply_text(
                "**Okay, changed ... now **"
                f"**<a href='tg://user?id={user_id}'>**"
                f"**{user_first_name}**"
                "**</a> To **"
                "** You can join the group!**"
            )	
	
@Client.on_message(filters.command("json"))
async def jsonify(_, message):
    the_real_message = None
    reply_to_id = None
    pk = InlineKeyboardMarkup([[InlineKeyboardButton(text="Star Bots Tamil", url="https://t.me/Star_Bots_Tamil")],[InlineKeyboardButton(text="🚫 Close", callback_data="close_data")]])  
                
    if message.reply_to_message:
        the_real_message = message.reply_to_message
    else:
        the_real_message = message

    try:        
        await message.reply_text(f"<code>{the_real_message}</code>", reply_markup=pk, quote=True)
    except Exception as e:
        with open("json.text", "w+", encoding="utf8") as out_file:
            out_file.write(str(the_real_message))       
        await message.reply_document(
            document="json.text",
            caption=str(e),
            disable_notification=True,
            quote=True,
            reply_markup=reply_markup
        )            
        os.remove("json.text")
	
@Client.on_message(filters.command("ping"))
async def ping(_, message):
    start_t = time.time()
    rm = await message.reply_text("**Processing...**")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"**Ping!\n{time_taken_s:.3f} ms**")
	
	
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
    "content-type": "application/json",
}

#Pastebins
async def p_paste(message, extension=None):
    siteurl = "https://pasty.lus.pm/api/v1/pastes"
    data = {"content": message}
    try:
        response = requests.post(url=siteurl, data=json.dumps(data), headers=headers)
    except Exception as e:
        return {"error": str(e)}
    if response.ok:
        response = response.json()
        purl = (
            f"https://pasty.lus.pm/{response['id']}.{extension}"
            if extension
            else f"https://pasty.lus.pm/{response['id']}.txt"
        )
        return {
            "url": purl,
            "raw": f"https://pasty.lus.pm/{response['id']}/raw",
            "bin": "Pasty",
        }
    return {"error": "Unable to reach pasty.lus.pm"}


@Client.on_message(filters.command(["tgpaste", "pasty", "paste"]))
async def pasty(client, message):
    pablo = await message.reply_text("**Please wait...**")
    tex_t = message.text
    if ' ' in message.text:
        message_s = message.text.split(" ", 1)[1]
    elif message.reply_to_message:
        message_s = message.reply_to_message.text
    else:
        await message.reply("**sorry no in put. please repy to a text or /paste with text**")
    if not tex_t:
        if not message.reply_to_message:
            await pablo.edit("**Only text and documents are supported.**")
            return
        if not message.reply_to_message.text:
            file = await message.reply_to_message.download()
            m_list = open(file, "r").read()
            message_s = m_list
            os.remove(file)
        elif message.reply_to_message.text:
            message_s = message.reply_to_message.text

    ext = "py"
    x = await p_paste(message_s, ext)
    p_link = x["url"]
    p_raw = x["raw"]

    pasted = f"**Successfully Paste to Pasty\n\nLink :- • [Click here]({p_link})\n\nRaw Link :- • [Click here]({p_raw}**)"
    await pablo.edit(pasted, disable_web_page_preview=True)	

@Client.on_message(filters.command("share"))
async def share_text(client, message):
    reply = message.reply_to_message
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    input_split = message.text.split(None, 1)
    if len(input_split) == 2:
        input_text = input_split[1]
    elif reply and (reply.text or reply.caption):
        input_text = reply.text or reply.caption
    else:
        await message.reply_text(
            text=f"**Notice :-\n\n1. Reply Any Messages.\n2. No Media Support\n\nAny Question Join Support Chat**",                
            reply_to_message_id=reply_id,
            quote=True,               
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👥 Support Chat", url=f"https://t.me/Star_Bots_Tamil_Support0")]])
            )                                                   
        return
    await message.reply_text(
        text=f"**Here is Your Sharing Text 👇\n\nhttps://telegram.me/share/url?url={quote(input_text)}**",
        reply_to_message_id=reply_id,
        quote=True,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("♂️ Share", url=f"https://telegram.me/share/url?url={quote(input_text)}")]])       
    )    

@Client.on_message(filters.command('status'))
async def bot_status(client,message):
    if HEROKU_API_KEY:
        try:
            server = heroku3.from_key(HEROKU_API_KEY)

            user_agent = (
                'Mozilla/5.0 (Linux; Android 10; SM-G975F) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/80.0.3987.149 Mobile Safari/537.36'
            )
            accountid = server.account().id
            headers = {
            'User-Agent': user_agent,
            'Authorization': f'Bearer {HEROKU_API_KEY}',
            'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
            }

            path = "/accounts/" + accountid + "/actions/get-quota"

            request = requests.get("https://api.heroku.com" + path, headers=headers)

            if request.status_code == 200:
                result = request.json()

                total_quota = result['account_quota']
                quota_used = result['quota_used']

                quota_left = total_quota - quota_used
                
                total = math.floor(total_quota/3600)
                used = math.floor(quota_used/3600)
                hours = math.floor(quota_left/3600)
                minutes = math.floor(quota_left/60 % 60)
                days = math.floor(hours/24)

                usedperc = math.floor(quota_used / total_quota * 100)
                leftperc = math.floor(quota_left / total_quota * 100)

                quota_details = f"""
**Heroku Account Status 📊
➪ You Have {total} Hours of Free Dyno Quota Available Each Month.
➪ Dyno Hours Used This Month :-
        • {used} 𝖧𝗈𝗎𝗋𝗌 ( {usedperc}% )
➪ Dyno Hours Remaining This Month :-
        • {hours} Hours ( {leftperc}% )
        • Approximately {days} Days!**"""
            else:
                quota_details = ""
        except:
            print("Check your Heroku API key")
            quota_details = ""
    else:
        quota_details = ""

    uptime = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - BOT_START_TIME))

    try:
        t, u, f = shutil.disk_usage(".")
        total = humanbytes(t)
        used = humanbytes(u)
        free = humanbytes(f)

        disk = "\n**Disk Details**\n\n" \
            f"> USED  :  {used} / {total}\n" \
            f"> FREE  :  {free}\n\n"
    except:
        disk = ""

    await message.reply_text(
        "**Current Status 📊 of Our Bot**\n\n"
        "**DB Status**\n"
        f"**➪ 𝖡𝗈𝗍 𝖴𝗉𝗍𝗂𝗆𝖾: {uptime}**\n"
        f"**{quota_details}**"
        f"**{disk}**",
        quote=True,
        parse_mode=enums.ParseMode.MARKDOWN
    )

@Client.on_message(filters.command("restart") & filters.user(ADMINS))
async def stop_button(bot, message):
    msg = await bot.send_message(text="**🔄 Bot 🤖 Process is Stopped. Bot is Restarting...**", chat_id=message.chat.id)       
    await asyncio.sleep(3)
    await msg.edit("**✅️ Bot 🤖 is Restarted. Now You Can Use Me 😁**")

    os.execl(sys.executable, sys.executable, *sys.argv)
	
@Client.on_message(filters.command(["stickerid"]))
async def stickerid(bot, message):
    if message.reply_to_message.sticker:
       await message.reply(f"**Sticker ID is**\n`{message.reply_to_message.sticker.file_id}`\n\n**Unique ID is **\n\n`{message.reply_to_message.sticker.file_unique_id}`", quote=True)
    else: 
       await message.reply("<b>Oops !! Not a sticker file</b>")


@Client.on_message(filters.command(["password"]))
async def password(bot, update):
    message = await update.reply_text(text="**Processing...**")
    password = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+".lower()
    if len(update.command) > 1:
        qw = update.text.split(" ", 1)[1]
    else:
        ST = ["5", "7", "6", "9", "10", "12", "14", "8", "13"] 
        qw = random.choice(ST)
    limit = int(qw)
    random_value = "".join(random.sample(password, limit))
    txt = f"<b>Limit:</b> {str(limit)} \n<b>Password:</b>€€ <code>{random_value}</code>"
    btn = InlineKeyboardMarkup([[InlineKeyboardButton('Star Movies Tamil', url='https://t.me/Star_Moviess_Tamil')]])
    await message.edit_text(text=txt, reply_markup=btn, parse_mode=enums.ParseMode.HTML)

@Client.on_message(filters.command("alive"))
async def check_alive(_, message):
    await message.reply_text("**Hello 👋🏻 Bro /start**")

@Client.on_message(filters.command('song') & filters.private)
async def song(client, message):
    user_id = message.from_user.id 
    user_name = message.from_user.first_name 
    rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = await message.reply(f"**ѕєαrchíng чσur ѕσng...!\n {query}**")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)
        performer = f"[Mᴋɴ Bᴏᴛᴢ™]" 
        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]
    except Exception as e:
        print(str(e))
        return await m.edit("**𝙵𝙾𝚄𝙽𝙳 𝙽𝙾𝚃𝙷𝙸𝙽𝙶 𝙿𝙻𝙴𝙰𝚂𝙴 𝙲𝙾𝚁𝚁𝙴𝙲𝚃 𝚃𝙷𝙴 𝚂𝙿𝙴𝙻𝙻𝙸𝙽𝙶 𝙾𝚁 𝙲𝙷𝙴𝙲𝙺 𝚃𝙷𝙴 𝙻𝙸𝙽𝙺**")
                
    await m.edit("**dσwnlσαdíng чσur ѕσng...!**")
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        cap = "**BY›› [Star Movies Tamil](https://t.me/Star_Moviess_Tamil)**"
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        await message.reply_audio(
            audio_file,
            caption=cap,            
            quote=False,
            title=title,
            duration=dur,
            performer=performer,
            thumb=thumb_name
        )            
        await m.delete()
    except Exception as e:
        await m.edit("**🚫 Error 🚫**")
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
def get_text(message: Message) -> [None,str]:
    text_to_return = message.text
    if message.text is None:
        return None
    if " " not in text_to_return:
        return None
    try:
        return message.text.split(None, 1)[1]
    except IndexError:
        return None

@Client.on_message(filters.command("text2speech"))
async def text_to_speech(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("**Reply to with Any Text.**")
    if not message.reply_to_message.text:
        return await message.reply_text("**Reply to with Any Text.**")
    m = await message.reply_text("**Processing**")
    text = message.reply_to_message.text
    try:
        loop = get_running_loop()
        audio = await loop.run_in_executor(None, convert, text)
        await message.reply_audio(audio)
        await m.delete()
        audio.close()
    except Exception as e:
        await m.edit(e)
        e = traceback.format_exc()
        print(e)


@Client.on_message(filters.command(["translate"]) & filters.private)
async def left(client,message):
	if (message.reply_to_message):
		try:
			lgcd = message.text.split("/translate")
			lg_cd = lgcd[1].lower().replace(" ", "")
			tr_text = message.reply_to_message.text
			translator = Translator()
			translation = translator.translate(tr_text,dest = lg_cd)
			hehek = InlineKeyboardMarkup(
                                [
                                    [
                                        InlineKeyboardButton(
                                            text=f"More Lang Codes", url="https://cloud.google.com/translate/docs/languages"
                                        )
                                    ],
				    [
                                        InlineKeyboardButton(
                                            "🚫 Close", callback_data="close_data"
                                        )
                                    ],
                                ]
                            )
			try:
				for i in list:
					if list[i]==translation.src:
						fromt = i
					if list[i] == translation.dest:
						to = i 
				await message.reply_text(f"Translated from {fromt.capitalize()} To {to.capitalize()}\n\n```{translation.text}``` Join @Star_Bots_Tamil", reply_markup=hehek, quote=True)
			except:
			   	await message.reply_text(f"Translated from **{translation.src}** To **{translation.dest}**\n\n```{translation.text}```Join @Star_Bots_Tamil", reply_markup=hehek, quote=True)
			
		except :
			print("error")
	else:
			 ms = await message.reply_text("You can Use This Command by using reply to message")

@Client.on_message(filters.command(["video"]))
async def vsong(client, message: Message):
    urlissed = get_text(message)
    pablo = await client.send_message(message.chat.id, f"**𝙵𝙸𝙽𝙳𝙸𝙽𝙶 𝚈𝙾𝚄𝚁 𝚅𝙸𝙳𝙴𝙾** `{urlissed}`")
    if not urlissed:
        return await pablo.edit("Invalid Command Syntax Please Check help Menu To Know More!")     
    search = SearchVideos(f"{urlissed}", offset=1, mode="dict", max_results=1)
    mi = search.result()
    mio = mi["search_result"]
    mo = mio[0]["link"]
    thum = mio[0]["title"]
    fridayz = mio[0]["id"]
    mio[0]["channel"]
    kekme = f"https://img.youtube.com/vi/{fridayz}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    url = mo
    sedlyf = wget.download(kekme)
    opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)
    except Exception as e:
        return await pablo.edit_text(f"**𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝙵𝚊𝚒𝚕𝚎𝚍 𝙿𝚕𝚎𝚊𝚜𝚎 𝚃𝚛𝚢 𝙰𝚐𝚊𝚒𝚗..♥️** \n**Error :** `{str(e)}`")       
    
    file_stark = f"{ytdl_data['id']}.mp4"
    capy = f"""**𝚃𝙸𝚃𝙻𝙴 :** [{thum}]({mo})\n**𝚁𝙴𝚀𝚄𝙴𝚂𝚃𝙴𝙳 𝙱𝚈 :** {message.from_user.mention}"""

    await client.send_video(
        message.chat.id,
        video=open(file_stark, "rb"),
        duration=int(ytdl_data["duration"]),
        file_name=str(ytdl_data["title"]),
        thumb=sedlyf,
        caption=capy,
        supports_streaming=True,        
        reply_to_message_id=message.id 
    )
    await pablo.delete()
    for files in (sedlyf, file_stark):
        if files and os.path.exists(files):
            os.remove(files)

@Client.on_message(filters.command(["ytthumb", 'dlthumb']))
async def send_thumbnail(bot, update):
    message = await update.reply_text(
        text="`𝙂𝙚𝙣𝙚𝙧𝙖𝙩𝙞𝙣𝙜 𝙏𝙝𝙪𝙢𝙗𝙣𝙖𝙞𝙡 𝙊𝙛 𝙔𝙤𝙪𝙧 𝙇𝙞𝙣𝙠...`",
        disable_web_page_preview=True,
        quote=True
    )
    try:
        if " | " in update.text:
            video = update.text.split(" | ", -1)[0]
            quality = update.text.split(" | ", -1)[1]
        else:
            video = update.text
            quality = "sd"
        thumbnail = ytthumb.thumbnail(
            video=video,
            quality=quality
        )
        await update.reply_photo(
            photo=thumbnail,
            quote=True
        )
        await message.delete()
    except Exception as error:
        await message.edit_text(
            text="**Please Use** /ytthumb (youtube link)\n\n**Example:** `/ytthumb https://youtu.be/examplelink`",
            disable_web_page_preview=True
	)

BITLY_API = os.environ.get("BITLY_API", "aa2132168583d283fb288625d9352f2c5835512a")
CUTTLY_API = os.environ.get("CUTTLY_API", "bd3a3ab946d7598ee459331dac9e9568e3d66")
EZ4SHORT_API = os.environ.get("EZ4SHORT_API", "e41618d805b3c4256dfa99abde6ef11fc7629c47")
TINYURL_API = os.environ.get("TINYURL_API", "iRkhyhlmfJ07cFVsFV0NpvX6dOWZIwPglbq8jQDuSBMqAEk5Y81BX04ejVQk")
DROPLINK_API = os.environ.get("DROPLINK_API", "1d85e33efc4969b36e0f6c0a017aaaefd8accccc")
TNLINK_API = os.environ.get("TNLINK_API", "d03a53149bf186ac74d58ff80d916f7a79ae5745")
SHAREUS_API = os.environ.get("SHAREUS_API", "IiXFmlsLukgMvDpc3t3FHbLal4u1")

reply_markup = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🎥 Movie Updates', url='https://t.me/Star_Moviess_Tamil')
        ],
        [
        InlineKeyboardButton('🤖 Bot Channel', url=f"https://t.me/Star_Bots_Tamil"),
        ],
        [
        InlineKeyboardButton('⚡ Request', url=f"https://t.me/TG_Karthik"),
        ],
        [
        InlineKeyboardButton('🚫 Close', callback_data='close_data')
        ]]
    )

@Client.on_message(filters.command(["short"]) & filters.regex(r'https?://[^\s]+'))
async def reply_shortens(bot, update):
    message = await update.reply_text(
        text="**Analysing Your Link...**",
        disable_web_page_preview=True,
        reply_markup=reply_markup,
        quote=True
    )
    link = update.matches[0].group(0)
    shorten_urls = await short(link)
    await message.edit_text(
        text=shorten_urls,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )

@Client.on_inline_query(filters.regex(r'https?://[^\s]+'))
async def inline_short(bot, update):
    link = update.matches[0].group(0),
    shorten_urls = await short(link)
    answers = [
        InlineQueryResultArticle(
            title="Short Links",
            description=update.query,
            input_message_content=InputTextMessageContent(
                message_text=shorten_urls,
                disable_web_page_preview=True
            ),
            reply_to_message_id=message.id
        )
    ]
    await bot.answer_inline_query(
        inline_query_id=update.id,
        results=answers
    )

async def short(link):
    shorten_urls = "**--Shortened URLs--**\n"
    
    # Bit.ly Shortener
    if BITLY_API:
        try:
            s = Shortener(api_key=BITLY_API)
            url = s.bitly.short(link)
            shorten_urls += f"\n**Bit.ly :- {url}**\n"
        except Exception as error:
            print(f"Bit.ly Error :- {error}")
        
    # Clck.ru Shortener
    try:
        s = Shortener()
        url = s.clckru.short(link)
        shorten_urls += f"\n**Clck.ru :- {url}**\n"
    except Exception as error:
        print(f"Click.ru Error :- {error}")
    
    # Cutt.ly Shortener
    if CUTTLY_API:
        try:
            s = Shortener(api_key=CUTTLY_API)
            url = s.cuttly.short(link)
            shorten_urls += f"\n**Cutt.ly :- {url}**\n"
        except Exception as error:
            print(f"Cutt.ly Error :- {error}")
    
    # Da.gd Shortener
    try:
        s = Shortener()
        url = s.dagd.short(link)
        shorten_urls += f"\n**Da.gd :- {url}**\n"
    except Exception as error:
        print(f"Da.gd Error :- {error}")
    
    # Is.gd Shortener
    try:
        s = Shortener()
        url = s.isgd.short(link)
        shorten_urls += f"\n**Is.gd :- {url}**\n"
    except Exception as error:
        print(f"Is.gd Error :- {error}")
    
    # Osdb.link Shortener
    try:
        s = Shortener()
        url = s.osdb.short(link)
        shorten_urls += f"\n**Osdb.link :- {url}**\n"
    except Exception as error:
        print(f"Osdb.link Error :- {error}")
                
    # Droplink.co Shortener
    try:
        api_url = "https://droplink.co/api" 
        params = {'api': DROPLINK_API, 'url': link}
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params, raise_for_status=True) as response:
                data = await response.json()
                url = data["shortenedUrl"]
                shorten_urls += f"\n**DropLink.co :- {url}**\n"
    except Exception as error:
        print(f"Droplink.co Error :- {error}")

    # TNLink.in Shortener
    try:
        api_url = "https://tnlink.in/api" 
        params = {'api': TNLINK_API, 'url': link}
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params, raise_for_status=True) as response:
                data = await response.json()
                url = data["shortenedUrl"]
                shorten_urls += f"\n**TNLink.in :- {url}**\n"
    except Exception as error:
        print(f"TNLink.in Error :- {error}")

    # TinyURL.com Shortener
    try:
        s = Shortener(api_key=TINYURL_API)
        url = s.tinyurl.short(link)
        shorten_urls += f"\n**TinyURL.com :- {url}**\n"
    except Exception as error:
        print(f"TinyURL.com Error :- {error}")
    
    # Ez4short.com Shortener
    try:
        api_url = "https://ez4short.com/api" 
        params = {'api': EZ4SHORT_API, 'url': link}
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params, raise_for_status=True) as response:
                data = await response.json()
                url = data["shortenedUrl"]
                shorten_urls += f"\n**Ez4short.com :- {url}**\n"
    except Exception as error:
        print(f"Ez4short.com Error :- {error}")

    # Shareus.io Shortener
    try:
        api_url = "https://shareus.io/api" 
        params = {'api': SHAREUS_API, 'url': link}
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params, raise_for_status=True) as response:
                data = await response.json()
                url = data["shortenedUrl"]
                shorten_urls += f"\n**Shareus.io :- {url}**\n"
    except Exception as error:
        print(f"Shareus.io Error :- {error}")
    
    # Send the text
    try:
        shorten_urls += ""
        return shorten_urls
    except Exception as error:
        return error

# Country Details

@Client.on_message(filters.command(["country"]))
async def country_info(bot, update):
    country = update.text.split(" ", 1)[1]
    country = CountryInfo(country)
    info = f"""𝖢𝗈𝗎𝗇𝗍𝗋𝗒 𝖨𝗇𝖿𝗈𝗋𝗆𝖺𝗍𝗂𝗈𝗇
𝖭𝖺𝗆𝖾 : {country.name()}
𝖭𝖺𝗍𝗂𝗏𝖾 𝖭𝖺𝗆𝖾 : {country.native_name()}
𝖢𝖺𝗉𝗂𝗍𝖺𝗅 : {country.capital()}
Population : <code>{country.population()}</code>
𝖱𝖾𝗀𝗂𝗈𝗇 : {country.region()}
𝖲𝗎𝖻 𝖱𝖾𝗀𝗂𝗈𝗇 : {country.subregion()}
𝖳𝗈𝗉 𝖫𝖾𝗏𝖾𝗅 𝖣𝗈𝗆𝖺𝗂𝗇𝗌 : {country.tld()}
𝖢𝖺𝗅𝗅𝗂𝗇𝗀 𝖢𝗈𝖽𝖾𝗌 : {country.calling_codes()}
𝖢𝗎𝗋𝗋𝖾𝗇𝖼𝗂𝖾𝗌 : {country.currencies()}
𝖱𝖾𝗌𝗂𝖽𝖾𝗇𝖼𝖾 : {country.demonym()}
𝖳𝗂𝗆𝖾𝗓𝗈𝗇𝖾 : <code>{country.timezones()}</code>
"""
    country_name = country.name()
    country_name = country_name.replace(" ", "+")
    buttons=[[
      InlineKeyboardButton("ᴡɪᴋɪᴘᴇᴅɪᴀ", url=f"{country.wiki()}"),
      InlineKeyboardButton("ɢᴏᴏɢʟᴇ", url=f"https://www.google.com/search?q={country_name}")
    ],[
       InlineKeyboardButton('ᴄʟᴏsᴇ', callback_data='close_data')
    ]]
    try:
        await update.reply_photo(
            photo="https://telegra.ph/file/834750cfadc32b359b40c.jpg",
            caption=info,
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True
        )
    except Exception as error:
        await update.reply_text(
            text=error,
            disable_web_page_preview=True,
            quote=True
	)
