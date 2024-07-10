from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import pandas as pd
import json
from bson.objectid import ObjectId
from typing import List
from config.database import collection
from services.file_service import save_file, insert_file_metadata, insert_analysis_file
from services.analysis_service import  analysis_report
from fastapi.exceptions import HTTPException

router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.post("/upload-csv/")
async def upload_csv(file: UploadFile):
    
    df, file_metadata = save_file(file)
    insert_file_metadata(file_metadata)
    # print(df)
    
    data = df.to_dict(orient='list')

    # Convert any NaN or Infinity values to None
    for key, value in data.items():
        data[key] = [None if pd.isna(x) or pd.isnull(x) or x == float('inf') else x for x in value]

    return file_metadata["filename"], data


@router.post("/files/{file_id}/analysis")
async def analyze_by_id(file_id: str):
    file_data = collection.find_one({"_id": ObjectId(file_id)})
    if not file_data:
        raise HTTPException(status_code=404, detail="File not found")

    df = pd.read_csv(file_data["file_path"])
    
    analysis_data , kpi = analysis_report(df)
    
    analysis_data = json.dumps(analysis_data)
    kpi = json.dumps(kpi)
    
    insert_analysis_file(ObjectId(file_id), analysis_data,kpi)
    
    # Merge the two dictionaries
    combined_response = {
        "analysis_data": analysis_data,
        "kpi": kpi
    }
    # Convert the combined dictionary to JSON response
    return JSONResponse(content=combined_response)



@router.get("/files/{file_id}")
async def get_file(file_id: str):
    try:
        file_data = collection.find_one({"_id": ObjectId(file_id)}, {})
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid file ID")

    if not file_data:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Convert ObjectId to string
    file_data["_id"] = str(file_data["_id"])
    
    return file_data

@router.get("/files/{file_id}/analysis")
async def get_analysis(file_id: str):
    file_data = collection.find_one({"_id": ObjectId(file_id)})
    if not file_data or "analysis" not in file_data:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return JSONResponse(content=json.loads(file_data["analysis"]))

@router.get("/files/{file_id}/kpi")
async def get_analysis(file_id: str):
    file_data = collection.find_one({"_id": ObjectId(file_id)})
    if not file_data or "KPI" not in file_data:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return JSONResponse(content=json.loads(file_data["KPI"]))

@router.get("/files/")
async def get_all_files():
    files_data = list(collection.find({}, {}))
    if not files_data:
        raise HTTPException(status_code=404, detail="No files found")
    
    # Convert ObjectId to string
    for file_data in files_data:
        file_data["_id"] = str(file_data["_id"])
    
    return files_data

@router.get("/files_metadata")
async def get_all_files():
    files_data = list(collection.find({}, {
        "_id": 1,
        "filename": 1,
        "file_size": 1,
        "file_path": 1,
        "file_mime_type": 1
    }).limit(5))
    
    if not files_data:
        raise HTTPException(status_code=404, detail="No files found")
    
    # Convert ObjectId to string for each document
    formatted_files_data = []
    for file_data in files_data:
        formatted_file_data = {
            "_id": str(file_data["_id"]),
            "filename": file_data["filename"],
            "file_size": file_data["file_size"],
            "file_path": file_data["file_path"],
            "file_mime_type": file_data["file_mime_type"]
        }
        formatted_files_data.append(formatted_file_data)
    
    return formatted_files_data
