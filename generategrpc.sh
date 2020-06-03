#!/bin/sh
# Python code generation
poetry run python -m grpc_tools.protoc -Iprotos --python_out=Playwright/generated --grpc_python_out=Playwright/generated protos/*.proto

PROTO_DEST=./src/generated

# JavaScript code generation
yarn run grpc_tools_node_protoc \
    --js_out=import_style=commonjs,binary:${PROTO_DEST} \
    --grpc_out=${PROTO_DEST} \
    --plugin=protoc-gen-grpc=./node_modules/.bin/grpc_tools_node_protoc_plugin \
    -I ./protos \
    protos/*.proto

# TypeScript code generation
yarn run grpc_tools_node_protoc \
    --plugin=protoc-gen-ts=./node_modules/.bin/protoc-gen-ts \
    --ts_out=${PROTO_DEST} \
    -I ./protos \
    protos/*.proto