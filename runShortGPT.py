from fastapi import FastAPI
import uvicorn

# Initialize FastAPI app
app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "Healthy"}

# Function to run FastAPI
def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=31415)

# Run FastAPI
if __name__ == "__main__":
    run_fastapi()