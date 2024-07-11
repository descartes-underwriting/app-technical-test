from pydantic import BaseModel, EmailStr, Field

#filed  2 certains pays on des noms de 2lettres
class Contact(BaseModel):
    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)
    job: str
    email_address: EmailStr
    comment: str
class ContactResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    job: str
    email_address: EmailStr
    comment: str