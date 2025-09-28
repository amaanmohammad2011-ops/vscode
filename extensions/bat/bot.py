#!/usr/bin/env python3
"""
bot.py — Simple resilient Telegram bot (long polling)

Requirements:
    pip install pyTelegramBotAPI

Usage:
    python3 bot.py
"""

import telebot
import logging
import time
import sys
import signal

# === Replace with the API token you gave ===
API_TOKEN = "8330171576:AAFL37ISOJ8SrWQ9DZEgpYJvnSXdfuF3rrM"

# === Setup logging ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

bot = telebot.TeleBot(API_TOKEN, parse_mode="HTML")

# ---- Handlers ----
@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id,
                     "👋 Hello! Bot is online and responding. Send any text and I'll echo it back.")

@bot.message_handler(commands=["help"])
def handle_help(message):
    bot.send_message(message.chat.id,
                     "This is a simple echo bot. Send text and it will be echoed back.")

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    # Example: simple echo with safe guard
    text = message.text or ""
    try:
        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, f"You said:\n{text}")
    except Exception:
        logging.exception("Failed to reply to message (ignored)")

# Graceful shutdown
def _shutdown(signum, frame):
    logging.info("Received stop signal, exiting...")
    try:
        bot.stop_polling()
    except Exception:
        pass
    sys.exit(0)

signal.signal(signal.SIGINT, _shutdown)
signal.signal(signal.SIGTERM, _shutdown)

# ---- Polling loop with automatic restart ----
if _name_ == "_main_":
    while True:
        try:
            logging.info("Starting bot polling...")
            # timeout helps detect network hiccups; non_stop True keeps polling loop.
            bot.polling(non_stop=True, timeout=30)
        except Exception:
            logging.exception("Polling crashed — restarting in 5 seconds...")
            time.sleep(5)
