"""
Модуль для работы с базой данных пользователей
"""

import sqlite3
from sqlite3 import Error


class UsersDataBase:
    def __init__(self, database):
        self.database = database
        try:
            self.database_connect = sqlite3.connect(self.database)
            print(f"Соединение с базой данных {database} установлено")
        except Error:
            print(f"Ошибка {Error} соединения с базой данных")
        self.cursor = self.database_connect.cursor()

    def check_users_db(self):
        """
        Проверка наличия данных в таблице пользователей
        :return: False, если таблица пуста
        """
        query = "SELECT name " \
                "FROM sqlite_master " \
                "WHERE type='table' AND name='users'"
        self.cursor = self.database_connect.execute(query)
        result = self.cursor.fetchone()
        return result

    def create_users(self):
        """
        Создание таблицы пользователей в базе данных
        id - числовой идентификатор пользователя
        login - имя пользователя
        password - пароль пользователя
        """

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
        :return: кортеж с информацией о пользователе (id, login, password)
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
        :return: тестовый режим - запись в БД не происходит (дабы не захламлять)
        """
        self.cursor.executemany(""" INSERT INTO users
                            VALUES(?, ?, ?) """, [(None, new_user, new_password)])

    def database_close(self):
        """
        Закрытие базы данных
        """
        self.cursor.close()


if __name__ == "__main__":
    db = UsersDataBase("users.sqlite3")
    db.create_users()

    for user in db.read_users():
        print(user[1])

    db.database_close()