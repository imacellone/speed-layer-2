#!/bin/bash

echo -e "\n\n#########################################"

echo -e "Initial Speed-Layer configuration\n\n"

read -e -p "Enter the directory where your ssh keys are (DO NOT USE ~ ):  " sshDirectory

echo "Enter your full name (eg.: John Doe): "
read name

echo "Enter your GitHub e-mail address (eg.: john.doe@mail.com): "
read email

sshExpr="s|\(^.*- \).*\(:\/home\/nifi\/\.ssh\)|\1$sshDirectory\2|"
nameExpr="s/^\(.*\)\(GIT_CONFIG_USER_NAME\).*$/\1\2: '$name'/"
emailExpr="s/^\(.*\)\(GIT_CONFIG_USER_EMAIL\).*$/\1\2: $email/"

if [[ "$OSTYPE" == "darwin"* ]]; then # sed on mac behaves a bit different
    sed -e "$sshExpr" -I '' docker-compose.yml
    sed -e "$nameExpr" -I '' docker-compose.yml
    sed -e "$emailExpr" -I '' docker-compose.yml 
else
    sed -i -e "$sshExpr" docker-compose.yml
    sed -i -e "$nameExpr" docker-compose.yml
    sed -i -e "$emailExpr" docker-compose.yml
fi

echo -e "\n\nDone!\n\n"

echo "#########################################"
