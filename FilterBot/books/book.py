import random
import requests
from pyrogram import Client as FilterBot, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from configs import BOT_PICS, StartTxT, HelpTxT, AboutTxT, LOGGER
from FilterBot.database import db
from pyrogram import enums


# Replace with your OpenLibrary API key
OPEN_LIBRARY_API_KEY = "your_api_key_here"

# Get the OpenLibrary book ID using the book's title
def get_book_id(book_title):
    if book_title:
        url = f"https://openlibrary.org/search.json?title={book_title}"
        response = requests.get(url)
        results = response.json()["docs"]
        if len(results) > 0:
            book_id = results[0]["key"].split("/")[-1]
            return book_id
    return None


# Define a command handler for the /book command
@FilterBot.on_message(filters.command("book"))
def send_book(_, update):
    try:
        # Check if the update is a message and has a document
        if update.message and update.message.document:
            # Get the book title from the user's message
            book_title = " ".join(update.command[1:])
            # Call the OpenLibrary API to get the book ID and download link
            book_id = get_book_id(book_title)
            if book_id:
                url = f"https://openlibrary.org/books/{book_id}/formats.json"
                response = requests.get(url)
                download_link = response.json().get("epub")
                if download_link:
                    # Send the book file to the user as a document
                    file_name = f"{book_title}.epub"
                    update.reply_document(document=download_link, file_name=file_name)
                else:
                    update.reply_text(f"Sorry, I couldn't find the download link for book '{book_title}'")
            else:
                update.reply_text(f"Sorry, I couldn't find any book with title '{book_title}'")
    except Exception as e:
        print(e)
        update.reply_text(f"An error occurred{e}")
