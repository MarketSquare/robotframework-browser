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
	.venv/bin/python -m robot.libdoc Browser docs/Browser.html

utest:
	pytest utest

atest:
	robot --pythonpath . --loglevel DEBUG --outputdir atest/output atest/test

lint-python:
	mypy .
	black Browser/ --exclude Browser/generated
	flake8

build:
	./generategrpc.sh
	yarn build
	cp package.json Browser/wrapper

release:
	rm -rf dist/
	.venv/bin/python setup.py sdist bdist_wheel
	python3 -m twine upload --repository pypi dist/*
