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
        ''')

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

    def find_answer(self, module, topic, exercise, project, programmer, question):
        self.cursor.execute('''
            SELECT a.response_text
            FROM answers a
            JOIN topics t ON a.topic_id = t.id
            WHERE t.topic_name = ? AND a.project_type = ? AND a.task_name = ? AND a.programmer_name = ?
        ''', (topic, project, exercise, programmer))
        result = self.cursor.fetchone()

        return result[0] if result else None

    def insert_answer(self, module, topic, exercise, project, programmer, response):
        self.cursor.execute('''
            INSERT INTO answers (topic_id, response_text, project_type, task_name, programmer_name)
            SELECT t.id, ?, ?, ?, ?
            FROM topics t
            WHERE t.topic_name = ?
        ''', (response, project, exercise, programmer, topic))

        self.conn.commit()

    def close(self):
        self.conn.close()
