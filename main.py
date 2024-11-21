from fastapi import FastAPI
from routers import router

app = FastAPI()

# Include the router for quotes
app.include_router(router, prefix="/quotes", tags=["Quotes"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Quotes API!"}
