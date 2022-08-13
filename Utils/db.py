import mysql.connector.pooling
import yaml

from mysql.connector import Error

bot = yaml.load(open("./Configs/bot.yml", "r"), Loader=yaml.FullLoader)

# FORMAT
# {"id:": INT, "user_id": INT, "coins": INT, "messages_sent": INT, "xp": INT, "perchased_roles": INT LIST, "warnings": INT}

database = mysql.connector.pooling.MySQLConnectionPool(
    host=bot['db']['host'],
    user=bot['db']['user'],
    password=bot['db']['password'],
    database=bot['db']['database'],
    pool_name='Database',
    pool_size=25
)


class DB:
    def __init__(self):
        pass
    
    @staticmethod
    def fetch(query):
        """Get a connection and a cursor from the pool"""
        connection = database.get_connection()
        cursor = connection.cursor()

        cursor.execute(query)
        result = cursor.fetchall()

        """Return the connection to the pool"""
        connection.close()
        return result

    @staticmethod
    def insert(query, values):
        """Get a connection and a cursor from the pool"""
        connection = database.get_connection()
        cursor = connection.cursor()

        cursor.execute(query, values)
        connection.commit()

        connection.close()

    @staticmethod
    def update(query):
        connection = database.get_connection()
        cursor = connection.cursor()

        cursor.execute(query)
        connection.commit()

        connection.close()

    @staticmethod
    def updateCache(querys):
        connection = database.get_connection()
        cursor = connection.cursor()

        for query in querys:
            cursor.execute(query)

        connection.commit()
        connection.close()

    @staticmethod
    def setup():
        connection = database.get_connection()
        create_user_table = """
        CREATE TABLE IF NOT EXISTS users(
            guild_id INT,
            user_id INT,
            messages_sent INT,
            coins INT,
            perchased_roles INT,
            PRIMARY KEY (guild_id, user_id)
        )
        """

        create_mod_table = """
        CREATE TABLE IF NOT EXISTS moderation(
            id INT AUTO_INCREMENT,
            type STRING,
            reason STRING,
            issuer_id INT,
            guild_id INT,
            PRIMARY KEY (id)
        )
        """

        execute_query(connection, create_user_table)
        execute_query(connection, create_mod_table)