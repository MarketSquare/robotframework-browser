#!/bin/sh
poetry run python -m grpc_tools.protoc -Iprotos --python_out=Playwright/generated --grpc_python_out=Playwright/generated protos/playwright.proto
