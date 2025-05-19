from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain.llms import OpenAI


#Função simples para coletar links internos
def coletar_links_internos(url_base, path_prefix=None):
    resp = requests.get(url_base)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    base_domain = urlparse(url_base).netloc

    urls = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # normaliza URL relativa
        full = urljoin(url_base, href)
        parsed = urlparse(full)
        # filtra mesmo domínio e (opcional) prefixo de caminho
        if parsed.netloc == base_domain:
            if path_prefix is None or parsed.path.startswith(path_prefix):
                urls.add(full)
    return list(urls)

#Coleta todos os links desejados
url_inicial = "https://www.orla.tech"
# por exemplo queremos apenas /home-portugues/*
links = coletar_links_internos(url_inicial, path_prefix="/home-portugues/")
# inclui também a página principal, se desejar
links.append(url_inicial)
links = list(set(links))

print(f"URLs encontradas: {len(links)}")

# supondo que `links` seja sua lista de URLs
documents = []
for url in links:
    loader = WebBaseLoader(web_path=url)
    documents += loader.load()

# --- Criação do banco de dados vetorial (usando Chroma) ---
gerador_embeddings = OpenAIEmbeddings(api_key='sk-VQPqGxsD9CsiIxXyDMoZra7mZqCrCuzkYYQz2914mrT3BlbkFJ7y8UgsBto7W_lwMS4XrkO_TmFF3NAm0Gzw0VAZFhIA')
index_name = 'dsa-pgs'

# Cria o vector store utilizando os documentos completos (sem text splitting)
index = Chroma.from_documents(documents, gerador_embeddings, collection_name=index_name, persist_directory="chroma_data")

print("O índice (vector store) foi criado com sucesso.")