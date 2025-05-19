from flask import Flask, render_template, request, session
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (SystemMessagePromptTemplate,HumanMessagePromptTemplate,ChatPromptTemplate,)
from langchain.vectorstores import Chroma

app = Flask(__name__)

# --- Define a função de busca por similaridade ---
def dsa_busca_similaridade(query: str, k: int = 3):
    return vectordb.similarity_search(query, k=k)

# Chaves e configurações do vector store
index_name = 'dsa-pgs'
persist_dir = "chroma_data"

#### Star Usando Banco Vectorial ######
gerador_embeddings = OpenAIEmbeddings(api_key='sk-VQPqGxsD9CsiIxXyDMoZra7mZqCrCuzkYYQz2914mrT3BlbkFJ7y8UgsBto7W_lwMS4XrkO_TmFF3NAm0Gzw0VAZFhIA')
index_name = 'dsa-pgs'
persist_dir = "chroma_data"

vectordb = Chroma(persist_directory=persist_dir, embedding_function=gerador_embeddings, collection_name=index_name)
###### END

chat_model = ChatOpenAI(
    openai_api_key='sk-VQPqGxsD9CsiIxXyDMoZra7mZqCrCuzkYYQz2914mrT3BlbkFJ7y8UgsBto7W_lwMS4XrkO_TmFF3NAm0Gzw0VAZFhIA',
    model_name="gpt-4o-mini",
    temperature=0.1,
    max_tokens=150,
)

# Prompt templates
system_template = """
                Você é uma assistente virtual da Orla Tech, respondendo dúvidas apenas sobre o conteúdo do site.
                Crie respostas estruturadas. em formato de itens, dexe em negritos os topicos.
                Responda sempre de forma honesta, sem viés de gênero, etnia, religião, orientação sexual ou qualquer outra característica pessoal.  
                Não gere conteúdo que incentive desinformação, discurso de ódio, ou atitudes ilegais.  
                Preserve a privacidade: não solicite dados pessoais sensíveis nem os divulgue.
                Use o contexto extraído dos documentos abaixo, e se a pergunta estiver fora de escopo, reposta que não foi possivel obter essa informação.Contexto:{context}
            """

system_prompt = SystemMessagePromptTemplate.from_template(system_template)
human_prompt = HumanMessagePromptTemplate.from_template("{mensagem}")
chat_prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])

# --- Define a função de busca por similaridade ---
def dsa_busca_similaridade(query: str, k: int = 3):
    return vectordb.similarity_search(query, k=k)


@app.route('/', methods=['GET', 'POST'])
def home():
    resposta = ""
    if request.method == "POST":
        mensagem = request.form.get("query", "").strip()
        if mensagem:
            # Recupera contexto relevante
            docs = dsa_busca_similaridade(mensagem, k=3)
            context = "\n".join(doc.page_content for doc in docs)

            # Formata e envia para o LLM
            messages = chat_prompt.format_messages(mensagem=mensagem, context=context)
            response = chat_model(messages)
            resposta = response.content

    return render_template("index.html", resposta=resposta, history=session.get("history"))

if __name__ == '__main__':
    app.run(debug=True)
