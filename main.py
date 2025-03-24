import utils
import pathlib
import pyrogram
import tiktok_downloader
from load import *
from datetime import datetime, timezone

cwd = pathlib.Path(__file__).parent

bot = pyrogram.Client(
    name="tiktok-bot", api_id=api_id, api_hash=api_hash, bot_token=token_bot
)

async def start_handler(client: pyrogram.Client, message: pyrogram.types.Message):
    first_name = message.chat.first_name
    userid = message.chat.id
    text = message.text
    print(f"{userid} {first_name} - {text}")
    retext = f"""Welcome {first_name} to Tiktok Video Downloader Bot

How to use :

ID : Cara menggunakan bot hanya dengan mengirimkan tautan dari video tiktok yang ingin kamu unduh.

EN : How to use the bot by simply sending the link of the tiktok video you want to download.
    """
    await client.send_message(chat_id=userid, text=retext, reply_to_message_id=message.id)
    return

async def ping_handler(client: pyrogram.Client, message: pyrogram.types.Message):
    userid = message.chat.id
    first_name = message.chat.first_name or ""
    print(f"{userid} {first_name} - /ping")
    await client.send_message(chat_id=userid, text="Pong!", reply_to_message_id=message.id)

async def tiktok_handler(client: pyrogram.Client, message: pyrogram.types.Message):
    userid = message.chat.id
    first_name = message.chat.first_name or ""
    text = message.text
    print(f"{userid} {first_name} - {text}")
    tiktok_url = text.split("\n")[0] if "\n" in text else text
    if "tiktok" not in tiktok_url:
        await client.send_message(chat_id=userid, text="The video link you sent may be wrong.", reply_to_message_id=message.id)
        return
    video_id, author_id, author_username, video_url, images, cookies = (
        await utils.get_video_detail(tiktok_url)
    )
    if video_id is None:
        await client.send_message(chat_id=userid, text="The tiktok video you want to download doesn't exist, it might be deleted or a private video.", reply_to_message_id=message.id)
        return
    retext = "Successfully download the video\n\nPowered by @TiktokVideoDownloaderIDBot"
    keylist = [
        [pyrogram.types.InlineKeyboardButton(text="Source Video", url=tiktok_url)],
        [
            pyrogram.types.InlineKeyboardButton(text="Follow Me", url="https://t.me/fawwazthoerif"),
            pyrogram.types.InlineKeyboardButton(text="Donation", callback_data="donation"),
        ],
    ]
    rekey = pyrogram.types.InlineKeyboardMarkup(inline_keyboard=keylist)
    output = cwd.joinpath(f"{video_id}.mp4")
    if video_url is None or len(video_url) <= 0:
        await tiktok_downloader.musicaldown(url=tiktok_url, output=output)
    else:
        await tiktok_downloader.get_content(url=video_url, output=output, cookies=cookies)
    await client.send_video(chat_id=userid, video=output, caption=retext, reply_markup=rekey)
    output.unlink(missing_ok=True)
    return

async def donation_handler(client: pyrogram.Client, message: pyrogram.types.Message | pyrogram.types.CallbackQuery):
    userid = message.chat.id if isinstance(message, pyrogram.types.Message) else message.from_user.id
    first_name = message.chat.first_name if isinstance(message, pyrogram.types.Message) else message.from_user.first_name
    print(f"{userid} {first_name} - donation")
    retext = """If you like my work, you can support me through the link below.
    
International : https://sociabuzz.com/fawwazthoerif/tribe
Indonesia : https://trakteer.id/fawwazthoerif/tip

CRYPTO
USDT (TON) : `UQDicJd7KwBcxzqbn6agUc_KVl8BklzyvuKGxEVG7xuhnTFt`
    """
    await client.send_message(chat_id=userid, text=retext, disable_web_page_preview=True)
    return

async def main():
    print(f"start bot !")
    await bot.start()
    me = await bot.get_me()
    print(f"Bot name : {me.first_name}")
    print(f"Bot username : {me.username}")
    bot.add_handler(pyrogram.handlers.message_handler.MessageHandler(callback=start_handler, filters=pyrogram.filters.command(["start"])))
    bot.add_handler(pyrogram.handlers.message_handler.MessageHandler(callback=ping_handler, filters=pyrogram.filters.regex(r"ping")))
    bot.add_handler(pyrogram.handlers.message_handler.MessageHandler(callback=tiktok_handler, filters=pyrogram.filters.regex(r"tiktok")))
    bot.add_handler(pyrogram.handlers.message_handler.MessageHandler(callback=donation_handler, filters=pyrogram.filters.regex(r"donation")))
    bot.add_handler(pyrogram.handlers.callback_query_handler.CallbackQueryHandler(callback=donation_handler, filters=pyrogram.filters.regex(r"donation")))
    await pyrogram.idle()
    await bot.stop()

import asyncio
bot.run(main())
