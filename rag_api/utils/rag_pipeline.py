from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from langchain_cohere import CohereEmbeddings
from dotenv import load_dotenv
load_dotenv()

# embedding_model = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )

# embedding_model = OpenAIEmbeddings(
#     api_key=os.getenv("OPENAI_API_KEY")
# )

# embedding_model = GoogleGenerativeAIEmbeddings(
#     model="models/embedding-001",
#     google_api_key=os.getenv("GOOGLE_API_KEY"),
#     transport="rest"
# )

embedding_model = CohereEmbeddings(
    model="embed-english-v3.0",
    cohere_api_key=os.getenv("COHERE_API_KEY")
)



def process_pdf(pdf_path,user_id):

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    documents = documents[3:]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=80
    )

    chunks = splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(chunks, embedding_model)

    vectorstore.save_local(f"vectordb/{user_id}")

    return len(chunks)