import fitz
from fastapi import HTTPException , status
from sentence_transformers import SentenceTransformer
from ..database import conn,cur
import os
from dotenv import load_dotenv 
from groq import Groq

load_dotenv()
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def extract_text(file_path:str)->str:
    try:
        with fitz.open(file_path) as pdf_doc:
            total_pages = pdf_doc.page_count
            if(total_pages==0):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="File is structurally corrupt or contains no readable pages")
            text=""
            for page_num in range(total_pages):
                page = pdf_doc.load_page(page_num)
                text+= page.get_text()
            if(len(text)==0):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="File containes no text")
        return text
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="file doesn't exist")
    except fitz.FileDataError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The processed file is empty (0 bytes)")
    except fitz.EmptyFileError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The file is not a valid PDF or is badly corrupted.")
    except Exception as e:
        print("ERROR: " ,e)


def chunk_text(text:str, chunk_length = 1000,chunk_overlap=200) -> list[str]:
    chunks = []
    start_pos= 0
    while start_pos < len(text):
        chunk = text[start_pos:start_pos+chunk_length]
        last_space = chunk.rfind(" ")
        if(last_space!=-1):
            chunk = chunk[:last_space]
        chunks.append(chunk)
        start_pos += chunk_length - chunk_overlap
    return chunks
    

def generate_embedding(chunk:str)->list:
    embeddings = model.encode(chunk)
    return embeddings.tolist()


def retrieve_chunks(query:str,document_id:int,top_k:int =5):
    query_vector = model.encode(query).tolist()
    cur.execute("SELECT content FROM document_chunks WHERE document_id=%s " \
    "ORDER BY embedding <=> %s::vector LIMIT %s ;",(document_id,query_vector,top_k))
    retrieved_chunks = cur.fetchall()
    return retrieved_chunks


def get_answer(query:str,chunks:list):
    context = "\n\n".join(chunk[0] for chunk in chunks)
    system_prompt="You are a helpful assistant that answers questions based on the provided document context."
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role":"system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": f"context:\n{context}\n\nQuestion:\n{query}",
        }
    ],
    model="llama-3.1-8b-instant",
    )
    return chat_completion.choices[0].message.content
