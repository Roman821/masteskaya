
bot.remove_command('help')

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
    await ctx.send(embed = em)

@bot.command()
async def start(ctx):
    author = ctx.message.author # Объявляем переменную author и записываем туда информацию об авторе.

    await ctx.send(f'Привет, {author.mention}!\n'
                   f'Это бот-помощник по курсу, напиши !help, чтобы ознакомиться с командами')



#@help.command()
#async def clear(ctx):
 #   em = discord.Embed(title = 'clear', description = '!clear позволяет очистить сообщения и свой выбор',
        #               color = 0xff9900)
 #   em.add_field(name = 'Синтаксис', value = '!clear')
  #  await ctx.send(embed = em)

#код для команды clear

#@bot.command()
#@commands.has_permissions(manage_messages=True)
#async def clear(ctx, amount = 20): #число 20 - это число удалённых сообщений, если число не указано
  #  await ctx.channel.purge(limit = amount)

