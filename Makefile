PYTHON	= python3
MAIN	= a_maze_ing.py
CONFIG	= config.txt
OUR_MODULE = mazegen-1.0.0-py3-none-any.whl

MYPY_FLAGS	= --warn-return-any --warn-unused-ignores \
			  --ignore-missing-imports --disallow-untyped-defs \
			  --check-untyped-defs

.PHONY: all install run debug lint lint-strict clean

all: run

install:
	pip install mypy flake8 OUR_MODULE --force-reinstall

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

lint:
	flake8 .--exclude .venv 
	mypy . $(MYPY_FLAGS) --exclude .venv 

lint-strict:
	flake8 . --exclude=.venv 
	mypy . --strict --exclude .venv 

clean:
	rm -rf __pycache__ .mypy_cache
