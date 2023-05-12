import random
import requests
from spotipy.oauth2 import SpotifyClientCredentials
from pyrogram import Client as FilterBot, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from configs import BOT_PICS, StartTxT, HelpTxT, AboutTxT, LOGGER
from FilterBot.database import db
from pyrogram import enums


# Replace with your OpenLibrary API key
OPEN_LIBRARY_API_KEY = "your_api_key_here"

# Get the OpenLibrary book ID using the book's title
def get_book_id(book_title):
    url = f"https://openlibrary.org/search.json?title={book_title}"
    response = requests.get(url)
    results = response.json()["docs"]
    if len(results) > 0:
        book_id = results[0]["key"].split("/")[-1]
        return book_id
    else:
        return None

# Define a command handler for the /bookid command
@FilterBot.on_message(filters.command("bookid"))
def get_bookid(bot, update):
    try:
        # Get the book title from the user's message
        book_title = " ".join(update.message.text.split()[1:])
        # Call the OpenLibrary API to get the book ID
        book_id = get_book_id(book_title)
        # Send the book ID back to the user
        if book_id:
            response_text = f"The ID of book '{book_title}' is: {book_id}"
        else:
            response_text = f"Sorry, I couldn't find any book with title '{book_title}'"
        bot.send_message(chat_id=update.chat.id, text=response_text)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.chat.id, text=f"An error occurred {e}")
