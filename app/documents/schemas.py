from pydantic import BaseModel
from datetime import datetime

class DocumentResponse(BaseModel):
    id: int
    uploaded_at: datetime
    filename: str

