# POC - Speed Layer - Open Banking

Instruções de como executar esta POC.

## Visão Geral da Arquitetura

![Arquitetura - Visão Geral](SpeedLayer.jpg)

## Software Necessário

 1. **Git** instalado e configurado adequadamente.
 2. **Docker**.
 3. **Docker Compose**.

## Configuração

1 -  Certifique-se te possuir sua chave SSH configurada em sua conta do Git. *Para mais informações: https://tinyurl.com/3tw839jj*

 - Não utilize senhas durante a criação da chave SSH!
 
2 - Clone **este** repositório. *Para mais informações: https://tinyurl.com/6bhk89tz*

3 - Configuração do docker-compose.yml:

3 .1 - SOMENTE LINUX e MAC:

- Dê permissão de execução aos scripts:
`chmod +x *.sh`

- Execute o script e responda a cada pergunta com seus dados:
`./poc-setup-unix.sh`

3 .2 - SOMENTE WINDOWS: Substitua os comentários em docker-compose.yml com as suas próprias informações:
 
 - Mapeamento do volume do NiFi Registry: Diretório da sua chave ssh.
 - Seu nome.
 - Endereço de e-mail relacionado à sua conta do GitHub.

## Preparação

1 - Em um terminal, abra o diretório raiz do projeto.

2 - Execute: `./poc-start-unix.sh` .  *A primeira execução deste comando pode levar vários minutos.*

### Acesse as duas instâncias de NiFi
**Instância 1:** `http://localhost:8080/nifi`

**Instância 2:** `http://localhost:9090/nifi`

## Execução
**Em cada instância:**  Inicie os processadores do Process Group recém importado.

- Execute o script para iniciar a simulação de streaming
`./poc-stream.sh`

 - O arquivo speed-layer-2/streaming/input/adults.data será consumido e criado na pasta output linha a linha, simulando o streaming.
 
 Acesse o contêiner do MongoDB. Para isso, em um terminal, execute os seguintes comandos:

    sudo docker exec -it mongodb /bin/bash
        
    mongo

    use raw

    db.adults.find().pretty()

Para verificar a quantidade de registros inseridos:
`db.adults.count()`

Verifique que os registros da simulação de streaming estão sendo/foram inseridos.

Para verificar os registros através do Metabase:
`http://localhost:4000`

Email address: fiap@fiap.com
Password: fiap2021

Para manipulação dos dados inseridos, poderá ser utilizado o jupyter em python ou R, acessando:

`http://localhost:8888`

**Já possui uma notebook criado com conexão de teste ao banco**

## Encerrar
Há diversas maneiras de parar os contêineres. Rode algum dos seguintes comandos no diretório raiz do projeto: 

1 - Apenas para os contêineres. Nenhum dado é perdido:

`./poc-stop-unix.sh`

2 - Para os contêineres e os destrói: (Com exceção dos dados do MongoDB, todos os dados serão perdidos. Para também excluir os dados do MongoDB, exclua o seguinte diretório: `speed-layer/mongo`)

`./poc-rm-containers-unix.sh`

3 - Para deletar todos os dados persistidos pelo MongoDB:
`./poc-rm-persisted-data-unix.sh`

