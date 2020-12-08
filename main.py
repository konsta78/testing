from db_users import UsersDataBase
import functions as f


DATABASE_USERS = "users.sqlite3"


if __name__ == "__main__":
    db = UsersDataBase(DATABASE_USERS)
    user_token, user_name = f.authorization(db)
    # while user_token:
    #     print(user_token)
    #     break

    db.database_close()
