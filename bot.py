import os
import discord
from discord.ext import commands
from database import session, Countdown


token = os.environ.get("TOKEN", "")

bot = commands.Bot(command_prefix="!")

startup_extensions = ["countdown"]

for extension in startup_extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Failed to load extension {}\n{}'.format(extension, exc))


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="!help cd"))
    print(f"Connected!\nName: {bot.user.name}\nId: {bot.user.id}\n")


bot.run(token)
