# RAG Workflow for LangChain and Ollama

This workflow demonstrates how to use RAG (Retrieval Augmented Generation) with LangChain.

## Diagram

```mermaid
sequenceDiagram
    autonumber
    actor User    
    User -->> Document Loader: Path
    Document Loader -->> Splitter: loaded text
    User -->> Embedding: select model
    Embedding -->> VectorStore: embedding    
    Splitter -->> VectorStore: splitted text    
    VectorStore -->> Retriever: search_type and search_kwargs
    User -->> Retriever: question      
    Retriever -->> LLM: formated context    
    activate LLM
    User -->> LLM: question
    LLM -->> User: response
    deactivate LLM
```

## Installation

需要本地运行Ollama。

```Bash
$ poetry install
```

## How to run

```Bash
$ poetry run python rag/main.py ./data/matches.txt 
```

Or 

```Bash
$ poetry shell
$ python rag/main.py ./data/matches.txt
```

## Issues

- Webscraper: Need to find a way to bypass the bot detection.