#!/bin/bash

echo "Initial Speed-Layer configuration"

echo "Enter your full name (eg.: John Doe): "
read name

echo "Enter your GitHub e-mail address (eg.: john.doe@mail.com): "
read email

sed -e "s/^\(.*\)\(GIT_CONFIG_USER_NAME\).*$/\1\2: '$name'/" -I '' docker-compose.yml
sed -e "s/^\(.*\)\(GIT_CONFIG_USER_EMAIL\).*$/\1\2: $email/" -I '' docker-compose.yml

echo "Done!"
