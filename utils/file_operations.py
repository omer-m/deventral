import pandas as pd
from io import BytesIO
from fastapi.exceptions import HTTPException
from config.database import collection

def save_file(file):
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Unsupported file type")

    try:
        file_path = f"upload_files/{file.filename}"
        file_bytes = BytesIO(file.file.read())
        df = pd.read_csv(file_bytes)
        df.to_csv(file_path, index=False)

        file_metadata = {
            "filename": file.filename,
            "file_size": file.file.tell(),
            "file_path": file_path,
            "file_mime_type": file.content_type
        }

        return df.head(), file_metadata
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid {file.content_type} file: {str(e)}")

def insert_file_metadata(file_metadata):
    collection.insert_one(file_metadata)

def insert_analysis_file(file_id, analysis_json):
    collection.update_one({"_id": file_id}, {"$set": {"analysis": analysis_json}})
