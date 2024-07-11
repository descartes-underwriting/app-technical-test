from typing import List
from fastapi import HTTPException
from server.models import Contact, ContactResponse
from server.mongo_database import contact_collection
from bson import ObjectId
from pymongo.errors import DuplicateKeyError


#peut etre de l'injection???
# not forget mongo rajoute son objectid, à renvoyer ou pas... cast en str...
async def get_contacts(limit: int, offset: int) -> List[ContactResponse]:
    contacts = await contact_collection.find().skip(offset).limit(limit).to_list(length=limit)
    return [ContactResponse(id=str(contact["_id"]), **contact) for contact in contacts]

async def get_contact_by_details(contact_info: dict) -> ContactResponse:
    contact = await contact_collection.find_one(contact_info)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return ContactResponse(id=str(contact["_id"]), **contact)

# sans doute besoin plus tard pour afficher le détail d'un contact via id
async def get_contact_by_id(contact_id: str) -> ContactResponse:
    contact = await contact_collection.find_one({"_id": ObjectId(contact_id)})
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return ContactResponse(id=str(contact["_id"]), **contact)

async def create_contact(contact: Contact) -> ContactResponse:
    try:
        result = await contact_collection.insert_one(contact.dict())
        # size de base vs need de retourner l'objet crée pour avoir l'id for ex.
        new_contact = await contact_collection.find_one({"_id": result.inserted_id})
        return ContactResponse(id=str(new_contact["_id"]), **new_contact)
    except DuplicateKeyError:
        # choisir entre retourner ce qui existe ou throw le duplicate key
        raise HTTPException(status_code=400, detail=" A contact with this firstname and lastname already exists")
