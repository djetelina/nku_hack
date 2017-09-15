PYTHON_VERSION=$(shell python -V)

default:
	@echo "make run?"

localdev:
ifneq ($(findstring Python 3.6, ${PYTHON_VERSION}), Python 3.6)
	@echo "Python 3.6+ required!"
	@exit 1
else
	pip install -r requirements.txt
	cd frontend && npm i
endif

run:
	cd src && python hackaton_nku.py
	cd frontend && make run dev

