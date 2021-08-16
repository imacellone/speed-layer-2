# POC - Speed Layer - Open Banking

#### Avisos
- Todos os comandos demonstrados devem ser executados no diretório raiz do projeto;
- Esta documentação não suporta Windows, apesar de a POC, em si, suportá-lo;


## Visão Geral da Arquitetura

![Arquitetura - Visão Geral](SpeedLayer.jpg)

## Pré-requisitos para a execução

 1. **Git** instalado e configurado adequadamente.
 2. **Docker**.
 3. **Docker Compose**.

## Configuração

1 -  Certifique-se de possuir chaves SSH **(SEM SENHA)** configuradas em sua máquina.
 
2 - Clone **este** repositório.

3 - Dê permissão de execução aos scripts:

`chmod +x *.sh`

4 - Execute o script e responda a cada pergunta com seus dados:

`./poc-setup-unix.sh`

## Execução
1 - `./poc-start-unix.sh`
*A primeira execução deste comando pode levar vários minutos.*

Este script irá:
- Criar todos os contêineres (Veja o desenho arquitetural acima);
- Fazer o deploy de todas as instâncias de Apache NiFi;
- Iniciar todos os process groups do Apache NiFi;
- Após um delay de 2 minutos, iniciar a simulação do streaming de dados;
 
## Acesso ao MongoDB
    ./poc-open-mongo.sh
    use raw
    db.adults.find().pretty()

Para verificar a quantidade de registros inseridos:

`db.adults.count()`

## Metabase
Utilize-o para verificar os registros, conforme são inseridos:

### URL
`http://localhost:4000`

### Credenciais
E-mail: `fiap@fiap.com`

Password: `fiap2021`

## Jupyter
Para manipular, com Python ou R, os dados persistidos no MongoDB, acesse:

`http://localhost:8888`

**Há um Notebook criado com uma conexão ao banco de dados.**

## Encerrar
1 - Para os contêineres e os destrói (Com exceção dos dados do MongoDB, todos os dados serão perdidos):

`./poc-rm-containers-unix.sh`

2- Para remover todos os dados persistidos pelo MongoDB:

`./poc-rm-persisted-data-unix.sh`

