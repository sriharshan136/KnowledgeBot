from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFaceEndpoint
import logging
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve Hugging Face access token from environment variables
HF_ACCESS_TOKEN = os.getenv("HF_ACCESS_TOKEN")
if not HF_ACCESS_TOKEN:
    raise RuntimeError("Hugging Face access token is missing. Ensure it's set in the .env file.")

# Step 1: Initialize Flask app
app = Flask(__name__)
CORS(app)

# Step 2: Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Step 4: Document Processing
def process_documents():
    try:
        loader = TextLoader("raw_data.txt")  # Load the document
        documents = loader.load()           # Convert to LangChain document format

        # Split into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        return texts
    except FileNotFoundError:
        logger.error("Error: raw_data.txt file not found.")
        return []
    except Exception as e:
        logger.error(f"Error processing documents: {e}")
        return []

texts = process_documents()
if not texts:
    raise RuntimeError("No documents were loaded for processing.")

# Step 5: Embedding Generation
embeddings = HuggingFaceEmbeddings()  # Default uses 'sentence-transformers/all-mpnet-base-v2'

# Step 6: Vector Store Creation with Persistence
db = Chroma.from_documents(
    texts,
    embeddings,
    persist_directory="chroma_db"  # Add persistence for larger datasets
)
db.persist()

# Step 7: Language Model Integration
try:
    response = requests.get("https://api-inference.huggingface.co/models/mistralai/Mistral-Nemo-Instruct-2407")
    if response.status_code != 200:
        logger.error("Error: Unable to connect to Hugging Face model endpoint.")
        raise RuntimeError("Hugging Face model endpoint is unavailable.")
except requests.exceptions.RequestException as e:
    logger.error(f"Connection error: {e}")
    raise

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-Nemo-Instruct-2407",
    task="text-generation",
    max_new_tokens=512,
    do_sample=False,
    repetition_penalty=1.03,
    huggingfacehub_api_token=HF_ACCESS_TOKEN
)

# Step 8: Question-Answering Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # Concatenates retrieved context into a single prompt
    retriever=db.as_retriever(),
    return_source_documents=True
)

# Step 9: Define API Route
@app.route('/query', methods=['POST'])
def query():
    user_query = request.json.get("query")  # Extract query from POST request
    if not user_query:
        logger.error("Query parameter is missing.")
        return jsonify({"error": "Query parameter is missing"}), 400

    try:
        # Get response from the QA chain
        response = qa_chain({"query": user_query})
        answer = response["result"]
        source_docs = [doc.page_content for doc in response["source_documents"]]

        return jsonify({
            "answer": answer,
            "sources": source_docs
        })
    except Exception as e:
        logger.error(f"Error in QA chain: {e}")
        return jsonify({"error": "Internal server error"}), 500

# Step 10: Run the Flask App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)  # Debug should be False in production

#End

