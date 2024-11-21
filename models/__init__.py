from pydantic import BaseModel, Field

class Quote(BaseModel):
    author: str
    quote: str
    source: str = Field(default="unknown", description="Source of the quote")
    link: str = Field(..., description="Affiliate link or related link")
