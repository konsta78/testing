from database import DataBase
import functions as f


DATABASE = "tests.sqlite3"


if __name__ == "__main__":
    db = DataBase(DATABASE)
    user_token, user_name = f.authorization(db)
    while user_token:
        print(user_token)
        break
    f.choose_test(db)
    db.database_close()
