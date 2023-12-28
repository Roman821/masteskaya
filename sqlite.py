import sqlite3

# Создание соединения и курсора для работы с базой данных
conn = sqlite3.connect('bot_database.db')
cursor = conn.cursor()

# Создание таблицы для модулей и тем
cursor.execute('''
    CREATE TABLE IF NOT EXISTS modules (
        id INTEGER PRIMARY KEY,
        module_name TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS topics (
        id INTEGER PRIMARY KEY,
        module_id INTEGER,
        topic_name TEXT,
        lesson_number INTEGER,
        project_type TEXT,
        task_name TEXT,
        FOREIGN KEY (module_id) REFERENCES modules(id)
    )
''')

# Создание таблицы для ответов на вопросы
cursor.execute('''
    CREATE TABLE IF NOT EXISTS answers (
        id INTEGER PRIMARY KEY,
        topic_id INTEGER,
        response_text TEXT,
        FOREIGN KEY (topic_id) REFERENCES topics(id)
    )
''')

# Пример добавления данных в таблицы (можно адаптировать под ваши нужды)
# Добавление модулей
cursor.execute('INSERT INTO modules (module_name) VALUES (?)', ('Тренажëр',))
cursor.execute('INSERT INTO modules (module_name) VALUES (?)', ('Проект',))
cursor.execute('INSERT INTO modules (module_name) VALUES (?)', ('Самоходный программист',))

# Добавление тем и ответов на вопросы
cursor.execute('''
    INSERT INTO topics (module_id, topic_name, lesson_number, project_type, task_name)
    VALUES (?, ?, ?, ?, ?)
''', (1, 'Название темы тренажëра', 1, None, None))

cursor.execute('''
    INSERT INTO answers (topic_id, response_text)
    VALUES (?, ?)
''', (1, 'Ответ на вопрос о тренажëре'))

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()
