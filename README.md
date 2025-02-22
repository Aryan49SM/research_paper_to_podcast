# Research Paper to Podcast

Research Paper to Podcast is an automated pipeline that transforms a PDF research paper into a podcast. It leverages AI for text processing, script generation, and TTS (text-to-speech) for audio synthesis, then merges the audio segments into a final MP3 output.

## Technical Overview

- Implements a FastAPI backend to handle file uploads, podcast generation, and file downloads.
- Uses PyPDF2 for PDF text extraction and splits content for plan and script generation.
- Integrates with Google Generative AI (Gemini model) via LangChain prompt chains to:
  - Parse the paper and generate a structured podcast plan.
  - Generate initial and section-specific dialogues.
  - Enhance the dialogue script by refining transitions and reducing redundancy.
- Employs edge_tts for TTS conversion, generating separate audio segments for three speaker roles (host, learner, expert) using distinct neural voices.
- Uses Pydub for merging individual MP3 segments based on timestamp ordering.
- Stores temporary and final outputs in organized directories for efficient file management.
- Logs process steps and errors using Python’s logging module for troubleshooting.

## Installation

### Prerequisites

- Python 3.8 or higher
- ffmpeg installed and available in your system PATH
- A valid Gemini API key (set as `GEMINI_API_KEY`)

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Aryan49SM/research_paper_to_podcast.git
   cd research_paper_to_podcast
   ```
   
2. **Create and Activate a Virtual Environment**
  
  ```bash
    python -m venv venv
    venv\Scripts\activate    # On Windows:
    source venv/bin/activate    # On macOS/Linux:
   ```

3. **Install the Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   Create a ```.env``` file in the root directory and add:

   ```bash
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Running the Application

Start the API server:

```bash
python main.py
```

#### Endpoints

- GET /
   
     Serves an HTML page with a PDF upload form.

- POST /generate-podcast/

    Accepts a PDF file, processes it, and returns JSON with details including the podcast MP3 path and processing duration.

- GET /download-podcast/{filename}

    Downloads the final merged podcast file.

## Project Structure

- main.py

  FastAPI application with endpoints and static file serving.

- generate_podcast.py

  Orchestrates PDF processing, script generation, and audio conversion.

- templates.py

  Contains prompt templates for AI script generation.

- utils/script.py

  Handles PDF parsing, text splitting, plan generation, and script enhancement.

- utils/audio_gen.py

  Generates individual audio segments using TTS and merges them into a final MP3 file.

## Example

#### Research paper: Attention Is All You Need
##### For demonstration purposes, the generated podcast MP3 was converted to MOV format.

https://github.com/user-attachments/assets/bb851aa2-c22e-4982-8000-3743edb9c985
