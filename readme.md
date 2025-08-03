# Inbox2Action

**Inbox2Action** é um sistema que transforma e-mails bagunçados em tarefas estruturadas no ClickUp. Toda mensagem recebida por um endereço específico é encaminhada para uma IA, a qual é responsável por resumir o conteúdo e estruturá-lo em forma de tarefa, com definição de prazo e prioridade. Por fim, a tarefa é cadastrada automaticamente no ClickUp, uma plataforma de gestão de tarefas e projetos.

## Como funciona:

1. O domínio de e-mail deve ter os registros **TXT**, **MX** e **DKIM** configurados conforme os requisitos da AWS.
2. Dessa forma, será possível registrar uma regra de recebimento no **AWS Simple Email Service (SES)**. Seu papel é armazenar as mensagens recebidas por um endereço específico em um **Bucket do S3** e publica uma mensagem em um tópico do **Simple Notification Service (SNS)**.
3. Após o salvamento do arquivo, uma **AWS Lambda**, em **Python**, é disparada via SNS. A função utiliza a biblioteca **boto3** para ler o e-mail, envia seu conteúdo para a **API da OpenAI** e recebe uma tarefa estruturada, com nome, descrição, prazo e prioridade. Com esses dados, o sistema usa a **API do ClickUp** para cadastrar o registro.

## Resultado:

[Clique aqui para assistir](https://www.youtube.com/watch?v=dOFVlCA9mD4)

Um fluxo inteligente que transforma e-mails em tarefas organizadas de acordo com sua prioridade. Com isso, diminuímos o ruído da caixa de entrada e favorecemos a gestão de tempo e tomada de decisão.

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