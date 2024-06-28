from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import pandas as pd
import json
from bson.objectid import ObjectId
from typing import List
from config.database import collection
from models.scheme import CSVUploadResponse, AnalysisResult, AnalysisResponse
from utils.file_operations import save_file, insert_file_metadata, insert_analysis_file
from utils.analysis import duplicate_checker, missing_checker, combine_analysis
from fastapi.exceptions import HTTPException

router = APIRouter()

def convert_to_serializable(obj):
    try:
        if isinstance(obj, pd.DataFrame):
            return obj.to_dict(orient='records')
        elif isinstance(obj, pd.Series):
            return obj.to_dict()
        elif isinstance(obj, dict):
           
            return {convert_to_serializable(key): convert_to_serializable(value) for key, value in obj.items()}
           
        elif isinstance(obj, list):
            return [convert_to_serializable(element) for element in obj]
        else:
            # Convert non-serializable types to serializable types or handle as needed
            return str(obj)
    except Exception as e:

        print("Error:", e)
        raise

@router.post("/upload-csv/", response_model=CSVUploadResponse)
async def upload_csv(file: UploadFile = File(...)):
    
    df, file_metadata = save_file(file)
    insert_file_metadata(file_metadata)
    print(df)
    
    data = df.to_dict(orient='list')

    # Convert any NaN or Infinity values to None
    for key, value in data.items():
        data[key] = [None if pd.isna(x) or pd.isnull(x) or x == float('inf') else x for x in value]

    return CSVUploadResponse(filename=file_metadata["filename"], data=data)


@router.post("/files/{file_id}/analysis", response_model=AnalysisResponse)
async def analyze_by_id(file_id: str):
    file_data = collection.find_one({"_id": ObjectId(file_id)})
    if not file_data:
        raise HTTPException(status_code=404, detail="File not found")

    df = pd.read_csv(file_data["file_path"])
    duplicate_values = duplicate_checker(df)
    missing_values = missing_checker(df)

    analysis_result = combine_analysis(missing_values, duplicate_values)
    analysis_result = convert_to_serializable(analysis_result)
    
    analysis_json_str = json.dumps(analysis_result)
    
    insert_analysis_file(ObjectId(file_id), analysis_json_str)
    
    return JSONResponse(content=json.loads(analysis_json_str))


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

@router.get("/files/{file_id}/analysis", response_model=AnalysisResponse)
async def get_analysis(file_id: str):
    file_data = collection.find_one({"_id": ObjectId(file_id)})
    if not file_data or "analysis" not in file_data:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return JSONResponse(content=json.loads(file_data["analysis"]))

@router.get("/files/")
async def get_all_files():
    files_data = list(collection.find({}, {}))
    if not files_data:
        raise HTTPException(status_code=404, detail="No files found")
    
    # Convert ObjectId to string
    for file_data in files_data:
        file_data["_id"] = str(file_data["_id"])
    
    return files_data