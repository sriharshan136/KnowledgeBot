# KnowledgeBot: A Retrieval-Augmented AI Chatbot with LangChain and Hugging Face

KnowledgeBot is a powerful AI chatbot designed to provide relevant answers based on the vast amounts of knowledge integrated into its system. Leveraging LangChain for document processing and Hugging Face models for language understanding, KnowledgeBot is capable of retrieving and generating accurate responses from large datasets, allowing users to interact with a knowledge base through a conversational interface.

## Features

- **Retrieval-Augmented Generation (RAG)**: Utilizes LangChain's document processing capabilities to retrieve relevant context from a set of documents and enhance the model's answer generation.
- **Hugging Face Integration**: Integrates state-of-the-art models from Hugging Face (such as Mistral-Nemo-Instruct) to provide accurate, informative, and human-like responses.
- **Interactive Chat Interface**: Provides a simple chat interface for users to interact with the bot and get relevant answers from the knowledge base.
- **Customizable Knowledge Base**: Easily replace or update the knowledge base by modifying text documents, which can be processed and used for answering queries.

## Architecture

The architecture of KnowledgeBot is built on two main components:

1. **Backend (Flask)**: The backend is powered by Flask, which serves as the API to handle user queries. It uses LangChain for document processing, splitting, and retrieval, and Hugging Face for generating responses based on the query and context.
2. **Frontend (React)**: The frontend is a React application where users can interact with the chatbot. It communicates with the Flask API to send and receive messages.

## Technologies Used

- **LangChain**: A framework for building applications with LLMs (Large Language Models). LangChain handles the document loading, splitting, and retrieval logic.
- **Hugging Face**: Provides pre-trained models like `Mistral-Nemo-Instruct` for text generation, ensuring high-quality responses.
- **Flask**: A lightweight Python web framework used to build the backend API.
- **React**: The frontend of the chatbot, offering an interactive and responsive user experience.
- **Chroma**: Used for creating and managing the vector store, enabling fast retrieval of relevant documents.
- **WebSocket**: Provides real-time communication between the frontend and backend.

## Setup Instructions

### Backend Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/KnowledgeBot.git
   cd KnowledgeBot

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use venv\Scripts\activate
    
3. Install the necessary Python dependencies:

    ```bash
    pip install -r requirements.txt

4. Set up the .env file with your Hugging Face API token and other configurations:

    ```bash
    echo "HF_API_TOKEN=your_token_here" > .env
    
5. Start the Flask server:

    ```bash
    python app.py
    
6. The backend will now be running on http://127.0.0.1:5000.

### Frontend Setup

1. Navigate to the frontend folder and install dependencies:

    ```bash
    cd frontend
    npm install

2. Create a .env file inside the frontend folder and add the backend API URL:

    ```bash
    VITE_API_URL=http://127.0.0.1:5000

3. Start the React development server:

    ```bash
    npm run dev

4. The frontend will now be running on http://localhost:3000.

### Usage

- Open the frontend application in your browser.
- Type a query in the chat input box and click "Send" to submit the query.
- The chatbot will process the query, retrieve relevant documents from the backend, and return an answer based on the context.

### Example Query:

- **User**: "What is the company policy on vacation?"
- **KnowledgeBot**: "Employees are entitled to 15 days of paid vacation each year. Sick leave can be taken when necessary, but employees are encouraged to notify their manager in advance if possible."

### Contributing

- Contributions are welcome! If you'd like to improve or extend the functionality of KnowledgeBot, feel free to fork this repository and create a pull request. Please make sure to follow best practices and add appropriate tests for any new features.

### License

- This project is licensed under the MIT License - see the LICENSE file for details.

### Acknowledgments

- **LangChain**: A powerful framework for document processing and retrieval-augmented generation.
- **Hugging Face**: Providing state-of-the-art models for natural language understanding and generation.
- **Flask**: Lightweight web framework used to build the backend.
- **Chroma**: A vector store to handle document retrieval efficiently.
