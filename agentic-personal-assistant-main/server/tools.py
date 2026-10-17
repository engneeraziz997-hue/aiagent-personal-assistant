import os
from langchain_core.tools import tool
from langchain_pinecone import PineconeVectorStore, PineconeEmbeddings
from pinecone import Pinecone

_vector_store = None

def get_vector_store():
    global _vector_store
    if _vector_store is not None:
        return _vector_store

    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX")

    if not api_key:
        raise ValueError("Missing PINECONE_API_KEY")
    if not index_name:
        raise ValueError("Missing PINECONE_INDEX")

    pc = Pinecone(api_key=api_key)
    index = pc.Index(index_name)

    embeddings = PineconeEmbeddings(model="llama-text-embed-v2", pinecone_api_key=api_key)
    _vector_store = PineconeVectorStore(index=index, embedding=embeddings)
    return _vector_store

@tool
def search_knowledge_base(query: str) -> str:
    """Searches the internal knowledge base for technical info and documentation. Use this when you need to find information from uploaded PDF documents."""
    print(f'🔍 Agent is searching Pinecone for: "{query}"')

    try:
        store = get_vector_store()
        results = store.similarity_search(query, k=10)

        for i, r in enumerate(results):
            print(f"Result {i + 1}:", r.page_content[:200])

        if not results:
            return "No relevant information found in the knowledge base."

        return "\n\n---\n\n".join([doc.page_content for doc in results])
    except Exception as e:
        print(f"❌ Error during knowledge base search: {e}")
        return f"Error searching knowledge base: {str(e)}"
