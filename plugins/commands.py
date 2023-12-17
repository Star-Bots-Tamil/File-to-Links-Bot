import os
import logging
import random
import asyncio
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
from random import choice
import os
import math
import time
import requests
from pyrogram import Client, filters, enums
from database.database import db
from database.connection import connection
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

ADMIN = int(os.environ.get("ADMIN", "1391556668"))

#=====================================================

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
        await asyncio.sleep(2)
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
    files_ = await get_file_details(file_id)           
    if not files_:
        buttons = [
            [InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url=await get_group(grp_id))],
            [InlineKeyboardButton('Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ', url=await get_channel(grp_id))],
            [InlineKeyboardButton("Bᴏᴛ Oᴡɴᴇʀ", url=await get_admin(grp_id))]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        return await message.reply('Nᴏ sᴜᴄʜ ғɪʟᴇ ᴇxɪsᴛ.', reply_markup=reply_markup)

    files = files_[0]
    title = files.file_name
    size = get_size(files.file_size)
    grp_id = await active_connection(str(message.from_user.id))
    settings = await get_settings(grp_id)
    FILE_CAPTION = settings["caption"]
    f_caption = files.caption
    if settings["caption"]:
        try:
            f_caption = FILE_CAPTION.format(file_name='' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
        except Exception as e:
            logger.exception(e)
            f_caption = f_caption
    if f_caption is None:
        f_caption = f"{files.file_name}"
    feck = await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=file_id,
        caption=f_caption + f"\n\n<b>Note :- This File Will be Deleted in {round(FILE_DELETE_TIMER/60)} Minutes. So Forward to Your Saved Messages.</b>",
        protect_content=True if pre == 'filep' else False,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url=await get_group(grp_id)),
                    InlineKeyboardButton('Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ', url=await get_channel(grp_id))
                ], [
                    InlineKeyboardButton("Bᴏᴛ Oᴡɴᴇʀ", url=await get_admin(grp_id))
                ]
            ]
        )
    )
    await asyncio.sleep(FILE_DELETE_TIMER)
    await feck.delete()

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

@Client.on_message(filters.command('set_shortlink'))
async def set_shortlink(bot, message):
    user_id = message.from_user.id
    data = message.text
    try:
        command, shortlink_url, api = data.split(" ")
    except ValueError:
        return await message.reply_text("<b>Command Incomplete :(\n\nGive me a shortlink and api along with the command !\n\nFormat: <code>/set_personal_shortlink tnshort.net d03a53149bf186ac74d58ff80d916f7a79ae5745</code></b>")

    reply = await message.reply_text("<b>Please Wait...</b>")
    # Assuming you have a function to save user settings, replace the following line accordingly
    await save_user_settings(user_id, 'shortlink', shortlink_url)
    await save_user_settings(user_id, 'shortlink_api', api)
    await save_user_settings(user_id, 'is_shortlink', True)
    await reply.edit_text(f"<b>Successfully added Shortlink API for {message.from_user.username}.\n\nCurrent Shortlink Website: <code>{shortlink_url}</code>\nCurrent API: <code>{api}</code></b>")

@Client.on_message(filters.command('get_shortlink'))
async def show_shortlink(bot, message):
    user_id = message.from_user.id

    # Assuming you have a function to retrieve user settings, replace the following line accordingly
    user_settings = await get_user_settings(user_id)

    if 'shortlink' in user_settings.keys() and 'shortlink_api' in user_settings.keys():
        shortlink_url = user_settings['shortlink']
        api = user_settings['shortlink_api']
        return await message.reply_text(f"<b>Your Shortlink Website: <code>{shortlink_url}</code>\nYour API: <code>{api}</code></b>")
    else:
        return await message.reply_text("<b>No Shortlink API found for your account. Use /set_shortlink command to set it up.</b>")

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
        shortened_link = await get_shortlink(star_stream)
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
		
