ifeq ($(OS),Windows_NT)
	rm_cmd = del
	backup_files = .\Browser\generated\playwright_pb2_grpc.py.bak
	PROTO_DEST = .\Browser\wrapper\generated
	PROTOC_GEN_PLUGIN = .\node_modules\.bin\grpc_tools_node_protoc_plugin.cmd
	PROTOC_TS_PLUGIN = .\node_modules\.bin\protoc-gen-ts.cmd
else
	rm_cmd = rm
	backup_files = Browser/generated/playwright_pb2_grpc.py.bak
	PROTO_DEST = ./Browser/wrapper/generated
	PROTOC_GEN_PLUGIN = ./node_modules/.bin/grpc_tools_node_protoc_plugin
	PROTOC_TS_PLUGIN = ./node_modules/.bin/protoc-gen-ts
endif

.PHONY: utest atest build protobuf

.venv: requirements.txt dev-requirements.txt
	if [ ! -d .venv ]; then \
		python3 -m venv .venv ; \
	fi
	.venv/bin/pip install -r requirements.txt;
	.venv/bin/pip install -r dev-requirements.txt;

node-deps:
	yarn install

dev-env: .venv node-deps

keyword-docs:
	python -m robot.libdoc Browser docs/Browser.html

utest-watch:
	ptw --ignore ./node_modules --ignore ./.venv

utest:
	pytest utest

clean:
	rm -rf atest/output
atest: clean
	ROBOT_SYSLOG_FILE=atest/output/syslog.txt python -m pabot.pabot --pabotlib --pythonpath . --exclude Not-Implemented --loglevel DEBUG --outputdir atest/output atest/test

atest-global-pythonpath: clean
	ROBOT_SYSLOG_FILE=atest/output/syslog.txt python -m pabot.pabot --pabotlib --exclude Not-Implemented --loglevel DEBUG --outputdir atest/output atest/test

test-failed: build
	PYTHONPATH=. python -m pabot.pabot --pabotlib --exclude Not-Implemented --loglevel DEBUG --rerunfailed atest/output/output.xml --outputdir atest/output atest/test

docker:
	docker build --tag rfbrowser .
docker-test:
	rm -rf atest/output
	docker run -it --rm --ipc=host --security-opt seccomp=chrome.json -v $(shell pwd)/atest/:/atest rfbrowser robot --loglevel debug --exclude Not-Implemented -d /atest/output /atest/test

lint-python:
	mypy .
	black Browser/
	flake8

lint-node:
	yarn run lint

lint-robot:
	python -m robot.tidy --recursive atest/test

lint: lint-node lint-python lint-robot

protobuf:
	mkdir -p Browser/generated/
	mkdir -p Browser/wrapper/generated/
	python -m grpc_tools.protoc -Iprotos --python_out=Browser/generated --grpc_python_out=Browser/generated protos/*.proto
	touch Browser/generated/__init__.py
	sed -i.bak -e 's/import playwright_pb2 as playwright__pb2/from Browser.generated import playwright_pb2 as playwright__pb2/g' Browser/generated/playwright_pb2_grpc.py
	$(rm_cmd) $(backup_files)

	yarn run grpc_tools_node_protoc \
		--js_out=import_style=commonjs,binary:$(PROTO_DEST) \
		--grpc_out=$(PROTO_DEST) \
		--plugin=protoc-gen-grpc=$(PROTOC_GEN_PLUGIN) \
		-I ./protos \
		protos/*.proto

	yarn run grpc_tools_node_protoc \
		--plugin=protoc-gen-ts=$(PROTOC_TS_PLUGIN) \
		--ts_out=$(PROTO_DEST) \
		-I ./protos \
		protos/*.proto

build: protobuf
	yarn build

package: build keyword-docs
	rm -rf dist/
	cp package.json Browser/wrapper
	python setup.py sdist bdist_wheel

release: package
	python3 -m twine upload --repository pypi dist/*
