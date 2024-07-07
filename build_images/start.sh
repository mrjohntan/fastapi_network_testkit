#!/bin/bash
docker run -p 8081:80 --name nginx-test -d nginx-test:latest
docker run -p 8082:80 --name fastapi-networktestkit -d fastapi-networktestkit:latest