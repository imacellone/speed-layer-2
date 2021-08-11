#!/bin/bash

echo -e "\n\n#########################################"

echo -e "Initial Speed-Layer configuration\n\n"

read -e -p "Enter the directory where your ssh keys are (DO NOT USE ~ ):  " sshDirectory

echo "Enter your full name (eg.: John Doe): "
read name

echo "Enter your GitHub e-mail address (eg.: john.doe@mail.com): "
read email

sed -e "s|\(^.*- \).*\(:\/home\/nifi\/\.ssh\)|\1$sshDirectory\2|" -I '' docker-compose.yml
sed -e "s/^\(.*\)\(GIT_CONFIG_USER_NAME\).*$/\1\2: '$name'/" -I '' docker-compose.yml
sed -e "s/^\(.*\)\(GIT_CONFIG_USER_EMAIL\).*$/\1\2: $email/" -I '' docker-compose.yml

echo -e "\n\nDone!\n\n"

echo "#########################################"
