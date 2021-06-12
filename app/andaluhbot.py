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
from telegram.ext import Updater, PicklePersistence, InlineQueryHandler, CommandHandler, ChosenInlineResultHandler

API_BASEURL=os.environ['APIURL']
USERPREF_PATH=os.environ.get('USERPREF_PATH', '/var/www/data/andaluhbot_data/userprefs')
HELP_STRING='Tan solo cítame al inicio de tu mensaje y se te presentarán diferentes opciones de transcripción.'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def merge_dicts(*dict_args):
    """
    Given any number of dictionaries, shallow copy and merge into a new dict,
    precedence goes to key-value pairs in latter dictionaries.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def help(update, context):
    """Send a message when with command help."""
    update.message.reply_text(HELP_STRING)

def inlinequeryselected(update, context):
    """Store the last selection for this user"""
    if update.chosen_inline_result.result_id != 'default':
        if update.chosen_inline_result.result_id != 'standard':
            arg, value = update.chosen_inline_result.result_id.split(':', 1)
            context.user_data[arg] = value
        else:
            context.user_data['vaf'] = u'ç'
            context.user_data['vvf'] = u'h'
    logger.info('after updating: ' + str(context.user_data))

def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query
    logger.info('inline query with existing user data: ' + str(context.user_data))
    apiParams = dict(
        spanish=query,
        vaf=context.user_data.get('vaf', u'ç'),
        vvf=context.user_data.get('vvf', u'h'),
        escapeLinks=True
    )
    transliterations = {
        'default': requests.get(API_BASEURL, params=apiParams).json()['andaluh'],
        'standard': requests.get(API_BASEURL, params=merge_dicts(apiParams, [('vaf', u'ç'), ('vvf', u'h')])).json()['andaluh'],
        'vaf:s': requests.get(API_BASEURL, params=merge_dicts(apiParams, [('vaf', u's')])).json()['andaluh'],
        'vaf:z': requests.get(API_BASEURL, params=merge_dicts(apiParams, [('vaf', u'z')])).json()['andaluh'],
        'vaf:h': requests.get(API_BASEURL, params=merge_dicts(apiParams, [('vaf', u'h')])).json()['andaluh'],
        'vvf:h': requests.get(API_BASEURL, params=merge_dicts(apiParams, [('vvf', u'h')])).json()['andaluh'],
        'vvf:j': requests.get(API_BASEURL, params=merge_dicts(apiParams, [('vvf', u'j')])).json()['andaluh'],
    }

    results = [
        InlineQueryResultArticle(
            id='default',
            title="EPA (tus preferencias guardadas)",
            description=transliterations['default'],
            input_message_content=InputTextMessageContent(
                transliterations['default'],
                parse_mode=ParseMode.MARKDOWN)),
        InlineQueryResultArticle(
            id='standard',
            title="EPA (standard)",
            description=transliterations['standard'],
            input_message_content=InputTextMessageContent(
                transliterations['standard'],
                parse_mode=ParseMode.MARKDOWN)),
        InlineQueryResultArticle(
            id='vaf:s',
            title="EPA seseante",
            description=transliterations['vaf:s'],
            input_message_content=InputTextMessageContent(
                transliterations['vaf:s'],
                parse_mode=ParseMode.MARKDOWN)),
        InlineQueryResultArticle(
            id='vaf:z',
            title="EPA zezeante",
            description=transliterations['vaf:z'],
            input_message_content=InputTextMessageContent(
                transliterations['vaf:z'],
                parse_mode=ParseMode.MARKDOWN)),
        InlineQueryResultArticle(
            id='vaf:h',
            title="EPA heheante",
            description=transliterations['vaf:h'],
            input_message_content=InputTextMessageContent(
                transliterations['vaf:h'],
                parse_mode=ParseMode.MARKDOWN)),
        InlineQueryResultArticle(
            id='vvf:h',
            title="EPA usando Aspirada[ʰ]",
            description=transliterations['vvf:h'],
            input_message_content=InputTextMessageContent(
                transliterations['vvf:h'],
                parse_mode=ParseMode.MARKDOWN)),
        InlineQueryResultArticle(
            id='vvf:j',
            title="EPA usando Jota",
            description=transliterations['vvf:j'],
            input_message_content=InputTextMessageContent(
                transliterations['vvf:j'],
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
    persistence = PicklePersistence(filename=USERPREF_PATH, store_user_data=True, store_chat_data=False, singe_file=False, on_flush=False )
    updater = Updater(os.environ["TOKEN"], use_context=True, persistence=persistence)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("ayuda", help))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("start", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))
    # Handle selection so we store that for latter use.
    dp.add_handler(ChosenInlineResultHandler(inlinequeryselected))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    logger.info('Initializating andalubot with settings: %s', str({
        "API_BASEURL": API_BASEURL,
        "USERPREF_PATH": USERPREF_PATH
    }))

    main()