# bot.py
import os
from re import sub
from pprint import pprint

import discord  # install
from discord.ext import commands
from spellchecker import SpellChecker
from spamprotector import SpamProtector

TOKEN = os.environ['']  # fill

bot = commands.Bot(command_prefix='w!')
spam = SpamProtector()
spell = SpellChecker()
previous_message = None


def corrections(author):
    words = [
        sub("(^[^a-zA-Z]+|[^a-zA-Z]+$)", "", word)
        for word in previous_message.split(" ")
    ]
    misspelled = spell.unknown(words)

    for word in misspelled:
        yield spell.correction(word)


@bot.event
async def on_message(message):
    global previous_message

    if message.author.bot:
        return

    if message.content == "*":
        if not spam.ignore(message.author.id):
            spam.log(message.author.id)

            print(len(spam.requests[message.author.id]))
            pprint(spam.requests)

            if previous_message is None:
                await message.channel.send("no recent messages")
                return

            await message.channel.send(
                "*" + ", ".join(corrections(message.author.id))
            )

    else:
        previous_message = message.content

    await bot.process_commands(message)


@bot.command(name="add")
async def add(ctx, word=None):
    """add words to your dictionary"""
    pass

bot.run(TOKEN)
