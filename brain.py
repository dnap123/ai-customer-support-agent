import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()

# Global variable to store the "brain"
vector_store = None

def initialize_brain():
    global vector_store
    print("Loading PDF and building brain... (this takes a moment)")
    
    # 1. Load the PDF
    try:
        # Check if file exists first
        if not os.path.exists("manual.pdf"):
            print("ERROR: 'manual.pdf' not found in this folder.")
            return

        loader = PyPDFLoader("manual.pdf")
        docs = loader.load()
    except Exception as e:
        print(f"Error loading PDF: {e}")
        return

    # 2. Split text into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = splitter.split_documents(docs)

    # 3. Create Embeddings
    embeddings = OpenAIEmbeddings()
    
    # 4. Store in a Vector Database
    vector_store = FAISS.from_documents(split_docs, embeddings)
    print("Brain built!")

def format_docs(docs):
    """Helper to combine multiple chunks of text into one block."""
    return "\n\n".join(doc.page_content for doc in docs)

def ask_question(question_text):
    if not vector_store:
        initialize_brain()
        
    if not vector_store:
        return "System Error: Brain failed to load. Check PDF file."

    # 1. Setup the LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # 2. Create the prompt template
    prompt = ChatPromptTemplate.from_template("""
    Answer the user's question based ONLY on the following context:
    <context>
    {context}
    </context>
    
    Question: {input}
    """)

    # 3. Setup the Retriever (The Librarian)
    retriever = vector_store.as_retriever()

    # 4. Build the Chain (The RAG Pipeline)
    # This says: "Take input -> Fetch Docs -> Format them -> Send to Prompt -> Send to LLM -> Parse String"
    rag_chain = (
        {"context": retriever | format_docs, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # 5. Get the answer
    print(f"DEBUG: Asking AI: {question_text}")
    try:
        answer = rag_chain.invoke(question_text)
        return answer
    except Exception as e:
        print(f"Error during AI generation: {e}")
        return "I'm sorry, I encountered an error processing your request."

if __name__ == "__main__":
    # Test it locally
    initialize_brain()
    print(ask_question("How do I turn this device on?"))