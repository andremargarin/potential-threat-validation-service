import mysql.connector
import settings


def get_mysql_connection():
    return mysql.connector.connect(
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        host=settings.MYSQL_HOST,
        database=settings.MYSQL_DATABASE
    )
