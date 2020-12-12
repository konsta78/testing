"""
Функции для работы с БД и сервисом тестирования
"""
import messages as m
import random


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
        else:
            if answer not in range(1, count):
                print("Такого пункта меню не существует.")
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
    :return: topic: тема тестирования (либо выход из программы)
    """
    topics = database.get_topics('topic')
    message = f"\n{user_name}, выберите тему для тестирования:\n"

    for topic in topics:
        message += f"{counter}. {topic[0]}\n"
        counter += 1
    message += f"{counter}. Выйти\n--->"

    topic = input_command_menu(counter+1, message)
    if topic == counter:
        topic = None
    else:
        topic = topics[topic-1][0]
    return topic


def testing(database, topic, q_counter=1):
    """
    Проведение тестирования по выбранной теме
    :param database: база данных с тестами
    :param topic: выбранная тема для тестирования
    :param q_counter: счетчик кол-ва вопросов для тестирования
    :return: results: словарь с ответами пользователя {"номер вопроса": "ответ пользователя"}
    """
    def shake_answers():
        """
        Функция для случайного отображения вариантов ответов на вопрос теста
        :return: список вариантов ответов
        """
        answers_list = database.get_answers_for_question(question[0])
        answers_list = [answers_list[i][0] for i in range(0, len(answers_list))]
        random.shuffle(answers_list)
        return answers_list

    results = {}
    questions = database.get_questions(topic)

    for question in questions:
        message = f"\nВопрос №{q_counter}\n"
        message += f"{question[0]}\n"
        q_counter += 1
        answers_list = shake_answers()

        for count, answer in enumerate(answers_list):
            message += f"{count+1}. {answer}\n"
        message += "-->"

        answer = input_command_menu(len(answers_list)+1, message)
        results[q_counter-1] = answers_list[answer-1]
    return results


def check_results(database, topic, results):
    """
    Проверка ответов пользователя
    :param database: база данных с тестами
    :param topic: выбранная тема для тестирования
    :param results: словарь с ответами пользователя {"номер вопроса": "ответ пользователя"}
    :return: кол-во правильных ответов
    """
    user_result = 0
    right_answers = database.get_right_answers(topic)
    right_answers = [right_answers[i][0] for i in range(0, len(right_answers))]
    for index, answer in enumerate(right_answers):
        if answer == results.get(index+1):
            user_result += 1
    return user_result


def show_result(user_name, topic, user_result):
    """
    Отображения результатов тестирования
    :param user_name: имя пользователя
    :param topic: выбранная тема для тестирования
    :param user_result: словарь с ответами пользователя {"номер вопроса": "ответ пользователя"}
    """
    print(f"Уважаемый {user_name}!\n"
          f"Тест по теме '{topic}' завершен и ваш результат: {user_result} правильных ответов.")