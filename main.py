from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from controller import *
app = FastAPI()

class Item(BaseModel):
    url: str

@app.post("/webscraping/")
async def WebScraping(item: Item):
    try :
        response = WebScrapingController(item.url)
        return response
    except Exception as e:
        return {
            "error": str(e),
            "stratusCode": 500
        }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)