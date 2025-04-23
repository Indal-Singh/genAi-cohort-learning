from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

import os

pdf_path = Path(__file__).parent / "nodejs.pdf"

loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

text_spliter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200,
)

split_docs = text_spliter.split_documents(documents=docs)

embedder = OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key=os.getenv("OPENAI_API_KEY")
)

# vector_store = QdrantVectorStore.from_documents(
#     documents=[],
#     url="http://localhost:6333",
#     collection_name="pdf_content_collection",
#     embedding=embedder
# )

# vector_store.add_documents(documents=split_docs)
# print("Injection completed.")

retriver = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="pdf_content_collection",
    embedding=embedder
)


search_result = retriver.similarity_search(
    query="What is FS express?"
)


print("Relevant Chunks", search_result)