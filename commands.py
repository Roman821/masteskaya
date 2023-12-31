import discord
from discord.ext import commands
from course_structure import *
from discord import ButtonStyle
from discord.ui import View, Button, Select

token = ''
intents = discord.Intents.default().all()
prefix = '!'
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command('help')

choice = ''
modul = ''
topic = ''
exercise = 0
project = ''
programmer = ''


def view_generation(dic):
    select = Select(placeholder='Выберите...')
    n = 1
    for i in dic:
        select.add_option(label=f'{n}. {i}', value=i)
        n += 1
    view = View()
    view.add_item(select)
    return view, select


@bot.group(invoke_without_command=True)
async def help(ctx):
    # global modul, topic, exercise, project, programmer
    # modul = ''
    # topic = ''
    # exercise = 0
    # project = ''
    # programmer = ''
    em = discord.Embed(title='help', description='Напиши !help <название команды>, чтобы узнать подробнее о ней',
                       color=0xff9900)
    em.add_field(name='Список команд', value='start, help, ask')
    await ctx.send(embed=em)


@help.command()
async def start(ctx):
    em = discord.Embed(title='start', description='!start позволяет узнать о боте',
                       color=0xff9900)
    em.add_field(name='Синтаксис', value='!start')
    await ctx.send(embed=em)


@help.command()
async def ask(ctx):
    em = discord.Embed(title='ask', description='!ask - команда чтобы задать вопрос',
                       color=0xff9900)
    em.add_field(name='Синтаксис', value='!ask')
    await ctx.send(embed=em)


@bot.command()
async def start(ctx):
    # global modul, topic, exercise, project, programmer
    # modul = ''
    # topic = ''
    # exercise = 0
    # project = ''
    # programmer = ''
    author = ctx.message.author  # Объявляем переменную author и записываем туда информацию об авторе.

    await ctx.send(f'Привет, {author.mention}!\n'
                   f'Это бот-помощник по курсу, напиши !help, чтобы ознакомиться с командами')


@bot.command()
async def ask(ctx):
    async def practicum_fun(interaction):
        async def topic_choose(interaction):
            async def exercise_choose(interaction):
                global topic
                topic = select_topics.values[0]
                if practicum_structure[modul][topic] == 0:
                    await interaction.response.send_message(f'В этой теме пока нет уроков. Пожалуйста, '
                                                            f'выберите другую тему')
                else:
                    await interaction.response.send_message(f'Введите номер урока (число от 1 до '
                                                            f'{practicum_structure[modul][topic]})')
            global modul
            modul = select_practicum.values[0]
            view_topics, select_topics = view_generation(practicum_structure[modul])
            select_topics.callback = exercise_choose
            await interaction.response.send_message(f'Выберите тему в модуле {modul}:', view=view_topics)

        global modul, topic, exercise
        modul = ''
        topic = ''
        exercise = 0
        view_practicum, select_practicum = view_generation(practicum_structure)
        select_practicum.callback = topic_choose
        await interaction.response.send_message('Выберите модуль:', view=view_practicum)

    async def project_fun(interaction):
        async def project_choose(interaction):
            async def choosen(interaction):
                global modul
                global project
                project = select_projects.values[0]
                global choice
                choice = f'Проект -> {modul} -> {project}'
                await interaction.response.send_message(f'Вы задали вопрос: {choice}. Подождите, идёт поиск ответов...')
                modul = ''
                project = ''
            global modul
            modul = select_modul.values[0]
            view_projects, select_projects = view_generation(projects_structure[modul])
            select_projects.callback = choosen
            await interaction.response.send_message('Выберите проект:', view=view_projects)
        view_modul, select_modul = view_generation(projects_structure)
        select_modul.callback = project_choose
        await interaction.response.send_message('Выберите модуль:', view=view_modul)

    async def programmer_fun(interaction):
        async def modul_choose(interaction):
            async def variant_choose(interaction):
                global modul
                global programmer
                programmer = select_programmer.values[0]
                global choice
                choice = f'Самоходный программист -> {modul} -> {programmer}'
                await interaction.response.send_message(f'Вы задали вопрос: {choice}. Подождите, идёт поиск ответов...')
                modul = ''
                programmer = ''
            global modul
            modul = select_modul.values[0]
            view_programmer, select_programmer = view_generation(programmer_list)
            select_programmer.callback = variant_choose
            await interaction.response.send_message('Выберите проект:', view=view_programmer)
        view_modul, select_modul = view_generation(projects_structure)
        select_modul.callback = modul_choose
        await interaction.response.send_message('Выберите модуль:', view=view_modul)

    button_practicum = Button(label='Тренажёр на платформе Практикума', style=ButtonStyle.blurple)
    button_project = Button(label='Проект', style=ButtonStyle.blurple)
    button_programmer = Button(label='Самоходный программист', style=ButtonStyle.blurple)
    button_practicum.callback = practicum_fun
    button_project.callback = project_fun
    button_programmer.callback = programmer_fun
    view = View()
    view.add_item(button_practicum)
    view.add_item(button_project)
    view.add_item(button_programmer)
    await ctx.send('Выбери тему вопроса:', view=view)


@bot.event
async def on_message(message):
    global choice
    if not message.author.bot and not message.content.startswith(prefix):
        global modul
        global topic
        if message.content.isdigit() and 0 < int(message.content) <= practicum_structure[modul][topic]:
            global exercise
            exercise = int(message.content)
            choice = f'Тренажёр на платформе Практикума -> {modul} -> {topic} -> {exercise} урок'
            await message.channel.send(f'Вы задали вопрос: {choice}. Подождите, идёт поиск ответов...')
            modul = ''
            topic = ''
            exercise = 0
        elif message.content.isdigit():
            await message.channel.send(f'Урока с номером {message.content} нет в этой теме. Может Вы ошиблись?')
        else:
            if modul and topic:
                await message.channel.send('Пожалуйста, введите номер урока числом')
            else:
                await message.channel.send('Общайтесь с ботом с помощью кнопок и команд')
    await bot.process_commands(message)

# @help.command()
# async def clear(ctx):
#   em = discord.Embed(title = 'clear', description = '!clear позволяет очистить сообщения и свой выбор',
#               color = 0xff9900)
#   em.add_field(name = 'Синтаксис', value = '!clear')
#  await ctx.send(embed = em)

# код для команды clear

# @bot.command()
# @commands.has_permissions(manage_messages=True)
# async def clear(ctx, amount = 20): #число 20 - это число удалённых сообщений, если число не указано
#  await ctx.channel.purge(limit = amount)

bot.run(token)
