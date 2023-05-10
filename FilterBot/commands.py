import random
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pyrogram import Client as FilterBot, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from configs import BOT_PICS, StartTxT, HelpTxT, AboutTxT, LOGGER
from FilterBot.database import db

# Initialize Spotify API credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="61dcb7d7bff442e3a54a3340825ade72", client_secret="ee316ec4c1e848078d9131c8922a343d"))

@FilterBot.on_message(filters.private & filters.command("start"))
async def startCMD(client: FilterBot, message: Message):

    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.first_name, message.from_user.id)

    bot = await client.get_me()
    keyboard = [[
      InlineKeyboardButton('Add Me To Your Chat', url=f"https://t.me/{bot.username}?startgroup=true")
      ],[
      InlineKeyboardButton('Help', callback_data='main#help'),
      InlineKeyboardButton('About', callback_data='main#about')
      ],[
      InlineKeyboardButton('Update', url='t.me/check_this_channel'),
      InlineKeyboardButton('Support', url='t.me/motechgroup')
      ]]

    if "motech" == BOT_PICS[0]:
        await message.reply_text(text=StartTxT.format(mention=message.from_user.mention), reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await message.reply_photo(photo=random.choice(BOT_PICS), caption=StartTxT.format(mention=message.from_user.mention), reply_markup=InlineKeyboardMarkup(keyboard))

@FilterBot.on_message(filters.private & filters.command("hi"))
async def helpCMD(client: FilterBot, message: Message):

    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.first_name, message.from_user.id)

    keyboard = [[ InlineKeyboardButton('Home', callback_data='main#start'),
                  InlineKeyboardButton('Close', callback_data='main#close') ]]

    if "motech" == BOT_PICS[0]:
        await message.reply_text(text=HelpTxT.format(mention=message.from_user.mention), reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await message.reply_photo(photo=random.choice(BOT_PICS), caption=HelpTxT.format(mention=message.from_user.mention), reply_markup=InlineKeyboardMarkup(keyboard))

@FilterBot.on_message(filters.private & filters.command("help"))
async def helpCMD(client: FilterBot, message: Message):

    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.first_name, message.from_user.id)

    keyboard = [[ InlineKeyboardButton('Home', callback_data='main#start'),
                  InlineKeyboardButton('Close', callback_data='main#close') ]]

    if "motech" == BOT_PICS[0]:
        await message.reply_text(text=HelpTxT.format(mention=message.from_user.mention), reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await message.reply_photo(photo=random.choice(BOT_PICS), caption=HelpTxT.format(mention=message.from_user.mention), reply_markup=InlineKeyboardMarkup(keyboard))

@FilterBot.on_message(filters.private & filters.command("about"))
async def aboutCMD(client: FilterBot, message: Message):

    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.first_name, message.from_user.id)

    keyboard = [[ InlineKeyboardButton('Channel', url='https://t.me/check_this_channel'),
                   InlineKeyboardButton('Group', url='https://t.me/Thedigital_library') ],
                [ InlineKeyboardButton('Home', callback_data='main#start'),
                  InlineKeyboardButton('Help', callback_data='main#help') ]]

    if "motech" == BOT_PICS[0]:
        await message.reply_text(text=AboutTxT.format(mention=message.from_user.mention), reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await message.reply_photo(photo=random.choice(BOT_PICS), caption=AboutTxT.format(mention=message.from_user.mention), reply_markup=InlineKeyboardMarkup(keyboard))



async def get_book_details(client, message):
    # Get the search query from the message text
    search_query = " ".join(message.command[1:])

    # Send a request to the Google Books API with the search query
    url = f"https://www.googleapis.com/books/v1/volumes?q={search_query}"
    response = requests.get(url)

    # Parse the response and extract the book details and thumbnail URL
    if response:
        book_data = response.json()["items"][0]["volumeInfo"]
        title = book_data["title"]
        authors = ", ".join(book_data["authors"])
        publisher = book_data["publisher"]
        published_date = book_data["publishedDate"]
        description = book_data["description"]
        thumbnail_url = book_data["imageLinks"]["thumbnail"]

    # Construct the message text with book details and thumbnail URL
        message_text = f"<b>{title}</b> by {authors}\n\n"
        message_text += f"<b>Publisher:</b> {publisher}\n"
        message_text += f"<b>Publication Date:</b> {published_date}\n\n"
        message_text += f"<i>{description}</i>\n"
        message_text += f"Thumbnail URL: {thumbnail_url}"

    # Send the message with the book details and thumbnail URL
    await message.reply_text(message_text, parse_mode=html)

@FilterBot.on_message(filters.private & filters.command("book"))
async def handle_book_command(client, message):
    await get_book_details(client, message)


@FilterBot.on_callback_query(filters.regex('main'))
async def maincallback(client: FilterBot, message):

    try:
        x, type = message.data.split("#")
    except:
        await message.answer("Erorrrr....")
        await message.message.delete()
        return

    if type == "start":
        bot = await client.get_me()
        keyboard = [[ InlineKeyboardButton('Add Me To Your Chat', url=f"t.me/{bot.username}?startgroup=true") ],
                    [ InlineKeyboardButton('Help', callback_data='main#help'),
                      InlineKeyboardButton('About', callback_data='main#about') ],
                    [ InlineKeyboardButton('Channel', url='t.me/check_this_channel'),
                      InlineKeyboardButton('Group', url='t.me/song_requestgroup') ]]
        await message.message.edit(text=StartTxT.format(mention=message.from_user.mention), reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True)

    elif type == "help":
        keyboard = [[ InlineKeyboardButton('Home', callback_data='main#start'),
                      InlineKeyboardButton('Close', callback_data='main#close') ]]
        await message.message.edit(text=HelpTxT, reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True)

    elif type == "about":
        keyboard = [[ InlineKeyboardButton('Channel', url='https://t.me/check_this_channel'),
                       InlineKeyboardButton('Group', url='https://t.me/Thedigital_library') ],
                    [ InlineKeyboardButton('Home', callback_data='main#start'),
                      InlineKeyboardButton('Help', callback_data='main#help') ]]
        await message.message.edit(text=AboutTxT, reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True)
