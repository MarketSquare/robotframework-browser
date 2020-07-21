ifeq ($(OS),Windows_NT)
	rm_cmd = del
	backup_files = .\Browser\generated\playwright_pb2_grpc.py.bak
	PROTO_DEST = .\node\playwright-wrapper\generated
	PROTOC_GEN_PLUGIN = .\node_modules\.bin\grpc_tools_node_protoc_plugin.cmd
	PROTOC_TS_PLUGIN = .\node_modules\.bin\protoc-gen-ts.cmd
else
	rm_cmd = rm
	backup_files = Browser/generated/playwright_pb2_grpc.py.bak
	PROTO_DEST = ./node/playwright-wrapper/generated
	PROTOC_GEN_PLUGIN = ./node_modules/.bin/grpc_tools_node_protoc_plugin
	PROTOC_TS_PLUGIN = ./node_modules/.bin/protoc-gen-ts
endif

.PHONY: utest clean-atest protobuf

.venv: Browser/requirements.txt Browser/dev-requirements.txt
	if [ ! -d .venv ]; then \
		python3 -m venv .venv ; \
	fi
	.venv/bin/pip install -r Browser/requirements.txt;
	.venv/bin/pip install -r Browser/dev-requirements.txt;

node_modules/.installed: package.json yarn.lock
	yarn install
	touch node_modules/.installed

dev-env: .venv node_modules

keyword-docs:
	python -m robot.libdoc Browser docs/Browser.html

utest-watch:
	ptw --ignore ./node_modules --ignore ./.venv

utest:
	pytest utest

clean-atest:
	rm -rf atest/output

atest: clean-atest build atest/test
	ROBOT_SYSLOG_FILE=atest/output/syslog.txt python -m pabot.pabot --pabotlib --verbose --pythonpath . --exclude Not-Implemented --loglevel DEBUG --outputdir atest/output atest/test

atest-global-pythonpath: clean-atest
	ROBOT_SYSLOG_FILE=atest/output/syslog.txt python -m pabot.pabot --pabotlib --verbose --exclude Not-Implemented --loglevel DEBUG --outputdir atest/output atest/test

test-failed: build
	python -m pabot.pabot --pabotlib --verbose --exclude Not-Implemented --loglevel DEBUG --rerunfailed atest/output/output.xml --outputdir atest/output atest/test

docker:
	docker build --tag rfbrowser --file atest/docker/Dockerfile .
docker-test:
	rm -rf atest/output
	docker run -it --rm --ipc=host --security-opt seccomp=atest/docker/chrome.json -v $(shell pwd)/atest/:/atest rfbrowser robot --loglevel debug --exclude Not-Implemented -d /atest/output /atest/test

lint-python:
	mypy --config-file Browser/mypy.ini Browser/ utest/
	black --config Browser/pyproject.toml Browser/
	black --config Browser/pyproject.toml utest/
	flake8 --config Browser/.flake8 Browser/ utest/

node/.linted: build node/playwright-wrapper/*.ts node/dynamic-test-app/src/*
	yarn run lint
	touch node/.linted

lint-robot:
	python -m robot.tidy --recursive atest/test

lint: node/.linted lint-python lint-robot

Browser/generated/.generated: protobuf/playwright.proto
	mkdir -p Browser/generated/
	touch Browser/generated/__init__.py
	python -m grpc_tools.protoc -I protobuf --python_out=Browser/generated --grpc_python_out=Browser/generated protobuf/*.proto
	sed -i.bak -e 's/import playwright_pb2 as playwright__pb2/from Browser.generated import playwright_pb2 as playwright__pb2/g' Browser/generated/playwright_pb2_grpc.py
	$(rm_cmd) $(backup_files)
	touch Browser/generated/.generated

node/playwright-wrapper/generated/.generated: protobuf/playwright.proto
	mkdir -p node/playwright-wrapper/generated
	yarn run grpc_tools_node_protoc \
		--js_out=import_style=commonjs,binary:$(PROTO_DEST) \
		--grpc_out=$(PROTO_DEST) \
		--plugin=protoc-gen-grpc=$(PROTOC_GEN_PLUGIN) \
		-I ./protobuf \
		protobuf/*.proto
	yarn run grpc_tools_node_protoc \
		--plugin=protoc-gen-ts=$(PROTOC_TS_PLUGIN) \
		--ts_out=$(PROTO_DEST) \
		-I ./protobuf \
		protobuf/*.proto
	touch node/playwright-wrapper/generated/.generated

protobuf: Browser/generated/.generated node/playwright-wrapper/generated/.generated

Browser/wrapper/index.js: node/playwright-wrapper
	yarn build
node/dynamic-test-app/dist: node/dynamic-test-app/src node/dynamic-test-app/static
	yarn build
webpack-typescript: node/dynamic-test-app/dist Browser/wrapper/index.js

build: protobuf node_modules/.installed webpack-typescript

watch-webpack: build
	yarn run webpack --watch

package: build keyword-docs
	rm -rf dist/
	cp package.json Browser/wrapper
	python setup.py sdist bdist_wheel

version:
	sed -i.bak -e 's/VERSION = .*/VERSION = "$(VERSION)"/' Browser/version.py
	sed -i.bak -e 's/"version": ".*"/"version": "$(VERSION)"/' package.json
	sed -i.bak -e 's/VERSION: .*/VERSION: $(VERSION)/' .github/workflows/python-package.yml
	${rm_cmd} Browser/version.py.bak package.json.bak .github/workflows/python-package.yml.bak

release: package
	python3 -m twine upload --repository pypi dist/*
