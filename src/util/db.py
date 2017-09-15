import sqlite3
import config
from typing import Union


class DB:

    def __init__(self, file_path, return_cursor=False):
        self.file_path = file_path
        self.return_cursor = return_cursor

    def __enter__(self) -> Union[sqlite3.Cursor, sqlite3.Connection]:
        self.connection = sqlite3.connect(self.file_path)
        self.connection.row_factory = sqlite3.Row  # chceme vraceti dicty
        return self.connection.cursor() if self.return_cursor else self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()


def common_db(cursor=False):
    """
    Vrati otevrenou spolecnou databazi.
    :param cursor: zdalipak vraceti kurzor, nebo konexi
    :return: ctx manager
    """
    return DB(config.DB_PATH, return_cursor=cursor)


def ruian_db(cursor=False) -> DB:
    """
    Vrati otevrenou RUIAN db
    :param cursor: zdalipak vraceti kurzor, nebo konexi
    :return: ctx manager
    """
    return DB(config.RUIAN_PATH, return_cursor=cursor)

