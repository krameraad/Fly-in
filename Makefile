install:
	pip install -r requirements.txt

run:
	python3 fly-in.py

debug:
	python3 -m pdb fly-in.py default_config.txt

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache

lint:
	flake8 --exclude=.venv
	python3 -m mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--explicit-package-bases \
		--exclude '^(venv|\.venv|env)/'

lint-strict:
	flake8 --exclude=.venv
	python3 -m mypy . \
		--strict \
		--explicit-package-bases \
		--exclude '^(venv|\.venv|env)/'