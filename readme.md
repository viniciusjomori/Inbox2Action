# Inbox2Action

**Inbox2Action** é um sistema que transforma e-mails bagunçados em tarefas estruturadas no ClickUp. Toda mensagem recebida por um endereço específico é encaminhada para uma IA, a qual é responsável por resumir o conteúdo e estruturá-lo em forma de tarefa, com definição de prazo e prioridade. Por fim, a tarefa é cadastrada automaticamente no ClickUp, uma plataforma de gestão de tarefas e projetos.

## Como funciona:

1. O domínio de e-mail deve ter os registros **TXT**, **MX** e **DKIM** configurados conforme os requisitos da AWS.
2. Dessa forma, será possível registrar uma regra de recebimento no **AWS Simple Email Service (SES)**. Seu papel é armazenar as mensagens recebidas por um endereço específico em um **Bucket do S3** e publica uma mensagem em um tópico do **Simple Notification Service (SNS)**.
3. Após o salvamento do arquivo, uma **AWS Lambda**, em **Python**, é disparada via SNS. A função utiliza a biblioteca **boto3** para ler o e-mail, envia seu conteúdo para a **API da OpenAI** e recebe uma tarefa estruturada, com nome, descrição, prazo e prioridade. Com esses dados, o sistema usa a **API do ClickUp** para cadastrar o registro.

## Resultado:

[Clique aqui para assistir](https://www.youtube.com/watch?v=dOFVlCA9mD4)

Um fluxo inteligente que transforma e-mails em tarefas organizadas de acordo com sua prioridade. Com isso, diminuímos o ruído da caixa de entrada e favorecemos a gestão de tempo e tomada de decisão.

## Deploy

### 1. Domínio
* Compre um domínio
* Crie uma identidade no Amazon SES
* Configure o TXT, MX e DKIM de acordo com as informações passadas pela AWS

### 2. ClickUp
* Abra uma conta no ClickUp
* Crie um espaço, listas e adicione uma descrição nas listas. O Inbox2Action usará essas descrições para determinar o local correto para cadastro da tarefa
* Copie a url do site para obter o ID do espaço e ID do time: `https://app.clickup.com/{teamId}/v/o/s/{spaceId}`
* Adquira a chave de API do ClickUp

### 3. OpenAi
* Abra uma conta na OpenAi e compre créditos
* Adquira a chave de API da OpenAI

### 4. Grupo de Regra de Recebimento de Email
* Na Console da AWS, no serviço Amazon Simple Email Service (SES), crie um grupo de regra de recebimento de e-mail
* Habilite o grupo

### 5. AWS CLI
* Instale a `AWS CLI`
* Crie um usuário no IAM e adquira suas chaves
* No terminal, execute o comando `aws configure`, para realizar a autenticação e escolher em qual região ocorrerá o deploy

### 6. Configuração de ambiente
* Na raiz do projeto, crie um diretório chamado `env`
* Nesse diretório, crie um arquivo `.json`. O nome do arquivo será o nome do ambiente: `env/dev.json`
* No Json, coloque essas informações:

```
{
    "username": "Seu nome",
    "openai": {
        "apiKey": "Chave de API da OpenAI"
    },
    "clickUp": {
        "apiKey": "Chave de API do ClickUp",
        "teamId": "ID do time",
        "spaceId": "ID do espaço"
    },
    "email": {
        "receiptRuleSet": "Nome do grupo de regra para recebimento de e-mail",
        "address": "Endereço de e-mail a receber as tarefas",
        "name": "Nome do remetente para enviar as mensagens de confirmação",
        "bcc": "Endereço de e-mail a receber todas as mensagens da aplicação (em cópia oculta)"
    },
    "log": {
        "level": "Nível de log a ser exibido no CloudWatch. Escolha um entre 'CRITICAL', 'ERROR', 'WARNING', 'INFO' e 'DEBUG'"
    }
}
```

### 7. Docker
* Instale o Docker
* Inicie o Docker Desktop

### 8. CDK
* Instale o `Node.js` e `AWS CDK`
* Caso seja sua primeira vez usando CDK, execute o comando `cdk bootstrap`, para instanciar os recursos padrão
* Execute o comando `cdk diff`, para visualizar os recursos a serem criados para o projeto
* Após seguir todos os passos anteriores, execute o comando `cdk deploy --require-approval never`, para criar todos os recursos e colocar a aplicação em produção

## Tecnologias

* **AWS Lambda**: Serviço de computação serverless da AWS usado para executar automaticamente a função que processa o e-mail salvo no S3.

* **Python**: Linguagem principal utilizada na imagem da AWS Lambda, a qual define todo o *core* do projeto.

* **Amazon Simple Email Service (SES)**: Utilizado para receber e-mails. Através de uma regra de recebimento, os e-mails são armazenados em um bucket do S3.

* **Amazon Simple Notification Service (SNS)**: Atua como intermediário entre o SES e a Lambda. Após o recebimento e armazenamento do e-mail no S3, o SES publica uma mensagem ao tópico SNS, que por sua vez aciona a função Lambda responsável por processar o conteúdo da mensagem.

* **AWS S3**: Armazena os e-mails recebidos pelo SES em formato `.eml`, que são posteriormente lidos pela Lambda.

* **AWS CloudWatch**: Serviço de monitoramento da AWS, usada para armazenar e visualizar os logs da função Lambda. Integrado com a lib `logging` do Python.

* **DNS (TXT, MX, DKIM)**: Configurações de autenticação de domínio necessárias para que o SES possa receber e-mails de forma segura e confiável.

* **CDK (TypeScript)**: Utilizado para provisionar toda a infraestrutura AWS do projeto, através de IoC (Infrastructure as Code).

* **OpenAI API**: Responsável por interpretar o conteúdo dos e-mails e gerar tarefas estruturadas, com nome, descrição, prazo e prioridade.

* **PydanticAI**: Biblioteca baseada em Pydantic que ajuda na validação e estruturação do retorno da OpenAI, garantindo que os dados sigam um modelo bem definido.

* **ClickUp API**: Usada para criar automaticamente as tarefas estruturadas dentro de um espaço e lista específicos no ClickUp.

* **boto3**: Biblioteca oficial da AWS para Python, utilizada para interagir com os serviços S3 e SES dentro da função Lambda.

* **Docker**: Utilizado para configurar o ambiente da função Lambda, permitindo a inclusão de pacotes externos e bibliotecas nativas que não estão disponíveis no ambiente padrão da AWS.