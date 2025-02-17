
init:
	python3 -m venv env

libhash:
	pip install pip-tools --no-cache && \
	rm requirements/requirements-dev.txt && \
	pip-compile --generate-hashes requirements/requirements-dev.in > requirements/requirements-dev.txt
	pip-compile --generate-hashes requirements/requirements-prod.in
	cp requirements/requirements-prod.txt requirements.txt

uninstall:
	pip freeze > uninstall
	pip uninstall -r uni -y
	rm uninstall


install:
	pip3 install --upgrade pip
	pip3 install wheel
	pip3 install -r requirements.txt --no-cache --default-timeout=200
	pip3 install -r requirements-tests.txt --no-cache --default-timeout=200

pretty:
	isort app/**/*.py && \
	flake8 app/*

format:
	black app  --line-length=140 --exclude=app/view/templates

secure:
	bandit -r app/* -x tests

safe:
	safety check -r requirements.txt

clean:
	find app -name '*.pyc' -exec rm -rf {} \;
	rm -rf .tox
	rm -rf .pytest_cache
	rm -rf *.egg-info
	rm -rf .coverage

up:
	docker-compose up --build

r:
	uvicorn backend.src.main:app --reload

load:
	locust -f tests/load.py

test:
	pytest -vv

.PHONY: init
