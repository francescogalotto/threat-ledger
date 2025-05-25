from fastapi import FastAPI
from pydantic import BaseModel
import hashlib
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Threat Ledger API running"}


# Dummy database
feed_db = []

class FeedItem(BaseModel):
    title: str
    content: str

# Endpoint to receive a new feed item and store its hash
@app.post("/feed")
def add_feed(item: FeedItem):
    # Create a hash of the content
    content_hash = hashlib.sha256((item.title + item.content).encode()).hexdigest()
    feed_db.append({"title": item.title, "content": item.content, "hash": content_hash})
    return {"message": "Feed item added", "hash": content_hash}

# Endpoint to list all feed items
@app.get("/feed")
def list_feed():
    return feed_db

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)