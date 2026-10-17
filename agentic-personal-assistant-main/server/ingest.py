import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore, PineconeEmbeddings
from pinecone import Pinecone

def ingest_data(file_path: str):
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX")

    if not api_key:
        raise ValueError("Missing PINECONE_API_KEY")
    if not index_name:
        raise ValueError("Missing PINECONE_INDEX")

    pc = Pinecone(api_key=api_key)
    index = pc.Index(index_name)

    embeddings = PineconeEmbeddings(model="llama-text-embed-v2", pinecone_api_key=api_key)
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)

    batch_size = 96
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        vector_store.add_documents(batch)

    print("✅ Ingestion Complete!")
