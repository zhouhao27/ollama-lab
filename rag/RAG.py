import ollama 
import os
from typing import List
from xml.dom.minidom import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class RAG:
    def __init__(self, path, question):
        self.path = path
        self.question = question

    def __load__(self, path: str) -> List[Document]:
        loader = None
        # Use extension to judge the file type. It's not accurate but it's good enough for now.
        if os.path.isdir(path):
            print("Directory")
            loader = DirectoryLoader(path)
        elif path.endswith('.pdf'):
            print("PDF")
            loader = PyMuPDFLoader(path)
        elif path.endswith('.txt'):
            print("Text")
            loader = TextLoader(path)
        elif path.endswith('.html'):
            print("HTML")
            loader = WebBaseLoader(path)

        if loader is None:
            print("Invalid file type")
            return None

        return loader.load() 

    def __ollama_llm__(self, question, context=None): 
        formatted_prompt = f'Question: {question}\n\n\nContext: {context}' if context is not None else question
        response = ollama.chat(model='llama3', messages=[{"role": "user", "content": formatted_prompt}])
        return response['message']['content']

    def __combin_docs__(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def query_without_rag(self):
        return self.__ollama_llm__(question=self.question)

    def query_with_rag(self):
        # 1. Load document
        docs = self.__load__(self.path)

        # 2. Split the text
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        # 3. Create embeddings and vector store
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

        # 5. RAG setup
        retriever = vectorstore.as_retriever()
        retrieved_docs = retriever.invoke(self.question)
        formatted_context = self.__combin_docs__(retrieved_docs)

        return self.__ollama_llm__(question=self.question, context=formatted_context)
    





