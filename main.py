from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
import uvicorn
import os
from datetime import datetime
import logging
from generate_podcast import process_paper
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('podcast_generator.log'),
        logging.StreamHandler()
    ]
)

# Initialize FastAPI app
app = FastAPI(
    title="Research Paper to Podcast API",
    description="API for converting research papers to podcasts",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mount the podcast directory to serve files
app.mount("/podcast", StaticFiles(directory="podcast"), name="podcast")

# Update the PodcastResponse model
class PodcastResponse(BaseModel):
    podcast_file: str
    segments_dir: str
    message: str
    duration: float
    
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Research Paper Multimedia Converter</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }
                .container {
                    background-color: #f5f5f5;
                    padding: 20px;
                    border-radius: 8px;
                }
                .upload-form {
                    margin: 20px 0;
                    padding: 15px;
                    background-color: white;
                    border-radius: 4px;
                }
                .submit-btn {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }
                .submit-btn:hover {
                    background-color: #45a049;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Research Paper Multimedia Converter</h1>
                
                <div class="upload-form">
                    <h2>Generate Podcast</h2>
                    <form action="/generate-podcast/" method="post" enctype="multipart/form-data">
                        <input type="file" name="file" accept=".pdf" required>
                        <button type="submit" class="submit-btn">Generate Podcast</button>
                    </form>
                </div>

                <h2>API Documentation</h2>
                <ul>
                    <li><a href="/docs">Interactive API documentation</a></li>
                </ul>
            </div>
        </body>
    </html>
    """

@app.post("/generate-podcast/", response_model=PodcastResponse)
async def create_podcast(file: UploadFile = File(...)):
    try:
        start_time = datetime.now()
        
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are accepted")

        os.makedirs("temp", exist_ok=True)
        
        file_path = f"temp/{file.filename}"
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Process the paper and generate podcast - with await
        output_file = await process_paper(file_path)
        
        # Get the segments directory
        timestamp = os.path.basename(output_file).replace("podcast_", "").replace(".mp3", "")
        segments_dir = f"podcast/segments/podcast_{timestamp}"
        
        duration = (datetime.now() - start_time).total_seconds()

        return PodcastResponse(
            podcast_file=output_file,
            segments_dir=segments_dir,
            message="Podcast generated successfully",
            duration=duration
        )

    except Exception as e:
        # Clean up temporary files
        if os.path.exists(file_path):
            os.remove(file_path)
        logging.error(f"Error in podcast generation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up temporary files
        if os.path.exists(file_path):
            os.remove(file_path)

# Add endpoint to get the final podcast file
@app.get("/download-podcast/{filename}")
async def download_podcast(filename: str):
    file_path = os.path.join("podcast/final", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg", filename=filename)
    raise HTTPException(status_code=404, detail="Podcast file not found")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )