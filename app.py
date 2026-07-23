from fastapi import FastAPI

from startup import initialize

# Initialize first
initialize()

from api.routes import router

app = FastAPI(
    title="Coastal Shipping Document Extractor",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Coastal Shipping Document Extractor API is running successfully."
    }