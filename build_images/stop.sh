#!/bin/bash
docker stop fastapi-networktestkit
docker stop nginx-test
docker system prune -f