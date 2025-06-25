import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery
from helper.database import jishubotz
from config import Config, Txt  
from .fsub import *

@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user = message.from_user
    await jishubotz.add_user(client, message)
    if Config.IS_FSUB and not await get_fsub(client, message):
        return

    button = InlineKeyboardMarkup([
        [InlineKeyboardButton('• ᴀʙᴏᴜᴛ •', callback_data='about'),
         InlineKeyboardButton('• ʜᴇʟᴘ •', callback_data='help')],
        [InlineKeyboardButton('♻ ᴅᴇᴠᴇʟᴏᴘᴇʀ ♻', user_id=int(Config.ADMIN))]
    ])

    if Config.START_PIC:
        pic = random.choice(Config.START_PIC)
        await message.reply_photo(
            photo=pic,
            caption=Txt.START_TXT.format(user.mention),
            reply_markup=button
        )
    else:
        await message.reply_text(
            text=Txt.START_TXT.format(user.mention),
            reply_markup=button,
            disable_web_page_preview=True
        )

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 
    if data == "start":
        await query.message.edit_text(
            text=Txt.START_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton('• ᴀʙᴏᴜᴛ •', callback_data='about'),
                InlineKeyboardButton('• ʜᴇʟᴘ •', callback_data='help')],
                [InlineKeyboardButton('♻ ᴅᴇᴠᴇʟᴏᴘᴇʀ ♻', user_id=int(Config.ADMIN))]
            ])
        )
    elif data == "help":
        await query.message.edit_text(
            text=Txt.HELP_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
		[InlineKeyboardButton("sᴇᴛ ᴍᴇᴛᴀᴅᴀᴛᴀ", callback_data = "meta")],
                [InlineKeyboardButton("ᴘʀᴇꜰɪx", callback_data = "prefix"),
                InlineKeyboardButton("sᴜꜰꜰɪx", callback_data = "suffix")],
		[InlineKeyboardButton("ᴄᴀᴘᴛɪᴏɴ", callback_data = "caption"),
                InlineKeyboardButton("ᴛʜᴜᴍʙɴᴀɪʟ", callback_data = "thumbnail")],
		[InlineKeyboardButton("ʜᴏᴍᴇ", callback_data = "start")]
            ])            
        )

    elif data == "meta":
        await query.message.edit_caption(
            caption=Txt.SEND_METADATA,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="help"), InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]
            ])
	)

    elif data == "prefix":
        await query.message.edit_caption(
            caption=Txt.PREFIX,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="help"), InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]
            ])
	)

    elif data == "suffix":
        await query.message.edit_caption(
            caption=Txt.SUFFIX,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="help"), InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]
            ])
	)

    elif data == "caption":
        await query.message.edit_caption(
            caption=Txt.CAPTION_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="help"), InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]
            ])
	)

    elif data == "thumbnail":
        await query.message.edit_caption(
            caption=Txt.THUMBNAIL_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="help"), InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]
            ])
	)

    elif data == "about":
        await query.message.edit_text(
            text=Txt.ABOUT_TXT,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🤖 ᴍᴏʀᴇ ʙᴏᴛs", url="https://t.me/ST_Rename_Update"),
                InlineKeyboardButton("💥  ᴅᴏɴᴀᴛᴇ", callback_data="donate")],
		[InlineKeyboardButton("ʜᴏᴍᴇ", callback_data="start")]
            ])            
        )

    elif data == "donate":
        await query.message.edit_text(
            text=Txt.DONATE_TXT,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🤖 ᴍᴏʀᴇ ʙᴏᴛs", url="https://t.me/ST_Rename_Update")],
                [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data = "about"),
                InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data = "close")]
            ])            
	)

    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except:
            await query.message.delete()
            await query.message.continue_propagation()

    elif data.startswith("sendAlert"):
        user_id =(data.split("_")[1])
        user_id = int(user_id.replace(' ' , ''))
        if len(str(user_id)) == 10:
            reason = str(data.split("_")[2])
            try:
                await client.send_message(user_id , f"<b>ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ʙʏ [ʀᴀʜᴜʟ](https://telegram.me/callownerbot)\nʀᴇᴀsᴏɴ : {reason}</b>")
                await query.message.edit(f"<b>Aʟᴇʀᴛ sᴇɴᴛ ᴛᴏ <code>{user_id}</code>\nʀᴇᴀsᴏɴ : {reason}</b>")
            except Exception as e:
                await query.message.edit(f"<b>sʀʏ ɪ ɢᴏᴛ ᴛʜɪs ᴇʀʀᴏʀ : {e}</b>")
        else:
            await query.message.edit(f"<b>Tʜᴇ ᴘʀᴏᴄᴇss ᴡᴀs ɴᴏᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ʙᴇᴄᴀᴜsᴇ ᴛʜᴇ ᴜsᴇʀ ɪᴅ ᴡᴀs ɴᴏᴛ ᴠᴀʟɪᴅ, ᴏʀ ᴘᴇʀʜᴀᴘs ɪᴛ ᴡᴀs ᴀ ᴄʜᴀɴɴᴇʟ ɪᴅ</b>")

    elif data.startswith('noAlert'):
        user_id =(data.split("_")[1])
        user_id = int(user_id.replace(' ' , ''))
        await query.message.edit(f"<b>Tʜᴇ ʙᴀɴ ᴏɴ <code>{user_id}</code> ᴡᴀs ᴇxᴇᴄᴜᴛᴇᴅ sɪʟᴇɴᴛʟʏ.</b>")

    elif data.startswith('sendUnbanAlert'):
        user_id =(data.split("_")[1])
        user_id = int(user_id.replace(' ' , ''))
        if len(str(user_id)) == 10:
            try:
                unban_text = "<b>ʜᴜʀʀᴀʏ..ʏᴏᴜ ᴀʀᴇ ᴜɴʙᴀɴɴᴇᴅ ʙʏ [ʀᴀʜᴜʟ](https://telegram.me/callownerbot)</b>"
                await client.send_message(user_id , unban_text)
                await query.message.edit(f"<b>Uɴʙᴀɴɴᴇᴅ Aʟᴇʀᴛ sᴇɴᴛ ᴛᴏ <code>{user_id}</code>\nᴀʟᴇʀᴛ ᴛᴇxᴛ : {unban_text}</b>")
            except Exception as e:
                await query.message.edit(f"<b>sʀʏ ɪ ɢᴏᴛ ᴛʜɪs ᴇʀʀᴏʀ : {e}</b>")
        else:
            await query.message.edit(f"<b>Tʜᴇ ᴘʀᴏᴄᴇss ᴡᴀs ɴᴏᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ʙᴇᴄᴀᴜsᴇ ᴛʜᴇ ᴜsᴇʀ ɪᴅ ᴡᴀs ɴᴏᴛ ᴠᴀʟɪᴅ, ᴏʀ ᴘᴇʀʜᴀᴘs ɪᴛ ᴡᴀs ᴀ ᴄʜᴀɴɴᴇʟ ɪᴅ</b>")   
    elif data.startswith('NoUnbanAlert'):
        user_id =(data.split("_")[1])
        user_id = int(user_id.replace(' ' , ''))
        await query.message.edit(f"Tʜᴇ ᴜɴʙᴀɴ ᴏɴ <code>{user_id}</code> ᴡᴀs ᴇxᴇᴄᴜᴛᴇᴅ sɪʟᴇɴᴛʟʏ.")
