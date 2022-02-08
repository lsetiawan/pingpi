from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import RedirectResponse
import pandas as pd
from .validator import header_check, dtype_check
from .store import setup_storage, clean_storage, save_data, read_data_file

app = FastAPI(
    title="pingpi",
    description="The mini upload and read API for ping csv data.",
)


@app.on_event("startup")
async def startup_event():
    """Start up to setup file storage"""
    setup_storage()


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown to clean up file storage"""
    clean_storage()


@app.get("/")
def home():
    """Home endpoint that redirects to docs"""
    return RedirectResponse("/docs")


@app.post("/upload/")
async def upload_file(file: UploadFile):
    """Uploads file to the server for ingestion."""
    content_type = getattr(file, "content_type", None)
    uploaded_file = getattr(file, "file", None)
    if content_type is None:
        raise HTTPException(status_code=422, detail="File is unreadable.")
    elif content_type != "text/csv":
        raise HTTPException(
            status_code=422, detail=f"{content_type} is not a valid format."
        )

    try:
        df = pd.read_csv(uploaded_file)

        # Cleans the headers of extra spaces
        df.columns = [d.strip().lower() for d in df.columns]

        # Check columns
        missing_cols = header_check(df)
        if len(missing_cols) > 0:
            raise HTTPException(
                status_code=422,
                detail=f"{','.join(missing_cols)} are missing from file!",
            )

        # Check data types
        incorrect_dtypes = dtype_check(df)
        if len(incorrect_dtypes) > 0:
            raise HTTPException(
                status_code=422,
                detail=f"{','.join(incorrect_dtypes)} have invalid data types!",
            )

        # Convert timestamps
        df.loc[:, 'timestamp'] = df['timestamp'].apply(
            pd.to_datetime, utc=True, unit='s'
        )

        file_id = save_data(df)

        return {
            "status": "success",
            "original_filename": file.filename,
            "id": file_id,
            "message": "Please use the id to access the data again."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/data/{id}")
async def get_data(id: str):
    """Read file data that has been uploaded."""
    try:
        data_dict = read_data_file(id)
        if data_dict is None:
            raise HTTPException(
                status_code=404,
                detail=f"Data with id {id} not found in the system.",
            )
        return data_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
