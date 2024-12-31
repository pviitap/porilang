PYTHON := python3
SRC := porilang.py
.DEFAULT_GOAL := test

lint:
	$(PYTHON) -m pylint $(SRC); $(PYTHON) -m mypy $(SRC)

test: lint
	$(PYTHON) -m pytest

run:
	$(PYTHON) $(SRC)
