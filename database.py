"""
Модуль для работы с базой данных
"""

import sqlite3
from sqlite3 import Error


class DataBase:
    def __init__(self, database):
        self.database = database
        try:
            self.database_connect = sqlite3.connect(self.database)
            print(f"Соединение с базой данных {database} установлено")
        except Error:
            print(f"Ошибка {Error} соединения с базой данных")
        self.cursor = self.database_connect.cursor()

    def create_users_database(self):
        """
        Создание таблицы пользователей в базе данных
        id - числовой идентификатор пользователя
        login - имя пользователя
        password - пароль пользователя
        """
        try:
            self.cursor.execute(""" DROP TABLE users """)
        except sqlite3.OperationalError:
            print("Отсутствует база данных пользователей")

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
            id integer PRIMARY KEY AUTOINCREMENT,
            login text, 
            password text 
            )""")

        self.cursor.executemany(""" INSERT INTO users
                    VALUES(?, ?, ?) """,
                    [(None, f'user{i}', f'pass{i}') for i in range(1, 4)])

        self.database_connect.commit()

    def read_users(self):
        """
        Чтение из БД сведений о пользователях
        :return: список кортежей с информацией о пользователе (id, login, password)
        """
        self.cursor.execute("""
                    SELECT * 
                    FROM users
                    ORDER BY id
                    """)
        data = self.cursor.fetchall()
        return data

    def add_new_user(self, new_user, new_password):
        """
        Добавление нового пользователя в БД
        :param new_user: имя нового пользователя
        :param new_password: пароль нового пользователя
        :return: тестовый режим - запись в БД не происходит (дабы не захломлять)
        """
        self.cursor.executemany(""" INSERT INTO users
                            VALUES(?, ?, ?) """,
                                [(None, new_user, new_password)])

    def create_tests_database(self):

        try:
            self.cursor.execute(""" DROP TABLE tests """)
        except sqlite3.OperationalError:
            print("Отсутствует база данных пользователей")

        create_tests_table_sql = """
                    CREATE TABLE IF NOT EXISTS tests(
                    id integer,
                    name text, 
                    questions text,
                    answers text -- not needed!
                    )"""
        create_answers_table_sql = """
                    create table if not exists answers(
                        id integer,
                        answer text,
                        testId integer,
                        is_right integer
                    )"""

        self.cursor.execute(create_tests_table_sql)
        self.cursor.execute(create_answers_table_sql)

        test_name = ["География", "Путешествия"]
        questions = [["Какое государство самое маленькое в мире?",
                     "Назовите наибольшее по площади озеро Америки",
                     "Чья экспедиция совершила первое кругосветное путешествие?"],

                     ["Какой из перечисленных вулканов является действующим?",
                      "Когда отмечается всемирный день туризма?",
                      "Как называют людей, отдыхающих на курорте без путевки?"]]

        answers = [[["Ватикан", "Лихтенштейн", "Монако", "Андорра"],
                   ["Верхнее", "Гурок", "Мичиган", "Онтарио"],
                   ["Магеллана", "Врангеля", "Лисянского", "Кука"]],

                   [["Везувий", "Килиманджаро", "Карадаг", "Кетой"],
                    ["27 сентября", "1 июня", "6 июля", "15 мая"],
                    ["Дикари", "Туземцы", "Варвары", "Отшельники"]]]

        # insert data into DB
        self.cursor.executemany(""" INSERT INTO tests
                            VALUES(?, ?, ?, ?) """,
                            [(k, test_name[k], questions[k][i], '+'.join(answers[k][i])) for i in range(3) for k in range(2)])

        self.database_connect.commit()

    # -- created by Dimon :)
    def create_tests_database_ver2(self):

        tables = ["answers", "questions"]
        for table in tables:
            try:
                self.cursor.execute(""" DROP TABLE """ + table)
            except sqlite3.OperationalError:
                print("Отсутствует база данных пользователей")

        create_tests_table_sql = """
                    CREATE TABLE IF NOT EXISTS questions(
                    id integer,
                    topic text, 
                    question text
                    )"""
        create_answers_table_sql = """
                    create table if not exists answers(
                        id integer,
                        answer text,
                        questionId integer,
                        is_right integer
                    )"""

        self.cursor.execute(create_tests_table_sql)
        self.cursor.execute(create_answers_table_sql)

        questionnaire = [
            ("География", "Какое государство самое маленькое в мире?", ["Ватикан", "Лихтенштейн", "Монако", "Андорра"], 0),
            ("География", "Назовите наибольшее по площади озеро Америки", ["Верхнее", "Гурок", "Мичиган", "Онтарио"], 0),
            ("География", "Чья экспедиция совершила первое кругосветное путешествие?", ["Магеллана", "Врангеля", "Лисянского", "Кука"], 0),
            ("Путешествия", "Какой из перечисленных вулканов является действующим?", ["Везувий", "Килиманджаро", "Карадаг", "Кетой"], 0),
            ("Путешествия", "Когда отмечается всемирный день туризма?", ["27 сентября", "1 июня", "6 июля", "15 мая"], 0),
            ("Путешествия", "Как называют людей, отдыхающих на курорте без путевки?", ["Дикари", "Туземцы", "Варвары", "Отшельники"], 0),
            ("new topic", "new question", ["var1", "var2"], 1)
        ]

        # select data: select * from questions q inner join answers a on q.id = a.questionId;

        counter = 1
        for test in questionnaire:
            print("===> ", test[0])
            insert_into_questions = """insert into questions values(?, ?, ?)"""
            self.cursor.execute(insert_into_questions, [counter, test[0], test[1]])

            answers_counter = 1
            for answer in test[2]:
                insert_into_answers = """insert into answers values(?, ?, ?, ?)"""

                is_right = 0
                if answers_counter - 1 == test[3]:
                    is_right = 1

                self.cursor.execute(insert_into_answers, [answers_counter, answer, counter, is_right])
                answers_counter += 1

            counter += 1

        self.database_connect.commit()

    def read_name_tests(self, filter):
        self.cursor.execute(f"""
                            SELECT DISTINCT {filter}
                            FROM tests
                            ORDER BY id
                            """)
        data = self.cursor.fetchall()
        return data

    def database_close(self):
        """
        Закрытие базы данных
        """
        self.cursor.close()


if __name__ == "__main__":
    db = DataBase("tests.sqlite3")
    db.create_users_database()
    db.create_tests_database()

    db.create_tests_database_ver2()

    for user in db.read_users():
        print(*user)
    for test in db.read_name_tests('id, name, questions, answers'):
        print(test)

    print(db.read_users())
    db.database_close()