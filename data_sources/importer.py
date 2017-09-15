# -*- coding utf-8 -*-

from csu_obyvatelstvo import importer as csu_obyvatelstvo_importer
from unemployed import importer as unemployed_importer


def main():
    """
    SEM napis seznam modulu k importu
    :return:
    """
    csu_obyvatelstvo_importer.main()
    unemployed_importer.run()


if __name__ == "__main__":
    main()
