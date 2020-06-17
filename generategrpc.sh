#!/bin/sh
# Python code generation
python -m grpc_tools.protoc -Iprotos --python_out=Playwright/generated --grpc_python_out=Playwright/generated protos/*.proto
# hack to fix import, empty -i '' is needed for macos sed compatibility
sed -i.bak -e 's/import playwright_pb2 as playwright__pb2/from Playwright.generated import playwright_pb2 as playwright__pb2/g' Playwright/generated/playwright_pb2_grpc.py
rm Playwright/generated/playwright_pb2_grpc.py.bak

PROTO_DEST=./Playwright/wrapper/generated

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
