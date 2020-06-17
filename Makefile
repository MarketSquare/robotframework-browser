.PHONY: utest atest build

.venv: requirements.txt dev-requirements.txt
	if [ ! -d .venv ]; then \
		python3 -m venv .venv ; \
	fi
	pip install -r requirements.txt
	pip install -r dev-requirements.txt

node-deps:
	yarn install

dev-env: .venv node-deps

utest:
	pytest

atest:
	PYTHONPATH=. robot --outputdir atest/output atest/test

lint-python:
	black Playwright/ --exclude Playwright/generated
	flake8 Playwright/

build:
	./generategrpc.sh
	yarn build
	cp package.json Playwright/wrapper
