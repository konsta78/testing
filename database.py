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
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tests(
                    id integer,
                    name text, 
                    questions text,
                    answers text 
                    )""")
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

        self.cursor.executemany(""" INSERT INTO tests
                            VALUES(?, ?, ?, ?) """,
                            [(k, test_name[k], questions[k][i], '+'.join(answers[k][i])) for i in range(3) for k in range(2)])
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
    for user in db.read_users():
        print(*user)
    for test in db.read_name_tests('id, name, questions, answers'):
        print(test)

    print(db.read_users())
    db.database_close()