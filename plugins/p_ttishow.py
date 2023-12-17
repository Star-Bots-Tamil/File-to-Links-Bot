import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid
from info import ADMINS, LOG_CHANNEL, SUPPORT_CHAT, MELCOW_NEW_USERS
from database.database import db
from utils import get_size, temp, get_settings
from Script import script
from pyrogram.errors import ChatAdminRequired

@Client.on_message(filters.command('stats') & filters.incoming)
async def get_stats(bot, message):
    buttons = [[
        InlineKeyboardButton('🌀 Refresh', callback_data='refresh')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    star = await message.reply('<b>Accessing Status 📊 Details...</b>')
    total_users = await db.total_users_count()
    size = await db.get_db_size()
    free = 536870912 - size
    size = get_size(size)
    free = get_size(free)
    await star.edit(script.STATUS_TXT.format(total_users, size, free),
                   reply_markup=reply_markup,
                   parse_mode=enums.ParseMode.HTML)


# a function for trespassing into others groups, Inspired by a Vazha
# Not to be used , But Just to showcase his vazhatharam.
# @Client.on_message(filters.command('invite') & filters.user(ADMINS))
async def gen_invite(bot, message):
    if len(message.command) == 1:
        return await message.reply('<b>Give Me a Chat 🆔</b>')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        return await message.reply('<b>Give Me A Valid Chat 🆔</b>')
    try:
        link = await bot.create_chat_invite_link(chat)
    except ChatAdminRequired:
        return await message.reply("<b>Invite Link Generation Failed, Iam Not Having Sufficient Rights</b>")
    except Exception as e:
        return await message.reply(f'<b>Error {e}</b>')
    await message.reply(f'<b>Here is your Invite Link :- {link.invite_link}</b>')

@Client.on_message(filters.command('ban') & filters.user(ADMINS))
async def ban_a_user(bot, message):
    # https://t.me/GetTGLink/4185
    if len(message.command) == 1:
        return await message.reply('<b>Give me a user 🆔 / Username</b>')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("<b>This is an Invalid User, Make Sure ia Have met him Before.</b>")
    except IndexError:
        return await message.reply("<b>This Might be a Channel, Make Sure its a user.</b>")
    except Exception as e:
        return await message.reply(f'<b>Error - {e}</b>')
    else:
        jar = await db.get_ban_status(k.id)
        if jar['is_banned']:
            return await message.reply(f"<b>{k.mention} is Already banned\nReason: {jar['ban_reason']}</b>")
        await db.ban_user(k.id, reason)
        temp.BANNED_USERS.append(k.id)
        await message.reply(f"<b>Successfully Banned {k.mention}</b>")


    
@Client.on_message(filters.command('unban') & filters.user(ADMINS))
async def unban_a_user(bot, message):
    if len(message.command) == 1:
        return await message.reply('<b>Give me a User 🆔 / Username</b>')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("<b>This is an Invalid User, Make Sure ia have met him Before.</b>")
    except IndexError:
        return await message.reply("<b>This might be a Channel, Make Sure its a User.</b>")
    except Exception as e:
        return await message.reply(f'<b>Error - {e}</b>')
    else:
        jar = await db.get_ban_status(k.id)
        if not jar['is_banned']:
            return await message.reply(f"<b>{k.mention} is Not yet Banned.</b>")
        await db.remove_ban(k.id)
        temp.BANNED_USERS.remove(k.id)
        await message.reply(f"<b>Successfully Unbanned {k.mention}</b>")

@Client.on_message(filters.command('invite') & filters.user(ADMINS))
async def gen_invite(bot, message):
    if len(message.command) == 1:
        return await message.reply('**Give Me a Chat 🆔**')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        return await message.reply('**Give Me A Valid Chat ID**')
    try:
        link = await bot.create_chat_invite_link(chat)
    except ChatAdminRequired:
        return await message.reply("**Invite Link Generation Failed, Iam Not Having Sufficient Rights**")
    except Exception as e:
        return await message.reply(f'Error {e}')
    await message.reply(f'**Here is your Invite Link {link.invite_link}**')

    
@Client.on_message(filters.command('users') & filters.user(ADMINS))
async def list_users(bot, message):
    # https://t.me/GetTGLink/4184
    raju = await message.reply('<b>Getting List Of Users</b>')
    users = await db.get_all_users()
    out = "Users Saved In DB Are:\n\n"
    async for user in users:
        out += f"<a href=tg://user?id={user['id']}>{user['name']}</a>"
        if user['ban_status']['is_banned']:
            out += '( Banned User )'
        out += '\n'
    try:
        await raju.edit_text(out)
    except MessageTooLong:
        with open('users.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('users.txt', caption="<b>List Of Users</b>")
