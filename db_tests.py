"""
Модуль для работы с базой данных
"""

import sqlite3
from sqlite3 import Error


class TestsDataBase:
    def __init__(self, database):
        self.database = database
        try:
            self.database_connect = sqlite3.connect(self.database)
            print(f"Соединение с базой данных {database} установлено")
        except Error:
            print(f"Ошибка {Error} соединения с базой данных")
        self.cursor = self.database_connect.cursor()

    def create_tests(self):

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
                    CREATE TABLE IF NOT EXISTS answers(
                        id integer,
                        answer text,
                        questionId integer,
                        is_right integer
                    )"""

        self.cursor.execute(create_tests_table_sql)
        self.cursor.execute(create_answers_table_sql)

        questionnaire = [
            ("География", "Какое государство самое маленькое в мире?",
                ["Ватикан", "Лихтенштейн", "Монако", "Андорра"], 0),
            ("География", "Назовите наибольшее по площади озеро Америки",
                ["Верхнее", "Гурок", "Мичиган", "Онтарио"], 0),
            ("География", "Чья экспедиция совершила первое кругосветное путешествие?",
                ["Магеллана", "Врангеля", "Лисянского", "Кука"], 0),
            ("Путешествия", "Какой из перечисленных вулканов является действующим?",
                ["Везувий", "Килиманджаро", "Карадаг", "Кетой"], 0),
            ("Путешествия", "Когда отмечается всемирный день туризма?",
                ["27 сентября", "1 июня", "6 июля", "15 мая"], 0),
            ("Путешествия", "Как называют людей, отдыхающих на курорте без путевки?",
                ["Дикари", "Туземцы", "Варвары", "Отшельники"], 0)
        ]

        counter = 1
        for item in questionnaire:
            insert_into_questions = """INSERT INTO questions VALUES(?, ?, ?)"""
            self.cursor.execute(insert_into_questions, [counter, item[0], item[1]])

            answers_counter = 1
            for answer in item[2]:
                insert_into_answers = """INSERT INTO answers VALUES(?, ?, ?, ?)"""
                is_right = 0
                if answers_counter - 1 == item[3]:
                    is_right = 1
                self.cursor.execute(insert_into_answers, [answers_counter, answer, counter, is_right])
                answers_counter += 1

            counter += 1
        self.database_connect.commit()

    def read_data_from_tests(self, filter):
        # select data: select * from questions q inner join answers a on q.id = a.questionId;

        self.cursor.execute(f"""
                            SELECT DISTINCT {filter} 
                            FROM questions
                            """)
        data = self.cursor.fetchall()
        return data

    def database_close(self):
        """
        Закрытие базы данных
        """
        self.cursor.close()


if __name__ == "__main__":
    db = TestsDataBase("tests.sqlite3")
    db.create_tests()

    for test in db.read_data_from_tests('topic'):
        print(test[0])

    db.database_close()