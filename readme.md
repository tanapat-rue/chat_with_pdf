# ReadMe

## 1) How Does It Work

This application allows you to chat with PDF documents using a backend powered by a language model and a PostgreSQL vector database for context storage. Here's the workflow:

- **PDF Processing**: The system reads PDF files from the `papers` directory, extracts text, and chunks it into manageable parts. Each chunk is then embedded into vector representations and stored in the PostgreSQL vector database.  
- **Contextual Chat**: When a user sends a chat request, the backend:
  - Retrieves previous messages from the session to maintain conversation history.  
  - Uses Retrieval-Augmented Generation (RAG) to find similar text chunks from the vector database based on the prompt.  
  - Enhances the user's prompt with the retrieved context and sends it to the language model.  
  - The response is returned to the user and stored in memory for ongoing conversation context.  

## 2) How to Run

To run the application, ensure you have Docker and Docker Compose installed. Execute the following command:

```bash
docker-compose -f docker-compose.yaml up -d
```

This command will spin up two Docker containers:
- **chat_db**: The PostgreSQL vector database that stores text embeddings for retrieval.  
- **chat_with_pdf**: The backend service that processes PDF files, handles chat requests, and communicates with the language model.  

## 3) How to Improve

To enhance the functionality and efficiency of this application, consider the following improvements:

- **Improve Memory Management**: Implement more sophisticated memory cognition techniques to manage larger contexts over extended conversations. This could include summarizing previous interactions to save memory.  
- **Incremental PDF Processing**: Since processing large PDFs can be time-consuming, allow for incremental or background processing, enabling the system to handle PDFs asynchronously without blocking other operations.  
- **Support Multiple LLM Models**: Enable the use of multiple language models to provide flexibility in choosing the best model for specific tasks or prompts, which can be particularly useful for optimizing cost and performance.  
- **Add Better Test Cases**: Implement more comprehensive test cases to ensure the robustness of the application, covering edge cases and simulating different usage scenarios to identify potential issues.