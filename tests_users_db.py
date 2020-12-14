import pytest
import db_users
import os
import config as c



def test_create_database():
    database = "test_db.sqlite3"
    if os.path.isfile(database) and open(database).close():
        os.remove(database)

    try:
        test_db = db_users.UsersDataBase('test_db.sqlite3')
    finally:
        assert test_db.cursor is not None, "Не удалось создать базу данных пользователей"
    return test_db

def test_check_database():
    test_db = test_create_database()
    result = test_db.check_users_db()
    assert result is not None, "База данных пользователей пуста!"

def test_create_users():
    test_db = test_create_database()
    test_db.create_users()
    result = test_db.read_users()
    assert isinstance(result, list) is True, "Не удалось создать базу данных пользователей"

def test_read_users():
    pass

def test_add_new_user():
    name = 'test1'
    password = 'test_pass'
    test_db = db_users.UsersDataBase('test_db.sqlite3')
    test_db.create_users()
    test_db.add_new_user(name, password)
    result = test_db.read_users()
    assert (result[-1][1] == name and result[-1][2] == password) is True, \
        "Не удалось добавить нового пользователя"
    test_db.add_new_user('', '')
    result = test_db.read_users()
    assert (result[-1][1] != '' or result[-1][2] != '') is True, \
        "Поля 'имя' и 'пароль' должны быть заполнены!"


if __name__ == "__main__":
    pytest.main(["tests_users_db.py", "-v"])