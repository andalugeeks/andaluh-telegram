#!/usr/bin/env python
# -*- coding: utf-8 -*-
###
# 
# Copyright (c) 2018 EPA
# Authors : J. Félix Ontañón <felixonta@gmail.com>

import os
import logging
import re
import random
from functools import reduce
from uuid import uuid4
import datetime as dt

import requests

from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.utils.helpers import escape_markdown

API_BASEURL=os.environ['APIURL']
HELP_STRING='Tan solo cítame al inicio de tu mensaje y se te presentarán diferentes opciones de transcripción.'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def help(update, context):
    """Send a message when with command help."""
    update.message.reply_text(HELP_STRING)

def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query

    results = [

        InlineQueryResultArticle(
            id=uuid4(),
            title="EPA (standard)",
            input_message_content=InputTextMessageContent(
                requests.get(API_BASEURL, params=dict(spanish=query, vaf=u'ç', escapeLinks=True)).json()['andaluh'],
                parse_mode=ParseMode.MARKDOWN)),

        InlineQueryResultArticle(
            id=uuid4(),
            title="EPA seseante",
            input_message_content=InputTextMessageContent(
                requests.get(API_BASEURL, params=dict(spanish=query, vaf=u's', escapeLinks=True)).json()['andaluh'],
                parse_mode=ParseMode.MARKDOWN)),    

        InlineQueryResultArticle(
            id=uuid4(),
            title="EPA zezeante",
            input_message_content=InputTextMessageContent(
                requests.get(API_BASEURL, params=dict(spanish=query, vaf=u'z', escapeLinks=True)).json()['andaluh'],
                parse_mode=ParseMode.MARKDOWN)),

        InlineQueryResultArticle(
            id=uuid4(),
            title="EPA heheante",
            input_message_content=InputTextMessageContent(
                requests.get(API_BASEURL, params=dict(spanish=query, vaf=u'h', escapeLinks=True)).json()['andaluh'],
                parse_mode=ParseMode.MARKDOWN))
    ]

    update.inline_query.answer(results)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(os.environ["TOKEN"], use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("ayuda", help))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("start", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()