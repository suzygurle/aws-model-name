sudo apt-get update
sudo apt-get install -y python3 python3-pip wget nano git awscli



curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

sudo pip3 install tensorflow==2.8 --no-cache-dir

sudo pip install wget
sudo pip install boto3

sudo git clone https://github.com/suzygurle/aws-model-name.git

cd aws-model-name

sudo docker build .

#sudo su 

#aws configure
#aws ecr get-login-password --region eu-west-3 | docker login --username AWS --password-stdin 124716560638.dkr.ecr.eu-west-3.amazonaws.com/aws-ecr-lab-l9    
#sudo docker push 124716560638.dkr.ecr.eu-west-3.amazonaws.com/aws-ecr-lab-l9 

