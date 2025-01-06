# quotes.py
from fastapi import APIRouter, HTTPException, Query, Body
from bson.objectid import ObjectId
from database import quotes_collection, quote_helper
from models import Quote
import random
from typing import Optional

router = APIRouter(prefix="/quotes", tags=["Quotes"])

# List all quotes with optional filtering by author
@router.get("/", response_description="List all quotes", response_model=list)
async def list_quotes(author: Optional[str] = Query(None, description="Filter by author")):
    query = {}
    if author:
        query["author"] = {"$regex": f"^{author}$", "$options": "i"}
    
    quotes = []
    async for quote in quotes_collection.find(query):
        quotes.append(quote_helper(quote))
    
    if not quotes:
        raise HTTPException(status_code=404, detail="No quotes found")
    
    return quotes

# Endpoint to add a new quote to the database
@router.post("/", response_description="Add a new quote", response_model=dict)
async def create_quote(quote: Quote):
    # Insert the new quote into the database
    new_quote = await quotes_collection.insert_one(quote.dict())
    # Fetch the newly inserted quote
    created_quote = await quotes_collection.find_one({"_id": new_quote.inserted_id})
    return quote_helper(created_quote)

# Get a random quote
@router.get("/random", response_description="Get a random quote", response_model=dict)
async def get_random_quote(author: Optional[str] = Query(None, description="Filter by author")):
    # Build the query
    query = {}
    if author:
        query["author"] = {"$regex": f"^{author}$", "$options": "i"}
    
    # Count the total number of matching quotes
    total_quotes = await quotes_collection.count_documents(query)
    if total_quotes == 0:
        raise HTTPException(status_code=404, detail="No quotes found for the specified filter")
    
    # Pick a random offset
    random_offset = random.randint(0, total_quotes - 1)
    
    # Fetch the random quote
    random_quote = await quotes_collection.find(query).skip(random_offset).to_list(length=1)
    if random_quote:
        return quote_helper(random_quote[0])
    raise HTTPException(status_code=404, detail="No quotes found")


# Update a quote by ID
@router.put("/{id}", response_description="Update a quote", response_model=dict)
async def update_quote(id: str, quote: dict = Body(...)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    # Update the document with only the fields provided in the body
    update_result = await quotes_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": quote}
    )

    if update_result.modified_count == 1:
        # Fetch and return the updated document
        updated_quote = await quotes_collection.find_one({"_id": ObjectId(id)})
        if updated_quote:
            return quote_helper(updated_quote)

    raise HTTPException(status_code=404, detail=f"Quote with ID {id} not found")
