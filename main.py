import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


@app.get("/api/news")
def get_news():
    """Return a vintage-style newspaper edition structure."""
    today = datetime.utcnow().strftime("%A, %B %d, %Y")
    edition = {
        "masthead": {
            "title": "The Daily Chronicle",
            "founded": "Founded 1896",
            "city": "New Albion",
            "motto": "All the News Fit to Print"
        },
        "dateline": {
            "city": "New Albion",
            "date": today,
            "price": "5¢",
            "edition": "Morning Edition"
        },
        "sections": [
            {
                "name": "Front Page",
                "layout": "lead",
                "articles": [
                    {
                        "headline": "Electric Carriage Astonishes Crowds on Market Street",
                        "subhead": "Inventor Demonstrates Noiseless Motor Coach; Horses Unperturbed, Onlookers Enthralled",
                        "byline": "By Edith Marlowe, Staff Correspondent",
                        "body": [
                            "A motored carriage, propelled without horse or steam, traversed Market Street at noon today to the great wonder of assembled citizens.",
                            "The contrivance, devised by a local engineer, emitted neither smoke nor cinder and advanced with steady purpose, drawing polite applause and much craning of necks.",
                            "Merchants report brisk talk of a coming age of gentle locomotion, though some gentlemen opine that the cobblestones shall have their say in the matter."
                        ]
                    },
                    {
                        "headline": "Council Weighs Gaslight to Electric Scheme",
                        "subhead": "Savings and Safety Argued in Lengthy Session",
                        "byline": "By J. H. Pike",
                        "body": [
                            "After three hours of deliberation, the city council advanced a measure to replace select gas lamps with electric bulbs along the harbor promenade.",
                            "Advocates cite fewer mishaps and clearer light for evening promenades; critics warn of expense and untested wires overhead.",
                            "A final vote is expected Friday, with merchants and lamplighters alike attending in number."
                        ]
                    }
                ]
            },
            {
                "name": "Society",
                "layout": "two-column",
                "articles": [
                    {
                        "headline": "Spring Cotillion Brings Splendor to Whitmore Hall",
                        "subhead": "Orchestra Favored Waltzes; Refreshments Praised by All",
                        "byline": "From Our Society Editor",
                        "body": [
                            "The annual Cotillion assembled a most agreeable company under garlands of laurel and paper lanterns, the ladies attired in creams and lilacs, the gentlemen in black and white.",
                            "Conversation sparkled, and no incident marred the occasion save a gentleman's glove gone missing, later recovered behind the palm." 
                        ]
                    },
                    {
                        "headline": "Lecture on Natural Philosophy Delights Young Minds",
                        "subhead": None,
                        "byline": "",
                        "body": [
                            "Professor Delaney illustrated the properties of air with bell jars and feathers, to the lively approbation of students and their parents." 
                        ]
                    }
                ]
            },
            {
                "name": "Classifieds",
                "layout": "classifieds",
                "ads": [
                    {"title": "FOR LET", "text": "A cheerful room with southern light. 12 Rose Lane."},
                    {"title": "WANTED", "text": "Boy of good character for errand service at bookseller's."},
                    {"title": "LOST", "text": "Small silver brooch in the shape of a lark. Reward offered."}
                ]
            }
        ]
    }
    return edition


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
