# chatterpi

This is the codebase for chatterpi's server, built using FastAPI in Python. The motivation for using a python framework comes from the AI ecosystem and libraries available in Python. 

FastAPI has a system of type hints - essentially a type system, and automatic documentation generator, and asynchronous code suport.

### Installing pip

pip is package manager for python and can be downloaded and installed as follows:

Linux 
``` bash
python -m ensurepip --upgrade
```


Windows
``` bash
py -m ensurepip --upgrade
```

### Installing FastAPI and uvicorn

FastAPI and what is used to serve projects built in it, uvicorn (an ASGI), can both be downloaded and installed using the following command

``` bash
pip install "fastapi[all]"
```

### Installing Dependencies

The dependencies 

```bash
pip install -r requirements.txt
```

### Running the project

Assuming a `main.py` file for the entry point of the project, the following command is used to run the project.

``` bash
uvicorn main:app --reload 
```

main is python module
app is application object
--reload is for restart on code changes (To be used in dev)

http://127.0.0.1:8000/

For interactive docs,
go to the root/docs
http://127.0.0.1:8000/docs

Alternative documentation is at
root/redoc
http://127.0.0.1:8000/redoc

For OpenAPI 
root/openapi.json
http://127.0.0.1:8000/openapi.json

### Running the ChromaDB

## Creating an Embedding File

This command creates a .pkl file by going over all the pdfs from the pdf pool and extracting all the sentences from the pdfs, later to be used as a context. 

``` bash
python chroma/create_embeddings.py
```

## Retrieving an Embedding File

This command retreives all the embeddings from the embeddings.pkl and creates a collection in the get_embeddings.py file. This file can then be used to run commands and queries on those embeddings.

``` bash
python chroma/get_embeddings.py
```
