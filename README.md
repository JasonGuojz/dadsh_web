# dadsh_web
an image retrieval web application based on the deep CNN model(we called it dadsh: double-bit asymmetric deep supervised hashing 

## how to start up
$  docker build github.com/JasonGuojz/dadsh_web -t dadsh:{tag}  
$  sudo fuser -k 80/tcp  
$  sudo docker run -d -p 80:80 --name dadsh_test dadsh:{tag}

OR  
$  git lfs clone https://github.com/JasonGuojz/dadsh_web.git  
$  cd dadsh_web  
$  docker build -t dadsh:{tag} .  
$  sudo fuser -k 80/tcp  
$  sudo docker run -d -p 80:80 --name test-dadsh-1 dadsh:{tag}

