import sqlite3

class Database:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS modules (
                id INTEGER PRIMARY KEY,
                module_name TEXT
            ) 
        ''') # TODO Вообще все вот эти вот настройки базы стоило вынести в отдельный метод setup_db() скажем
        # Чтоб в ините такой срач не разводить

        self.cursor.execute('''
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

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS answers (
                id INTEGER PRIMARY KEY,
                topic_id INTEGER,
                project_type TEXT,
                response_text TEXT,
                task_name TEXT,
                programmer_name TEXT,
                FOREIGN KEY (topic_id) REFERENCES topics(id)
            )
        ''')

        self.conn.commit()
    # TODO Не используете module и question, да и по итогу как-то очен ьмного переменных дернуто
        
    def find_answer(self, module, topic, exercise, project, programmer, question):
        self.cursor.execute('''
            SELECT a.response_text
            FROM answers a
            JOIN topics t ON a.topic_id = t.id
            WHERE t.topic_name = ? AND a.project_type = ? AND a.task_name = ? AND a.programmer_name = ?
        ''', (topic, project, exercise, programmer)) # TODO в запросе вышел какой-то огроменный where
        result = self.cursor.fetchone()

        return result[0] if result else None # TODO Хорошо кстати, аж глаз радуется

    def insert_answer(self, module, topic, exercise, project, programmer, response):
        self.cursor.execute('''
            INSERT INTO answers (topic_id, response_text, project_type, task_name, programmer_name)
            SELECT t.id, ?, ?, ?, ?
            FROM topics t
            WHERE t.topic_name = ?
        ''', (response, project, exercise, programmer, topic)) 
        # TODO Я понимаю что мы мягко говоря очень далеко за рамками курса сейчас, и мне нравится что вы
        # не побоялись залезть с головой в это!
        # Я это вообще все к чему, я думаю тут сильно нормальность бд порушена, но особо не вдавался,
        # в любом случае я бы посоветовал почитать про виды нормальности реляционных бд, на хабре есть статья на русском
        self.conn.commit()

    def close(self):
        self.conn.close()
