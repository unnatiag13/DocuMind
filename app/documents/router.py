from fastapi import APIRouter ,Depends, File, UploadFile,HTTPException,status
from typing import Annotated
from pathlib import Path
from ..auth.token import get_current_user
from .schemas import DocumentResponse
from app.database import cur,conn
import uuid, os 
from datetime import datetime

router = APIRouter()

@router.post("/upload")
async def upload_documents(current_logged_in_user:Annotated[str, Depends(get_current_user)],file:Annotated[UploadFile, File()]):
    # fetch id from db , generate a unqiue filename.
    cur.execute("SELECT id from users WHERE email=%s",(current_logged_in_user,))
    id = cur.fetchone()
    if id == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid User")
    else:
        id = id[0]
        original_filename = file.filename
        generated_filename = str(uuid.uuid4()) + "_" + original_filename
    # store file on disk and metadata in db
    try:
        content = await file.read()
        BASE_DIR = Path(__file__).resolve().parents[2]
        UPLOAD_DIR = BASE_DIR / "uploads"
        UPLOAD_DIR.mkdir(exist_ok=True)
        file_path = str(UPLOAD_DIR / generated_filename)
        with open(file_path,"wb") as f:
            f.write(content)
        cur.execute("INSERT INTO documents(filename,file_path,uploaded_by,original_filename) VALUES(%s,%s,%s,%s) RETURNING id",(generated_filename,file_path,id,original_filename))
        conn.commit()
        doc_id = cur.fetchone()[0]
        res = DocumentResponse(id=doc_id,uploaded_at=datetime.now(),filename=original_filename)
        return res

    except Exception as e:
        conn.rollback()
        print("Error: ",e)
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="File saving failed")
    
    finally:
        await file.close()
    