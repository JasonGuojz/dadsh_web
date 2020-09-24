# dadsh_web
a image retrieval web application based on the deep CNN mode(we called it dadsh: double-bit asymmetric deep supervised hashing 

## how to start up
$  sudo fuser -k 80/tcp  
$  docker build github.com/JasonGuojz/dadsh_web -t dadsh:{tag}  
$  sudo docker run -d -p 80:80 --name dadsh_test dadsh:{tag}

