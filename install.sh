# Update package manager
sudo apt update -y

# Install npm
sudo apt install npm -y

curl https://ollama.ai/install.sh | sh

npm i

ollama create blog -f ./Modelfile