PYTHON_VERSION=$(shell python -V)

default:
	@echo "Na vyber:"
	@echo "run - spusti"
	@echo "localdev - zinicializuje"
	@echo ""

localdev:
ifneq ($(findstring Python 3.6, ${PYTHON_VERSION}), Python 3.6)
	@echo "Python 3.6+ required!"
	@exit 1
else
	pip install -r requirements.txt
endif

run:
	cd frontend && npm run dev &
	cd src && python nku_hack.py

import:
	rm -f db/db.sqlite
	PYTHONPATH=src:. python data_sources/importer.py

db-dump:
	mkdir -p dump
	sqlite3 db/db.sqlite .dump | gzip > dump/dump.sql.gz

db-recreate:
	rm -f db/db.sqlite
	gunzip -c dump/* | sqlite3 db/db.sqlite
	echo "vacuum;" | sqlite3 db/db.sqlite

