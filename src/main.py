from random import randint
from datetime import datetime, timedelta

from discord.ext import commands
import discord

from constants import token

intents = discord.Intents.default()
bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True, # Commands aren't case-sensitive
    intents = intents # Set up basic permissions
)

bot.author_id = 601345051502837780  # Change to your discord id

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

@bot.command()
async def pong(ctx):
    await ctx.send('pong')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

## WARMUP
### Warm-up 1
@bot.command()
async def name(ctx):
    await ctx.send(ctx.author.name)

### Warm-up 2
@bot.command()
async def d6(ctx):
    await ctx.send(randint(1,6))

### Warm-up 3
@bot.event
async def on_message(message):
    if message.content == "Salut tout le monde":
        await message.channel.send("Salut tout seul")
        await message.channel.send(message.author.mention)
    await bot.process_commands(message)

## ADMINISTRATION
### Administration 1

@bot.command()
async def admin(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Admin")
    if role is None:
        await ctx.guild.create_role(name="Admin", permissions=discord.Permissions.all())
        await ctx.send("Admin role created")
        role = discord.utils.get(ctx.guild.roles, name="Admin")
    await member.add_roles(role)
    await ctx.send("Admin role given to " + member.name)

### Administration 2
funny_reasons = ["you don't slay", "my starbucks is cold", "I don't like your profile picture", "you said Beyonce is overrated", "you said one direction was just a phase"]

@bot.command()
async def ban(ctx, member: discord.Member, reason=None):
    if reason is None:
        await ctx.send(f"{member.name}, you were banned because {funny_reasons[randint(0, len(funny_reasons)-1)]}")
    else:
        await ctx.send(f"{member.name}, you were  banned because {reason}")
    await member.ban(reason=reason)

### Administration 3

flood_active = True
last_warning = None
X_messages = 2
Y_minutes = 2

@bot.command()
async def flood(ctx):
    print("flood")
    global flood_active
    flood_active = not flood_active
    if flood_active:
        await ctx.send("Flood activated")
    else:
        await ctx.send("Flood deactivated")
    
@bot.event
async def on_message(message):
    global last_warning
    global flood_active
    global X_messages
    global Y_minutes
    if flood_active:
        # get current author, channel and messages from author in the last Y minutes
        author = message.author
        channel = message.channel
        time_threshold = datetime.utcnow() - timedelta(minutes=Y_minutes)
        
        messages = []
        async for msg in channel.history(before=time_threshold):
            if msg.author == author:
                messages.append(msg)
        if len(messages) >= X_messages and (last_warning == None or last_warning + timedelta(minutes=Y_minutes) < datetime.utcnow()):
            last_warning = datetime.utcnow()
            await channel.send(f"{author.mention}, STOP SENDING MESSAGES, NO ONE CARES ABOUT YOUR OPINION.")
    await bot.process_commands(message)

## FUN AND GAMES
### Fun and games 1
@bot.command()
async def xkcd(ctx):
    await ctx.send("https://xkcd.com/" + str(randint(10, 2001)))

### Fun and games 2

@bot.command()
async def poll(ctx, question):
    message = await ctx.send("@here " +question)
    await message.add_reaction("👍")
    await message.add_reaction("👎")

bot.run(token)  # Starts the bot
