import psycopg2
from decouple import config


class DatabaseError(psycopg2.Error):
    pass


class DB:
    """
    Database class. Handles all connections to the database on heroku.
    """
    def __init__(self):
        self.__connection = None
        self.__cursor = None

    def connect(self):
        """
        creates a connection to the postgres database.
        :return: connection cursor
        """
        try:
            self.__connection = psycopg2.connect(
                                          dbname=config("DB_NAME"),
                                          port=config("DB_PORT"),
                                          host=config("DB_HOST"),
                                          user=config("DB_USER"),
                                          password=config("DB_PASSWORD")
            )
            self.__connection.autocommit = True
            self.__cursor = self.__connection.cursor()
            return self.__cursor
        except DatabaseError:
            raise DatabaseError("There was a problem connecting to the requested database.")

    def setup_tables(self):
        """
        sets up the Listings and Categories tables in the database.
        :return: Table successfully created message.
        """
        try:
            self.__cursor.execute("CREATE TABLE IF NOT EXISTS Categories(id SERIAL PRIMARY KEY, category VARCHAR UNIQUE)")
            self.__cursor.execute("""CREATE TABLE IF NOT EXISTS Listings
                                   (id SERIAL PRIMARY KEY, title VARCHAR, 
                                   price VARCHAR, item_url VARCHAR, image_url VARCHAR, 
                                   category_id INTEGER REFERENCES Categories(id) ) 
                                    """)
            print("Listings and Categories tables now available in database.")
        except (DatabaseError, Exception):
            raise DatabaseError("Could not create tables in the specified database")

    def delete_tables(self):
        """
        deletes Listing and Categories tables from the database
        :return: Tables successfully deleted message
        """
        try:
            self.__cursor.execute("DROP TABLE IF EXISTS Listings CASCADE ")
            self.__cursor.execute("DROP TABLE IF EXISTS Categories")
            print("Listings and Categories tables no longer in database.")
        except (Exception, DatabaseError):
            raise DatabaseError("Could not drop tables in the specified database")
