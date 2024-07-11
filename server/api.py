import sys, logging
from fastapi import FastAPI, HTTPException, Query
from server.models import Contact, ContactResponse
from server.database import get_contacts, get_contact_by_details, get_contact_by_id, create_contact
from server.mongo_database import clear_database

# pour mieux faire il vaut mieux créer un logger et faire de l'injection avec la metthode de logging pour un déployment sur GCP for ex. 
# sans doute comme j'ai fait pour mongo recup le niveau de log via le yaml/env...
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()

#need CORS? SECURITY 

#si dans un container ça peut être utile un health check
@app.get("/")
async def root():
    logger.info(f"API Ready")
    return {"HEALTH": "OK"}


@app.get("/contacts/", response_model=list[ContactResponse])
async def contactsList(limit: int = Query(10, gt=0), offset: int = Query(0, ge=0)):
    logger.info(f"GET contacts called with limit={limit}, offset={offset}")
    try:
        contacts = await get_contacts(limit, offset)
        # ne pas lister vu la taille pot.
        logger.info("Contacts retrieved successfully")
        return contacts
    except Exception as e:
        logger.error(f"Error retrieving contacts: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/contact/", response_model=ContactResponse)
async def contactView(first_name: str = None, last_name: str = None):
    logger.info(f"GET contact called with first_name={first_name}, last_name={last_name}")
    contact_info = {"first_name":first_name} if first_name else {}
    if last_name:
        contact_info["last_name"] = last_name
    if not contact_info:
        logger.error("Invalid request: both first_name and last_name are missing")
        raise HTTPException(status_code=400, detail="Invalid Request")
    # process request
    try:
        contacts = await get_contact_by_details(contact_info)
        logger.info(f"Contact retrieved successfully: {contacts}")
        return contacts
    except HTTPException as e:
         # je retrow l'erreur que j'ai raise dans la fonction fille
        logger.error(f"Error retrieving contact: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Error retrieving contact: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/contact/id/{contact_id}", response_model=ContactResponse)
async def contactViewbyId(id: str):
    logger.info(f"GET contact called with contact_id={id}")
    if not id:
        logger.error("Invalid request: id is missing")
        raise HTTPException(status_code=400, detail="Invalid Request")
    # process request
    try:
        contact = await get_contact_by_id(id)
        logger.info(f"Contact retrieved successfully: {contact}")
        return contact
    except HTTPException as e:
        # same retrow
        logger.error(f"Error retrieving contact: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Error retrieving contact: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/contact/", response_model=ContactResponse)
async def contactCreate(contact: Contact):
    logger.info(f"POST contact called with contact={contact}")
    try:
        new_contact = await create_contact(contact)
        logger.info(f"Contact created successfully: {new_contact}")
        return new_contact
    except HTTPException as e:
        logger.error(f"Error creating contact: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Error creating contact: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

#DELETE UPDATE?(since i dont do an upsert)


# @app.on_event("startup")
# async def startup_event():
#     logger.info("Starting up and clearing the database...")
#     await clear_database()
