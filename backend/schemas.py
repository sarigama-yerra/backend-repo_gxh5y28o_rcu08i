from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class Inquiry(BaseModel):
    name: str = Field(..., description="Sender name")
    email: EmailStr = Field(..., description="Contact email")
    service: Optional[str] = Field(None, description="Requested service")
    message: str = Field(..., description="Project details")
