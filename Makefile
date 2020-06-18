.PHONY: utest atest build

.venv: requirements.txt dev-requirements.txt
	if [ ! -d .venv ]; then \
		python3 -m venv .venv ; \
	fi
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pip install -r dev-requirements.txt

node-deps:
	yarn install

dev-env: .venv node-deps

keyword-docs:
	.venv/bin/python -m robot.libdoc Playwright docs/Playwright.html

utest:
	pytest

atest:
	PYTHONPATH=. robot --loglevel DEBUG --outputdir atest/output atest/test

lint-python:
	black Playwright/ --exclude Playwright/generated
	flake8 Playwright/

build:
	./generategrpc.sh
	yarn build
	cp package.json Playwright/wrapper
