PYTHON	= python3
MAIN	= a_maze_ing.py
CONFIG	= config.txt

MYPY_FLAGS	= --warn-return-any --warn-unused-ignores \
			  --ignore-missing-imports --disallow-untyped-defs \
			  --check-untyped-defs

.PHONY: all install run debug lint lint-strict clean

all: run

install:
	pip install mypy flake8

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

lint:
	flake8 .
	mypy . $(MYPY_FLAGS)

lint-strict:
	flake8 .
	mypy . --strict

clean:
	rm -rf __pycache__ .mypy_cache
