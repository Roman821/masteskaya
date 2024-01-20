import asyncio
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import ButtonStyle
from discord.ui import View, Button, Select
from database import Database
from course_structure import * # TODO вот так лучше не импортировать, ты сразу же теряешься че ты там импортируешь и тд


class Question:
    def __init__(self):
        self.choice = ''
        self.module = ''
        self.topic = ''
        self.exercise = 0
        self.project = ''
        self.programmer = ''
#TODO Вот это тоже надо бы вытащить в отдельный файл

load_dotenv()

token = os.getenv('DISCORD_TOKEN') # TODO Вообще стоило все переменные, которые зависят от окружения
# вынести в отдельный файл. Тот же префикс, токен, путь до базы, айдишники админов, айдишник канала
intents = discord.Intents.default().all()
prefix = '!'
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command('help')
question = Question() # TODO и у нас получается один вопрос на всех пользователей?
database = Database('bot_database.db')  # Создаем экземпляр класса Database


def view_generation(dic): #TODO WALTER.... Я вообще не понял че за dic
    select = Select(placeholder='Выберите...')
    for n, i in enumerate(dic, start=1):
        select.add_option(label=f'{n}. {i}', value=i)
    view = View()
    view.add_item(select)
    return view, select # TODO А сам селект зачем еще возвращать?


async def background_task(coro, *args, **kwargs):
    loop = asyncio.get_event_loop() # TODO Вау, пока не нашел зачем вам собственный луп, но круто
    return await loop.create_task(coro(*args, **kwargs))


@bot.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title='help', description='Напиши !help <название команды>, чтобы узнать подробнее о ней',
                       color=0xff9900)
    em.add_field(name='Список команд', value='start, help, ask')
    await ctx.send(embed=em)


@help.command()
async def start(ctx):
    em = discord.Embed(title='start', description='!start позволяет узнать о боте', color=0xff9900)
    em.add_field(name='Синтаксис', value='!start')
    await ctx.send(embed=em)


@help.command()
async def ask(ctx):
    em = discord.Embed(title='ask', description='!ask - команда чтобы задать вопрос', color=0xff9900)
    em.add_field(name='Синтаксис', value='!ask')
    await ctx.send(embed=em)


@bot.command()
async def start(ctx):
    author = ctx.message.author
    await ctx.send(
        f'Привет, {author.mention}!\nЭто бот-помощник по курсу, напиши !help, чтобы ознакомиться с командами')


@bot.command()
async def ask(ctx):
    async def practicum_fun(interaction): # TODO Так и не вынесли это в отдельный файл/место, читается ну прям жесть тяжело
        async def topic_choose(interaction):
            async def exercise_choose(interaction):
                question.topic = select_topics.values[0]
                #TODO две квардратные скобки подряд тоже лучше не допускать, practicum_structure кстати сломался
                if practicum_structure[question.module][question.topic] == 0:
                    await interaction.response.send_message(
                        f'В этой теме пока нет уроков. Пожалуйста, выберите другую тему')
                else:
                    await interaction.response.send_message(
                        f'Введите номер урока (число от 1 до {practicum_structure[question.module][question.topic]})')

            question.module = select_practicum.values[0]
            view_topics, select_topics = view_generation(practicum_structure[question.module])
            select_topics.callback = exercise_choose
            await interaction.response.send_message(f'Выберите тему в модуле {question.module}:', view=view_topics)

        question.module = ''
        question.topic = ''
        question.exercise = 0
        try:
            view_practicum, select_practicum = view_generation(practicum_structure)
            select_practicum.callback = topic_choose
            await interaction.response.send_message('Выберите модуль:', view=view_practicum)
        except Exception as e: # TODO Лучше не жрать так все ошибки, напоминаю!
            print(f'An error occurred in practicum_fun: {e}')

    async def project_fun(interaction):
        async def project_choose(interaction):
            async def choosen(interaction):
                question.project = select_projects.values[0]
                question.choice = f'Проект -> {question.module} -> {question.project}'
                await interaction.response.send_message(
                    f'Вы задали вопрос: {question.choice}. Подождите, идёт поиск ответов...')
                question.module = ''
                question.project = ''

            question.module = select_modul.values[0]
            view_projects, select_projects = view_generation(projects_structure[question.module])
            select_projects.callback = choosen
            await interaction.response.send_message('Выберите проект:', view=view_projects)

        question.module = ''
        question.project = ''
        try:
            view_modul, select_modul = view_generation(projects_structure)
            select_modul.callback = project_choose
            await interaction.response.send_message('Выберите модуль:', view=view_modul)
        except Exception as e:
            print(f'An error occurred in project_fun: {e}')
    #TODO Все вот эти функции в итоге вообще один в один по логике, стоило сделать ее одну
    async def programmer_fun(interaction):
        async def modul_choose(interaction):
            async def variant_choose(interaction):
                question.programmer = select_programmer.values[0]
                question.choice = f'Самоходный программист -> {question.module} -> {question.programmer}'
                await interaction.response.send_message(
                    f'Вы задали вопрос: {question.choice}. Подождите, идёт поиск ответов...')
                question.module = ''
                question.programmer = ''

            question.module = select_modul.values[0]
            view_programmer, select_programmer = view_generation(programmer_list)
            select_programmer.callback = variant_choose
            await interaction.response.send_message('Выберите проект:', view=view_programmer)

        question.module = ''
        question.programmer = ''
        try:
            view_modul, select_modul = view_generation(projects_structure)
            select_modul.callback = modul_choose
            await interaction.response.send_message('Выберите модуль:', view=view_modul)
        except Exception as e:
            print(f'An error occurred in programmer_fun: {e}')

    button_practicum = Button(label='Тренажёр на платформе Практикума', style=ButtonStyle.blurple)
    button_project = Button(label='Проект', style=ButtonStyle.blurple)
    button_programmer = Button(label='Самоходный программист', style=ButtonStyle.blurple)
    button_practicum.callback = practicum_fun
    button_project.callback = project_fun
    button_programmer.callback = programmer_fun
    # TODO У вас же есть функция которая уже генерирует вью, 34я строка
    view = View()
    view.add_item(button_practicum)
    view.add_item(button_project)
    view.add_item(button_programmer)

    await ctx.send('Выберите курс:', view=view)


