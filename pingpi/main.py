from fastapi import FastAPI, File, UploadFile, HTTPException
import pandas as pd

app = FastAPI()

@app.get("/")
def home():
    return "Hello world!"


@app.post("/upload/")
async def upload_file(file: UploadFile):
    """Uploads file to the server for ingestion"""
    content_type = getattr(file, "content_type", None)
    uploaded_file = getattr(file, "file", None)
    if content_type is None:
        raise HTTPException(status_code=422, detail="File is unreadable.")
    elif content_type != "text/csv":
        raise HTTPException(status_code=422, detail=f"{content_type} is not a valid format.")

    df = pd.read_csv(uploaded_file)
    return {"status": "success", "filename": file.filename}
