import discord # Подключаем библиотеку
from discord.ext import commands

intents = discord.Intents.default() # Подключаем "Разрешения"
intents.message_content = True
Задаём префикс и интенты
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')
С помощью декоратора создаём первую команду
@bot.group(invoke_without_command = True)
async def help(ctx):
    em = discord.Embed(title = 'help', description = 'Напиши !help <название команды>, чтобы узнать подробнее о ней',
                       color = 0xff9900)
    em.add_field(name = 'Список команд', value = 'start, help')
    await ctx.send(embed = em)

@help.command()
async def start(ctx):
    em = discord.Embed(title = 'start', description = '!start позволяет узнать о боте',
                       color = 0xff9900)
    em.add_field(name = 'Синтаксис', value = '!start')

@bot.command() 
async def start(ctx): 
    author = ctx.message.author # Объявляем переменную author и записываем туда информацию об авторе.

    await ctx.send(f'Привет, {author.mention}!\n'
                   f'Это бот-помощник по курсу, напиши !help, чтобы ознакомиться с командами')



#@help.command()
#async def clear(ctx):
 #   em = discord.Embed(title = 'clear', description = '!clear позволяет очистить сообщения и свой выбор',
        #               color = 0xff9900)
 #   em.add_field(name = 'Синтаксис', value = 'start, help')


#код для команды clear

#@bot.command()
#@commands.has_permissions(managemessages=True)
#async def clear(ctx, amount = 20): #число 20 - это число удалённых сообщений, если число не указано
  #  await ctx.channel.purge(limit = amount)

bot.run('MTE4NzAyNTU5MjIxNDg4MDMyNw.G4a-I.2302WyvokUhUs3rU5toG7OJhGJPaMV1S3AA5kI')
