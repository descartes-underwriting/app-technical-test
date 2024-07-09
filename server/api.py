import sys
print(sys.path)
from fastapi import FastAPI, HTTPException
from server.models import Contact
from server.database import contact_collection
app = FastAPI()


@app.get("/")
async def root():
    return {"HEALTH": "OK"}


@app.get("/contacts/", response_model=list[Contact])
async def contactsList():
    #surement call la db et retourner la liste ...hum prevoir un filtre et sort?
    contacts = await contact_collection.find().to_list(length=100)
    return [Contact(id=str(contact["_id"]), **contact) for contact in contacts]
    # return []

@app.get("/contact/{contact_id}", response_model=Contact)
async def contactView(contact_id: str):
    if contact_id is None:
        raise HTTPException(status_code=404, detail="Invalid Id")
    # utiliser id de la db ou ajouter au model...
    contact = {"_id":"", "first_name": "Elpido", "last_name": "HOUNAKE", "job": "Dev", "email_address": "secret@something.com", "comment": "test" }
    # si mongo il faudra separer et ajouter not JSON serializable blabla
    return Contact(id=str(contact["_id"]), **contact)

@app.post("/contact/", response_model=Contact)
async def contactCreate(contact: Contact):


    result = await contact_collection.insert_one(contact.dict())
    new_contact = await contact_collection.find_one({"_id": result.inserted_id})
    return Contact(id=str(new_contact["_id"]), **new_contact)
    # demander si besoin de faire un model avec des required fields size limit etc...
    # demander que faire pour les doublons, quel/quels sont les clés uniques, et si faire un upsert ou refuser la copie
    new_contact = contact.__dict__.copy() # un shallow copy mais il faut mieux request pour get ce quon a inseré 100% sûr
    # creer un modele de réponse ou renvoyer l'objet contact ou just un Ok?
    return Contact(new_contact)