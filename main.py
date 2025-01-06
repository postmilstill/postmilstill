from fastapi import FastAPI
from routers import router

app = FastAPI()

# Include the aggregated router (prefixes are defined in the individual routers)
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Quotes API!"}
