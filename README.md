# fastapi_network_testkit
Implementing a network test kit container with fastapi

# use case
Building a container to facilitate network tests during the initial phase of deploying cloud infrastructure.  
In an enterprise, the production network will often tightly controlled and use of terminals might be discouraged.  
This containerised api service could be deployed to facilitate network testing.

# guide

1. Build containers
```
cd build_images
./build.sh
```

2. Run the containers

```
docker run -p 8081:80 --name nginx-test -d nginx-test:latest
docker run -p 8082:80 --name fastapi-networktestkit -d fastapi-networktestkit:latest
```
3. Get a list the list of running containers on the host

```
docker ps -a
```
4. Get ip address of a selected container.  
Replace ${CONTAINER_ID} with value of "CONTAINER ID".  
This will reveal the IP address of the container. e.g. 172.17.0.2
```
docker inspect -f '{{ .NetworkSettings.IPAddress }}' ${CONTAINER_ID}
```
5. Access swagger ui on fastapi container.  
> http://localhost:8082/docs  

6. Testing urlrequest endpoint
```
curl -X 'POST' \
  'http://localhost:8082/urlrequest' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "url": "http://172.17.0.2"
}'
```
