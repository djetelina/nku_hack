# -*- coding utf-8 -*-

import os

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

from unemployed import importer


def main():
    """
    SEM napis seznam modulu k importu
    :return:
    """
    importer.run()


if __name__ == "__main__":
    main()
