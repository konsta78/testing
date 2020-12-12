from db_users import UsersDataBase
from db_tests import TestsDataBase
import functions as f


DATABASE_USERS = "users.sqlite3"
DATABASE_TESTS = "tests.sqlite3"


if __name__ == "__main__":
    db_users = UsersDataBase(DATABASE_USERS)
    db_tests = TestsDataBase(DATABASE_TESTS)
    if db_users.check_users_db() is None:
        db_users.create_users()
    if db_tests.check_tests_db() is None:
        db_tests.create_tests()

    # user_token, user_name = f.authorization(db_users)
    user_token, user_name = 1, 'test_user'

    if user_token:
        topic = f.choose_test(db_tests, user_name)
        if topic:
            results = f.testing(db_tests, topic)
            print(results)
    db_users.database_close()
    db_tests.database_close()
