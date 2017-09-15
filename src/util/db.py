import sqlite3
import config


class DB:

    def __init__(self, file_path):
        self.file_path = file_path

    def __enter__(self):
        self.connection = sqlite3.connect(self.file_path)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()


def common_db():
    """
    Vrati otevrenou spolecnou databazi.
    :return: ctx manager
    """
    return DB(config.DB_PATH)


def ruian_db():
    """
    Vrati otevrenou RUIAN db
    :return: ctx manager
    """
    return DB(config.RUIAN_PATH)

