# Orla

Este repositório contém a aplicação Orla, uma assistente virtual construída com Flask, LangChain, OpenAI e ChromaDB. A aplicação realiza buscas por similaridade em um banco vetorial e serve respostas estruturadas via interface web.

Instalação

Faça o clone deste repositório:
git clone https://github.com/<seu-usuario>/Orla.git
cd Orla

Construindo o Banco Vetorial
python ConstruindoBancoDados.py

Executando a Aplicação

Inicie o servidor Flask executando:
python app.py

OBS: Nesse case é preciso alterar a API Key, dos dois codigo app.py e ConstruindoBancoDados.py para alguma atualmente ativa. Por questão segurança publiquei o arquivo no git mais cancelei a API Key da OpenIA
