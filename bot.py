import discord
from discord.ext import commands

intents = discord.Intents.default() # Подключаем "Разрешения"
intents.message_content = True

bot = commands.Bot(commandprefix='!', intents=intents)

@bot.command()
async def test(ctx):
    await ctx.send('Бот работает!')

bot.run('MTE4NzAyNTU5MjIxNDg4MDMyNw.G4a-I.2302WyvokUhUs3rU5toG7OJhGJPaMV1S3AA5kI')
