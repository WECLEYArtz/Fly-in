.PHONY: all run debug install clean lint

MAP = maps/easy/01_linear_path.txt

install:
	$(CAHCE) $(VENV) uv sync

run:
	$(CAHCE) $(VENV) uv run python3 main.py $(MAP)

deug:
	$(CAHCE) $(VENV) uv run python3 -m pdb main.py $(MAP)

clean:
	rm -rf .mypy_cache __pycache__

lint: 
	uv run flake8 .
	uvv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
