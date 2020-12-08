"""
Функции для работы с БД и сервисом тестирования
"""
import messages as m


def input_command_menu(count, message, answer=0):
    """
    Отображение меню с вариантами ответа пользователя
    :param count: кол-во пунктов в меню
    :param message: текст сообщений в меню
    :param answer: пункт меню, выбранный пользователем
    :return: пункт меню
    """
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
            print("Имя пользователя: "+user[1]+", пароль: "+user[2])
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


def choose_test(database, user_name, counter=1):
    """
    Выбор темы тестирования
    :param database: база данных с тестами
    :param user_name: имя авторизованного пользователя
    :param counter: счетчик количества тем для тестирования
    :return: пункт меню
    """
    topics = database.read_data_from_tests('topic')
    message = f"\n{user_name}, выберите тему для тестирования:\n"
    for topic in topics:
        message += f"{counter}. {topic[0]}\n"
        counter += 1
    message += f"{counter}. Выйти\n--->"
    answer = input_command_menu(counter+1, message)
    return answer