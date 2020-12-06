from database import DataBase
import functions as f


DATABASE = "tests.sqlite3"


if __name__ == "__main__":
    db = DataBase(DATABASE)
    user_token = f.authorization(db)
    if user_token:
        print(user_token)
    db.database_close()
