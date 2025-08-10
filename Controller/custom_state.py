""" Customize state """
from typing import Optional, Dict, Any
from pydantic import BaseModel

class CustomStateType(BaseModel):
    file_path: Optional[str] = None
    prompt: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    result: Optional[str] = None
    next: Optional[str] = None