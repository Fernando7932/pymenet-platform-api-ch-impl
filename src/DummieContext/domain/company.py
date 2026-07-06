from pydantic import BaseModel, Field
from uuid import uuid4

class Company(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    tax_id: str
    is_active: bool = True
