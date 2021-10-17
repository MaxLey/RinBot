# bot.py
import os
import urllib
import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import DBManager
import DiceHandler
import MessageHandler
from models import Mun, Character

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

MessageHandler.bot = bot #TODO is this okay?

@bot.event
async def on_ready():

    engine = create_engine('sqlite:///stiltz_db.db')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    guild = None
    for guild in bot.guilds:
        break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == 'Ping!':
        response = 'Pong!'
        await message.channel.send(response)

    await bot.process_commands(message)

#TODO fancy little icons?
@bot.command(name='characters')
async def characters(ctx):
    session = DBManager.DBSessionMaker()
    author_id = ctx.author.id
    mun = session.get(Mun.Mun, author_id)
    if not mun:
        await ctx.send("I don't think I know you! Please create a character first using !addchar")
        session.close()
        return
    embed = discord.Embed(title="Characters for " + ctx.author.display_name)
    characters_str = ""
    for character in mun.characters:
        if character.name == mun.active_character:
            characters_str += "**-  " + character.name + " (active)**\n"
        else:
            characters_str += "-  " + character.name + "\n"
    embed.description = characters_str
    embed.colour = discord.Color.red()
    embed.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
    session.close()

@bot.command(name='char')
async def char(ctx):
    session = DBManager.DBSessionMaker()
    author_id = ctx.author.id
    mun = session.get(Mun.Mun, author_id)
    character = [character for character in mun.characters if character.name == mun.active_character]
    if not character:
        await ctx.send("Active character not found! Please set your active character with !iam <character name>")
        session.close()
        return
    character = character[0]
    embed_title = character.name
    if character.pronoun_obj and character.pronoun_subj:
        embed_title += " " + character.pronoun_obj + "/" + character.pronoun_subj
    embed = discord.Embed(title=embed_title)
    #TODO add thumbnail/sprite
    stats_str = ""
    stats_str += "Str: " + character.str_base + "\n"
    stats_str += "Def: " + character.def_base + "\n"
    stats_str += "Mag: " + character.mag_base + "\n"
    stats_str += "Agi: " + character.agi_base + "\n"
    embed.add_field(name="Stats", value=stats_str)
    #TODO finish
    await ctx.send(embed=embed)
    session.close()


#TODO fix return session close
@bot.command(name='rollstat')
async def rollstat(ctx):
    session = DBManager.DBSessionMaker()
    author_id = ctx.author.id
    mun = session.get(Mun.Mun, author_id)
    character = [character for character in mun.characters if character.name == mun.active_character]
    if not character:
        await ctx.send("Active character not found! Please set your active character with !iam <character name>")
        session.close()
        return
    character = character[0]
    dicestring = ctx.message.content.split(' ', 1)[1].lower() #Split the command out of the message content
    dicestring = "2d6" + character.replace_stats_in_string(dicestring)
    await ctx.send("Rolling " + dicestring)
    dicedict = DiceHandler.parse_dice_string(dicestring)
    if not dicedict:
        await ctx.send("Error rolling dice! Please make sure your command is correct! (e.g. \"!rollstat str+5\")")
        session.close()
        return
    result = sum(DiceHandler.roll_dice_dict(dicedict))
    await ctx.send(str(result))
    session.close()


@bot.command(name='roll')
async def roll(ctx):
    dicestring = ctx.message.content.split(' ', 1)[1].lower()
    dicedict = DiceHandler.parse_dice_string(dicestring)
    if not dicedict:
        await ctx.send("Error rolling dice! Please make sure your command is correct! (e.g. \"!roll 3d6+5\")")
        return
    await ctx.send("Rolling " + dicestring)
    result = sum(DiceHandler.roll_dice_dict(dicedict))
    await ctx.send(str(result))

@bot.command(name='iam')
async def iam(ctx, character_name):
    session = DBManager.DBSessionMaker()
    author_id = ctx.author.id
    mun = session.get(Mun.Mun, author_id)
    if not mun:
        await ctx.send("I don't think I know you! Please create a character first using !addchar")
        session.close()
        return
    character_list = [character for character in mun.characters if character.name == character_name]
    if not character_list:
        await ctx.send("Character not found! Please check the spelling of the character name.")
        print("Charnotfound happened")
        print(character_name)
        print(mun.characters)
        for character in mun.characters:
            print(character.name)
        print(character_list)
        session.close()
        return
    else:
        found_character = character_list[0]
        mun.active_character = found_character.name
    session.commit()
    await ctx.send(("<@!{id}>, your active character is now " + character_name).format(id=author_id))
    session.close()

#TODO add message on timeout
#TODO fix return session close
@bot.command(name='addchar')
async def add_character(ctx):
    session = DBManager.DBSessionMaker()
    author_id = ctx.author.id
    usermention = '<@!{id}>'.format(id=author_id)
    await ctx.send('{user}, instructions for character creation sent in DM\'s!'.format(user=usermention))
    await ctx.author.create_dm()
    await ctx.author.dm_channel.send(
        'Hello! Please fill in the following form with the basic details of your character.\n'
        'Please don\'t add or remove any \'=\'s, or I won\'t be able to read it properly!\n'
        'https://cdn.discordapp.com/attachments/885179213387276289/885941400947015710/template.txt')

    def check(m):
        return m.attachments and m.channel == ctx.author.dm_channel
    try:
        msg = await bot.wait_for("message", check=check, timeout=180)
    except asyncio.TimeoutError:
        await ctx.send("Operation timed out - Please call !addchar again to resume character creation.")
        session.close()
        return
    attachment = msg.attachments[0]
    file_location = '{author}.txt'.format(author=ctx.author.id)
    await attachment.save(file_location)
    mun = session.get(Mun.Mun, author_id)
    if not mun:
        mun = Mun.Mun()
        mun.id = ctx.author.id
        session.merge(mun)
    attribs = Character.parse_attributes_from_txt(file_location)
    if not attribs:
        await ctx.author.dm_channel.send("Error in file parse! Please don't change anything, other than adding in your stats.")
        session.close()
        return
    character_name = attribs['name']
    if character_name in [character.name for character in mun.characters]:
        await ctx.author.dm_channel.send("Character already exists! Please use the !editchar command or delete the char before adding it again.")
        session.close()
        return
    character = Character.create_from_attribute_dict(attribs)
    mun.characters.append(character)
    #TODO do I need to merge the mun, since it already came from the session?
    session.merge(mun)
    await ctx.author.dm_channel.send("Character created succesfully!")
    session.commit()
    session.close()


#TODO add database support for prefix!
@bot.command(name='stiltzkinprefix')
async def change_prefix(ctx, new_prefix):
    print(ctx.args)
    print(new_prefix)

    response = "Prefix changed to " + new_prefix
    print("Prefix changed : " + new_prefix)
    await ctx.send(response)

    bot.command_prefix = new_prefix



bot.run(TOKEN)
