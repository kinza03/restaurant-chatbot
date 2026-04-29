from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

load_dotenv()

def ingest_data():
    print("Loading restaurant data...")
    loader = TextLoader("data/restaurant_info.txt", encoding="utf-8")
    documents = loader.load()

    print("Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks")

    print("Creating embeddings and storing in Pinecone...")
    embeddings = OpenAIEmbeddings()
    
    vectorstore = PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name="restaurant-chatbot"
    )
    
    print("Done! Data stored in Pinecone.")

if __name__ == "__main__":
    ingest_data()