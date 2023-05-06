#!/bin/bash

if [ "$USER" != "root" ]; then
    echo "ERROR: This script must be run as root."
    exit 1
fi

salt_master_ip=''

while getopts 'i:' flag; do
    case "${flag}" in
        i) salt_master_ip="${OPTARG}" ;;
    esac
done

if [ "$salt_master_ip" = "" ]; then
    echo "ERROR: Missing the -i flag for the salt master IP"
    exit 1
fi

echo "> Checking if the salt-minion is already installed..."
which salt-minion
return_code=$?
if [ $return_code -ne 0 ]; then
    sudo mkdir -p /etc/apt/keyrings
    sudo wget -O /etc/apt/keyrings/salt-archive-keyring-2023.gpg https://repo.saltproject.io/salt/py3/ubuntu/20.04/amd64/SALT-PROJECT-GPG-PUBKEY-2023.gpg
    echo "deb [signed-by=/etc/apt/keyrings/salt-archive-keyring-2023.gpg arch=amd64] https://repo.saltproject.io/salt/py3/ubuntu/20.04/amd64/minor/3006.1/ focal main" | sudo tee /etc/apt/sources.list.d/salt.list

    sudo apt-get update
    sudo apt-get install salt-minion -y
else
    echo "> The salt-minion is already installed."
fi

echo "> Setting the salt-minion to start on start-up..."
sudo systemctl enable salt-minion
return_code=$?
if [ $return_code -eq 0 ]; then
    echo "> Successfully set the salt-minion to start on start-up."
else
    echo "> Failed to set the salt-minion to start on start-up... Continuing because it's not crucial."
fi

echo "> Starting the salt-minion..."
sudo systemctl start salt-minion
return_code=$?
if [ $return_code -eq 0 ]; then
    echo "> Successfully started the salt-minion."
else
    echo "> Failed to start the salt-minion!"
    exit 1
fi

echo "> Adding the salt master to /etc/hosts..."
grep -wq "salt" /etc/hosts # check if the salt master has already been added to /etc/hosts
return_code=$?
if [ $return_code -eq 0 ]; then
    sed -i "/salt/c\\$salt_master_ip salt" /etc/hosts # replace the line containing salt in case our IP changed
else
    echo -e "\n$salt_master_ip salt" >> /etc/hosts # add the salt master to /etc/hosts
fi
echo "> Successfully added the salt master to /etc/hosts."
