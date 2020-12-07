"""
Функции для работы с БД и сервисом тестирования
"""
import messages as m


def input_command_menu(count, message):
    answer = 0
    while answer not in range(1, count):
        try:
            answer = int(input(message))
        except ValueError:
            print("Неверный формат ввода!")
    return answer


def authorization(database):
    """
    Авторизация пользователя для запуска сервиса тестирования
    :param database: база данных
    :return: user_id: уникальный идентификатор пользователя (id)
    """
    user_name = None
    user_id = None

    def show_menu():
        """
        Отображение меню авторизации
        :return: answer: номер команды меню
        """
        print("В нашей базе данных зарегистрированы следующие пользователи: ")
        for user in database.read_users():
            print(user[1])
        answer = input_command_menu(4, m.mg_start)
        return answer

    def new_user():
        """
        Добавление нового пользователя в базу данных
        :return: user_id: уникальный идентификатор нового пользователя (id)
        """
        print("Регистрация нового пользователя")
        user = str(input("\nВведите имя пользователя: "))
        password = str(input("Введите пароль: "))
        database.add_new_user(user, password)
        user_id = database.read_users()[-1][0]
        print(f"\n{user}, регистрация завершена.\n"
              f"Доступ к сервису тестирования разрешен. Ваш id - {user_id}")
        return user_id, user

    def loging():
        """
        Авторизация ранее зарегистрированного пользователя
        :return: user_id: уникальный идентификатор пользователя (id)
        """

        user = str(input("\nВведите имя пользователя: "))
        for item in database.read_users():
            if user == item[1]:
                password = str(input("Введите пароль: "))
                if password == item[2]:
                    user_id = int(item[0])
                    print(f"\n{user}, доступ к сервису тестирования разрешен. Ваш id - {user_id}")
                    return user_id, user
                else:
                    print("Неверный пароль!")
                    return None, None
        print("Такого пользователя не существует!")
        return None, None

    while not isinstance(user_id, int):
        answer = show_menu()
        if answer == 1:
            user_id, user_name = loging()
        elif answer == 2:
            user_id, user_name = new_user()
        else:
            user_id = 0

    return user_id, user_name


def choose_test(database):
    print(f"Выберите тему для тестирования:")
    for test in database.read_name_tests('id, name'):
        print(f"{test[0]+1}. {test[1]}")