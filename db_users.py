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

    def create_users(self):
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