# -*- coding utf-8 -*-

from population import importer as population_importer
from unemployed import importer as unemployed_importer
from elections import importer as election_importer


def main():
    """
    SEM napis seznam modulu k importu
    :return:
    """
    population_importer.main()
    unemployed_importer.run()
    election_importer.main()


if __name__ == "__main__":
    main()
