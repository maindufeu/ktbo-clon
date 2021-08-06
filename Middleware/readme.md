# Integración con Gitlab

para clonar el repositorio es necesario crear llaves rsa con: 

ssh-keygen -t rsa -b 2048 -C "EC2 keys"

copiarlas con:

cat ~/.ssh/id_rsa.pub

y después pegarlas en gitlab en https://gitlab.com/maindufeu/ktbo-bi/-/settings/repository#js-deploy-keys-settings


después puede clonar este repositorio entero con 

git clone git@gitlab.com:maindufeu/ktbo-bi.git
