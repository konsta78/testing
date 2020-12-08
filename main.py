from db_users import UsersDataBase
from db_tests import TestsDataBase
import functions as f


DATABASE_USERS = "users.sqlite3"
DATABASE_TESTS = "tests.sqlite3"


if __name__ == "__main__":
    db_users = UsersDataBase(DATABASE_USERS)
    db_tests = TestsDataBase(DATABASE_TESTS)

    user_token, user_name = f.authorization(db_users)
    if user_token:
        topic = f.choose_test(db_tests, user_name)

    db_users.database_close()
    db_tests.database_close()
