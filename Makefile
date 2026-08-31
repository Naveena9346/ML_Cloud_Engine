# Root Makefile for MLCloudEngine Platform

.PHONY: install run test docker-build

install:
	pip install -r backend/requirements.txt
	cd frontend && npm install

run:
	python run_server.py

test:
	python -m pytest tests/ -v

docker-build:
	docker build -t mlcloudengine:latest -f Dockerfile .
