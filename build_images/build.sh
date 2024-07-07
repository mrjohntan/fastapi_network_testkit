#!/bin/bash
docker build -t nginx-test nginx/.
docker build -t fastapi-networktestkit networktestkit/.