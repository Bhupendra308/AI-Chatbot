import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="PASSWORD",
        database="chatbotdb",
        charset="utf8mb4"
    )
    return connection
