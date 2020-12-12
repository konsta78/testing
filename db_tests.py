"""
Модуль для работы с базой данных
"""

import sqlite3
from sqlite3 import Error
import questionnaire as q


class TestsDataBase:
    def __init__(self, database):
        self.database = database
        try:
            self.database_connect = sqlite3.connect(self.database)
            print(f"Соединение с базой данных {database} установлено")
        except Error:
            print(f"Ошибка {Error} соединения с базой данных")
        self.cursor = self.database_connect.cursor()

    def check_tests_db(self):
        """
        Проверка наличия данных в таблицах с вопросами и ответами
        :return: False, если таблицы пусты
        """
        tables = ["answers", "questions"]
        for table in tables:
            query = f"SELECT name " \
                    "FROM sqlite_master " \
                    f"WHERE type='table' AND name='{table}'"
            self.cursor = self.database_connect.execute(query)
            result = self.cursor.fetchone()
        return result

    def create_tests(self):
        """
        Создание базы данных с тестами. Две таблицы: 'answers' и 'questions'.
        """

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

        counter = 1
        for item in q.questionnaire:
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

    def get_topics(self, filter):
        """
        Получение списка тем для тестирования из БД по фильтру запроса
        :param filter: поле в БД
        :return: кортеж с данными
        """
        self.cursor.execute(f"""
                            SELECT DISTINCT {filter} 
                            FROM questions
                            """)
        data = self.cursor.fetchall()
        return data

    def get_questions(self, topic):
        """
        Получение списка вопросов по выбранной теме тестирования
        :param topic: тема для тестирования
        :return: кортеж с данными
        """
        self.cursor.execute(f"""
                            SELECT question 
                            FROM questions
                            WHERE topic=?
                            """, (topic,))
        data = self.cursor.fetchall()
        return data

    def get_answers_for_question(self, question):
        """
        Получения списка вариантов ответа для текущего вопроса
        :param question: вопрос теста
        :return: кортеж с данными
        """
        self.cursor.execute(f"""
                            SELECT a.answer 
                            FROM questions q INNER JOIN answers a 
                            ON q.id = a.questionId AND q.question=?
                            ORDER BY a.id;
                            """, (question, ))
        data = self.cursor.fetchall()
        return data

    def get_right_answers(self, topic):
        self.cursor.execute(f"""
                            SELECT a.answer
                            FROM questions q INNER JOIN answers a 
                            ON q.id = a.questionId AND q.topic=? AND a.is_right=1;
                            """, (topic,))
        data = self.cursor.fetchall()
        return data

    def database_close(self):
        """
        Закрытие базы данных
        """
        self.cursor.close()


if __name__ == "__main__":
    db = TestsDataBase("tests.sqlite3")
    if db.check_tests_db() is None:
        db.create_tests()
    # db.shake_answers()
    # for item in db.get_topics('topic'):
    #     print(item[0])
    # for test in db.get_questions('Путешествия'):
    #     print(test)
    # answers = db.get_answers_for_question('Какое государство самое маленькое в мире?')
    # print(answers)
    # answers = [answers[i][0] for i in range(0, len(answers))]
    # print(answers)

    # for test in db.get_answers_for_question('Какое государство самое маленькое в мире?'):
    #     print(test[4])
    right_answers = db.get_right_answers('География')
    print(right_answers)
    # for test in db.get_right_answers('География'):
    #     print(test)

    db.database_close()