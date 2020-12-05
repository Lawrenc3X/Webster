# bot.py
import os
from typing import Generator
from re import sub
from pprint import pprint

import discord
from discord.ext import commands
from dotenv import load_dotenv
from spellchecker import SpellChecker
from spamprotector import SpamProtector
from customdictionary import UserDictionary

load_dotenv()
# TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN = os.environ['DISCORD_TOKEN']

bot = commands.Bot(command_prefix='w!')
spellcheckers = {}
spam = SpamProtector()
previous_message = None

def corrections(author) -> Generator[str, None, None]:
    if author in spellcheckers:
        spell = spellcheckers[author]
    else:
        spellcheckers[author] = UserDictionary()
        spell = spellcheckers[author]

    words = [sub("(^[^a-zA-Z]+|[^a-zA-Z]+$)", "", word) for word in previous_message.split(" ")]
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

            if previous_message == None:
                await message.channel.send("no recent messages")
                return

            await message.channel.send("*" + ", ".join(corrections(message.author.id) ) )

    else:
        previous_message = message.content
 
    await bot.process_commands(message)

@bot.command(name = "add")
async def add(ctx, word = None):
    """add words to your dictionary"""
    if word == None:
        print("no word")
        await ctx.send("usage: w!add [word]")
        return
    
    if ctx.author.id in spellcheckers:
        spellcheckers[ctx.author.id].add(word)
    else:
        spellcheckers[ctx.author.id] = UserDictionary()
        spellcheckers[ctx.author.id].add(word) 

    print("invoked")
    await ctx.send("placeholder command")

bot.run(TOKEN)
