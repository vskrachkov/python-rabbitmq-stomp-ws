docker build -t rabbit-stomp-websockets .
docker run -d --hostname my-rabbit --name rabbit-stomp -p 15672:15672 -p 15674:15674 -p 61613:61613 -p 5672:5672 rabbit-stomp-websockets