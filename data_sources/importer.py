# -*- coding utf-8 -*-

from population import importer as population_importer
from unemployed import importer as unemployed_importer
from elections import importer as election_importer
from to_survive import importer as to_survive_importer


def main():
    """
    SEM napis seznam modulu k importu
    :return:
    """
    population_importer.main()
    unemployed_importer.run()
    election_importer.main()
    to_survive_importer.run()


if __name__ == "__main__":
    main()
