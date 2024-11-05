import fitz  # PyMuPDF for PDF reading
import openai
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import Table
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
import re

# Replace with your actual database URL

class Rag:
    def __init__(self) -> None:
        DATABASE_URL = "postgresql+psycopg2://postgres:postgres@db:5432/chat_db"
        engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=engine)


    def extract_text_from_pdf(self, file_path):
        """Extract text from a given PDF file."""
        print(file_path)
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text


    def get_embedding(self, text_to_embed):

        response = openai.embeddings.create(
            model= "text-embedding-ada-002",
            input=[text_to_embed]
        )
        
        return response.data[0].embedding # Change this

    def embed_text(self, text):
        """Embed the text using OpenAI's embedding model."""
        return self.get_embedding(text_to_embed=text) # Adjust model if necessary

    def store_embedding(self, vector, text_content, paper_name):
        """Store the embedded text in the PostgreSQL database using a raw SQL INSERT INTO statement."""
        with self.Session() as session:
            try:
                # Convert the vector (list of floats) to a PostgreSQL array string
                vector_str = '[' + ','.join(map(str, vector)) + ']'
                
                # Prepare the SQL INSERT INTO statement
                insert_sql = text("""
                    INSERT INTO papers_vectors (vector, text, paper_name)
                    VALUES (:vector, :text, :paper_name)
                """)
                
                # Execute the SQL statement with parameters
                session.execute(insert_sql, {
                    'vector': vector_str,
                    'text': text_content,
                    'paper_name': paper_name
                })
                session.commit()
            except OperationalError as e:
                raise e



    def chunk_text(self, text, max_chars=5000):
        """Split text into chunks that comply with the character limit without breaking words."""
        
        words = re.findall(r'\S+\s*', text)
        chunks = []
        current_chunk = ''
        for word in words:
            if len(current_chunk) + len(word) <= max_chars:
                current_chunk += word
            else:
                chunks.append(current_chunk)
                current_chunk = word
        if current_chunk:
            chunks.append(current_chunk)
        return chunks

    

    def query_similar_text(self, query_text):
        """Query the database for similar text using vector similarity."""
        query_vector = self.embed_text(query_text)

        with self.Session() as session:
            result = session.execute(
                text("""
                    SELECT text, paper_name, vector
                    FROM papers_vectors
                    ORDER BY vector <-> :query_vector LIMIT 1;
                """),
                {'query_vector': str(query_vector)}
            ).fetchall()
            
        return result
