#!/bin/bash

printf "Get API key for FAIRsharing.org\n"
printf "(see https://fairsharing.org/API_doc)\n\n"

read -p "FAIRsharing.org login: " LOGIN
read -s -p "FAIRsharing.org password: " PASSWORD
printf "\n"

response=$(curl --location --request POST 'https://api.fairsharing.org/users/sign_in' \
    --header 'Accept: application/json' \
    --header 'Content-Type: application/json' \
    --data-raw '{"user": {"login":"'"$LOGIN"'","password":"'"$PASSWORD"'"} }')

echo "${response}" | jq .
echo
echo

printf "Get API key for DSW FAIRsharing.org proxy\n"
printf "(see https://guide.ds-wizard.org/for-users/for-data-stewards/knowledge-model-editor/add-integration#fairsharing-proxy)\n\n"

apikey=$(echo -n "${LOGIN}:${PASSWORD}" | base64 --wrap 0 -)
printf "integration.yml lines:\n\n"
cat <<EOT
fairsharing:
  apiUrl: https://fairsharing4dsw.ds-wizard.org/legacy
  apiKey: ${apikey}
EOT
echo

av=$(echo -n "${apikey}" | ansible-vault encrypt_string --stdin-name dsw.integration.fairsharing.apiKey | tail -n+2)
printf "integration.yml lines with Ansible Vault encryption:\n\n"
cat <<EOT
fairsharing:
  apiUrl: https://fairsharing4dsw.ds-wizard.org/legacy
  apiKey: {{ dsw.integration.fairsharing.apiKey }}
EOT
cat <<EOT
dsw:
  integration:
    fairsharing:
      apiKey: !vault |
$av
EOT
