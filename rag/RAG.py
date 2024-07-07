from urllib.parse import urlparse
import ollama 
import os
from typing import List
from xml.dom.minidom import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import FireCrawlLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class RAG:
    def __init__(self, path, question, prompt):
        self.path = path
        self.question = question
        # System prompt
        self.prompt = prompt 

        self.persistent_directory = self.__create_db_directory()
        # Check if the Chroma vector store already exists
        if not os.path.exists(self.persistent_directory):
            self.__create_vector_store__()
        else:
            print(
                f"Vector store {self.persistent_directory} already exists. No need to initialize.")

    def __create_vector_store__(self):
        
        # 1. Load documents
        docs = self.__load__(self.path)
        if docs is None:
            print("No documents found")
            return
        
        # Convert metadata values to strings if they are lists
        for doc in docs:
            for key, value in doc.metadata.items():
                if isinstance(value, list):
                    doc.metadata[key] = ", ".join(map(str, value))

        # Step 2: Split the crawled content into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        split_docs = text_splitter.split_documents(docs)

        # 3. Create embeddings for the document chunks
        embeddings = OllamaEmbeddings(model="nomic-embed-text")

        # 4. Create and persist the vector store with the embeddings
        vectorstore = Chroma.from_documents(
            documents=split_docs, 
            embedding=embeddings,
            persist_directory=self.persistent_directory,
        )

    def __load__(self, path: str) -> List[Document]:
        loader = None
        # Use extension to judge the file type. It's not accurate but it's good enough for now.
        if os.path.isdir(path):
            loader = DirectoryLoader(path)
        elif path.endswith('.pdf'):            
            loader = PyMuPDFLoader(path)
        elif path.endswith('.txt'):            
            loader = TextLoader(path)
        elif path.endswith('.html'):            
            loader = WebBaseLoader(path)
        elif RAG.is_valid_url(path):
            loader = FireCrawlLoader(
                api_key='fc-7090c52264864b56baeb4f0dcc1d8d08',
                url=path,
                mode='scrape' # 'scrape' or 'crawl', 'scrape' is for one page, 'crawl' is for multiple pages
            )
        if loader is None:
            print("Invalid file type")
            return None

        return loader.load() 

    def __ollama_llm__(self, question, context=None): 
        formatted_prompt = f'Question: {question}\n\n\nContext: {context}' if context is not None else question
        response = ollama.chat(model='llama3', messages=[
            {"role": "system", "content": self.prompt},
            {"role": "user", "content": formatted_prompt}
        ])
        return response['message']['content']

    def __combin_docs__(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def query_without_rag(self):
        return self.__ollama_llm__(question=self.question)

    def query(self):
        # Load the vector store with the embeddings
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        vectorstore = Chroma(
            persist_directory=self.persistent_directory,
            embedding_function=embeddings
        )
        # 5. RAG setup
        retriever = vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": 3, "score_threshold": 0.6},
        )
        retrieved_docs = retriever.invoke(self.question)
        formatted_context = self.__combin_docs__(retrieved_docs)

        return self.__ollama_llm__(question=self.question, context=formatted_context)
    
    @staticmethod
    def is_valid_url(url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def __create_db_directory(self) -> str:
        # Get current directory        
        current_dir = os.path.abspath(os.getcwd())
        db_dir = os.path.join(current_dir, "db")
        print(f'Creating db directory: {db_dir}')
        return db_dir