@bot.command()
async def question(ctx):
    async def callback(interaction):
        question.exercise = int(interaction.data['values'][0])
        question.choice = f'{question.module} -> {question.topic} -> Урок {question.exercise}'
        await interaction.response.send_message(
            f'Вы задали вопрос: {question.choice}. Подождите, идёт поиск ответов...')
        question.module = ''
        question.topic = ''
        question.exercise = 0

    if not all([question.module, question.topic]):
        await ctx.send('Сначала выберите модуль и тему с упражнением')
    else:
        try:
            view_exercise, input_exercise = view_generation(
                list(range(1, practicum_structure[question.module][question.topic] + 1)))
            input_exercise.callback = callback
            await ctx.send('Введите номер урока:', view=view_exercise)

            # Асинхронно выполним фоновую задачу по поиску ответа
            await background_task(database.find_answer,
                                  question.module, question.topic, question.exercise,
                                  question.project, question.programmer, ctx.message.content)
        except Exception as e:
            print(f'An error occurred in question command: {e}')


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message) # TODO Лучше было вынести это в отдельную команду, чтобы сервера лишний раз не дергать


@bot.event
async def on_ready():
    print(f'Бот подключен к Discord как {bot.user.name} (ID: {bot.user.id})')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Такой команды не существует. Напишите `!help`, чтобы увидеть доступные команды.')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            'Вы забыли указать аргументы команды. Напишите `!help`, чтобы увидеть примеры использования команд.')
    else:
        await ctx.send(f'Произошла ошибка: {error}')


@bot.event
async def on_interaction(interaction):
    if interaction.type == discord.InteractionType.component: # TODO Видимо какая-то заглушка, стоило тогда ее удалить/не нести в мастер
        # Код для обработки взаимодействий с компонентами
        if interaction.data['component_type'] == discord.ComponentType.button:
            # Обработка кнопок
            pass
        elif interaction.data['component_type'] == discord.ComponentType.select:
            # Обработка выпадающих списков
            pass


@bot.command()
async def asck(ctx): # TODO команда так и называется asck?
    if not question.choice:
        await ctx.send('Для начала воспользуйтесь командой `!ask`')
    else:
        answer = await bot.loop.run_in_executor(None, database.find_answer, question.module, question.topic,
                                                question.exercise, question.project, question.programmer,
                                                ctx.message.content)
        if answer:
            await ctx.send(f'Вот ответ на ваш вопрос: {answer}')
        else:
            # Отправка вопроса на канал для наставника TODO Стоило вынести айдишник в константу сверху, я мог ее вполне тут и не найти
            mentor_channel_id = 1195277379212423239  # Замените на ID вашего канала для наставника
            mentor_channel = ctx.guild.get_channel(mentor_channel_id)
            if mentor_channel:
                await mentor_channel.send(f'Вопрос от {ctx.author.mention}: {ctx.message.content}')
                await ctx.send(
                    'Ответа на ваш вопрос нет в базе. Вопрос был передан наставнику. Пожалуйста, ожидайте ответа.')
            else:
                await ctx.send('Не удалось найти канал для наставника. Пожалуйста, настройте канал для наставника.')


@bot.command()
async def add_answer(ctx, module, topic, exercise, project, programmer, response):
    # Проверка, является ли автор сообщения администратором
    if ctx.message.author.id not in [1124225406522888244]: #TODO Аналогично с айдишниками юзеров
        await ctx.send("У вас нет прав для выполнения этой команды.")
        return

    # Вставка нового ответа в базу данных
    await bot.loop.run_in_executor(None, database.insert_answer, module, topic, exercise, project, programmer, response)

    await ctx.send("Ответ успешно добавлен в базу данных.")


@bot.event
async def on_disconnect():
    database.close()


bot.run(token)
# TODO Оверол, очень не хватает модульности, очень сильно хромает читаемость из-за этого. По факту вышел
# огроменный файл на ~300 строк, который стоило разнести точно файлов на 5.
# И обратите огромное внимание на вложенные функции друг в друга, это ну просто очень сложно читать!
# Если нужны какие-то объяснения,, не стесняйтесь писать, задавать вопросы, разберемся во всем обязательно
