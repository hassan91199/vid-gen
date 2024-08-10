from fastapi import FastAPI
import uvicorn

# Initialize FastAPI app
app = FastAPI()

# Include API routes
from app.api import routes
app.include_router(routes.router)

# Function to run FastAPI
def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=31415)

# Run FastAPI
if __name__ == "__main__":
    run_fastapi()
