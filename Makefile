.PHONY: utest atest

utest:
	poetry run pytest
atest:
	poetry run robot --outputdir atest/output atest/test

lint-python:
	poetry run black Playwright/ --exclude Playwright/generated
	poetry run flake8 Playwright/

build:
	./generategrpc.sh
	poetry build
	yarn build
