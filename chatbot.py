from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

def load_chain():
    embeddings = OpenAIEmbeddings()
    
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.2
    )

    prompt = ChatPromptTemplate.from_template("""You are a helpful and friendly assistant for Spice Garden Lahore restaurant.
Answer questions only based on the context provided below.
If the question is not related to the restaurant, politely say you can only help with restaurant related questions like menu, deals, reservations and hours.
Always be warm and professional.
Keep answers concise.

Context: {context}

Question: {question}

Answer:""")

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain