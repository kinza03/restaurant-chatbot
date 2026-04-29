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
If you don't know something, politely say you're not sure and suggest they call 0300-1234567.
Always be warm and professional.
Keep answers concise.
IMPORTANT: Always respond in the same language the user is writing in. If they write in Urdu, respond in Urdu. If they write in Roman Urdu, respond in Roman Urdu. If they write in English, respond in English. Match the user's language exactly.

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