from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv

load_dotenv()

def load_chain():
    embeddings = OpenAIEmbeddings()
    
    vectorstore = PineconeVectorStore(
        index_name="restaurant-chatbot",
        embedding=embeddings
    )
    
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )
    
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.2
    )

    prompt = ChatPromptTemplate.from_template("""You are a helpful and friendly assistant for Spice Garden Lahore restaurant.
Answer questions only based on the context provided below.
Always be warm and professional.
Keep answers concise.

LANGUAGE RULES — FOLLOW STRICTLY:
1. Detect the language the user is writing in.
2. Respond ENTIRELY in that same language — no exceptions.
3. If user writes in Urdu script — respond 100% in Urdu script including dish names translated to Urdu.
4. If user writes in English — respond 100% in English including dish names in English.
5. If user writes in Roman Urdu — respond 100% in Roman Urdu.
6. NEVER mix two languages in a single response under any circumstances.
7. Dish names in Urdu: Chicken Tikka = چکن ٹکہ, Seekh Kebab = سیخ کباب, Lahori Karahi = لاہوری کڑاہی, Mutton Handi = مٹن ہانڈی, Grilled Fish = گرلڈ مچھلی, Vegetable Biryani = سبزی بریانی, Crispy Calamari = کرسپی کلماری, Family Deal = فیملی ڈیل, Lunch Special = لنچ اسپیشل.

CONTACT NUMBER RULES:
Always write the contact number as 0300-1234567 in all languages including Urdu. Never reverse or change the number format.

ANSWERING RULES:
1. Only answer from the context provided below.
2. If the answer is not in the context say you are not sure and suggest contacting the restaurant at 0300-1234567.
3. If user asks to see the menu or what dishes are available always list all dishes with prices.
4. Never make up prices, times, or any information not in the context.

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