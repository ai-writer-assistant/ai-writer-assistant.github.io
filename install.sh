
# Install npm
curl -fsSL https://deb.nodesource.com/setup_21.x | sudo -E bash - &&\
sudo apt install -y nodejs

curl https://ollama.ai/install.sh | sh

npm i

ollama create blog -f ./Modelfile

./start.sh