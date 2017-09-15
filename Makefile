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
	cd src && python nku_hack.py
	cd frontend && npm i

import:
	PYTHONPATH=src:. python data_sources/importer.py
