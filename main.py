from db_users import UsersDataBase
from db_tests import TestsDataBase
import functions as f
import config as c


if __name__ == "__main__":
    db_users = UsersDataBase(c.DATABASE_USERS)
    db_tests = TestsDataBase(c.DATABASE_TESTS)
    if db_users.check_users_db() is None:
        db_users.create_users()
    if db_tests.check_tests_db() is None:
        db_tests.create_tests()

    user_token, user_name = f.authorization(db_users)

    if user_token:
        topic = f.choose_test(db_tests, user_name)
        if topic:
            results = f.testing(db_tests, topic)
            user_result = f.check_results(db_tests, topic, results)
            f.show_result(user_name, topic, user_result)

    db_users.database_close()
    db_tests.database_close()
