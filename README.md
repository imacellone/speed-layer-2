# POC - Speed Layer - Open Banking

#### Avisos
- Todos os comandos demonstrados devem ser executados no diretório raiz do projeto;
- Esta documentação não suporta Windows, apesar de a POC, em si, suportá-lo;


## Visão Geral da Arquitetura

![Arquitetura - Visão Geral](SpeedLayer.jpg)

## Pré-requisitos para a execução

 1. **Git**.
 2. **Docker**.
 3. **Docker Compose**.

## Configuração

1 -  Certifique-se de possuir chaves SSH **(SEM SENHA)** configuradas em sua máquina;

2 - Clone **este** repositório;

3 - Dê permissão de execução aos scripts:

`chmod +x *.sh`

4 - Execute o script e responda a cada pergunta com seus dados:

`./setup.sh`

## Execução
1 - `./start.sh`
*A primeira execução deste comando pode levar vários minutos.*

Este script irá:
- Criar todos os contêineres (Veja o desenho arquitetural acima);
- Fazer o deploy de todas as instâncias de Apache NiFi;
- Iniciar todos os process groups do Apache NiFi;
- Após um delay de 2 minutos, iniciar a simulação do streaming de dados;
 
## MongoDB
Após os dados serem processados pelo Apache NiFi, eles são inseridos no database **raw**, na collection **adults**.
Para acessá-los:

    ./mongo.sh
    mongo
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

`./rm-containers.sh`

2- Para remover todos os dados persistidos pelo MongoDB:

`./rm-persisted.sh`


## Scripts
1 - `setup.sh`
- Permite a configuração de campos necessários no docker-compose.yml automaticamente;

2 - `start.sh`
- Inicia todos os contêineres;
- Faz deploy de todos os process groups nas instâncias de Apache NiFi;
- Inicia todos os process groups de todas as instâncias;
- Inicia a simulação do streaming;

3 - `tail-streaming.sh`
- Permite acompanhar em tempo real as linhas geradas pelo simulador de streaming;

4 - `rm-containers.sh`
- Destrói todos os contêineres;
- Os dados persistidos pelo MongoDB são mantidos;

5 - `rm-persisted.sh`
- Remove os dados persistidos pelo MongoDB;
- Remove os arquivos gerados para simular o streaming;
