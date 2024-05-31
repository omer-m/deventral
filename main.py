import pandas as pd
import numpy as np
import json
from io import BytesIO

from fastapi import FastAPI
from fastapi import FastAPI, UploadFile, File

from fastapi.exceptions import HTTPException
import mysql.connector
from mysql.connector import Error

from ydata_quality.duplicates import DuplicateChecker
from ydata_quality.missings import MissingsProfiler

app = FastAPI()


dir_path="C:/Users/HP/Desktop/deventral internship/Data Profilling Libraries/YData/ydata-quality/app/"

# # Define supported MIME types and their corresponding pandas read functions
# mime_types = {
#     "text/csv": ("csv", pd.read_csv, {"sep": ","}),
#     "text/tab-separated-values": ("tsv", pd.read_csv, {"sep": "\t"}),
#     "application/vnd.ms-excel": ("xls", pd.read_excel, {}),
#     "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ("xlsx", pd.read_excel, {}),
#     "application/vnd.oasis.opendocument.spreadsheet": ("ods", pd.read_excel, {"engine": "odf"}),
#     "text/psv": ("psv", pd.read_csv, {"sep": "|"}),
#     "text/ssv": ("ssv", pd.read_csv, {"sep": " "}),
# }

# Database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",       # Update with your MySQL username
            password="",   # Update with your MySQL password
            database="dataquality_db"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")

# Function to insert file metadata into the database
def insert_file_metadata(file_name, file_size, file_path, file_mime_type):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        query = """
        INSERT INTO file_details (fileName, fileSize, fileLocation, fileType)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (file_name, file_size, file_path, file_mime_type))
        connection.commit()
    except Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to insert data: {e}")
    finally:
        cursor.close()
        connection.close()
   
   # Function to fetch file metadata from the database
def insert_file_names(missing_file,duplicate_file,ID):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        query = """
       UPDATE file_details SET missing_checkerfile = %s, duplicate_checkerfile = %s WHERE fileID = %s;
        """
        cursor.execute(query, (missing_file,duplicate_file,ID))
        connection.commit()
    except Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to insert data: {e}")
    finally:
        cursor.close()
        connection.close()       
        
def fetch_file(file_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM file_details WHERE fileID = %s"
        cursor.execute(query, (file_id,))
        result = cursor.fetchall()
        if result is None:
            raise HTTPException(status_code=404, detail="File not found")
        return result
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data: {e}")
    finally:
        cursor.close()
        connection.close()

def fetch_all_file():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM file_details"
        cursor.execute(query)
        result = cursor.fetchall()
        if result is None:
            raise HTTPException(status_code=404, detail="File not found")
        return result
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data: {e}")
    finally:
        cursor.close()
        connection.close()

# Function to fetch specific file metadata from the database
def fetch_file_metadata_by_id(file_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT fileLocation,fileName FROM file_details WHERE fileID = %s"
        cursor.execute(query, (file_id,))
        result = cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="File not found")
        return result
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data: {e}")
    finally:
        cursor.close()
        connection.close()


def convert_to_serializable(obj):
    if isinstance(obj, pd.DataFrame):
        return obj.to_dict(orient='records')
    elif isinstance(obj, pd.Series):
        return obj.to_dict()
    elif isinstance(obj, dict):
        return {key: convert_to_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(element) for element in obj]
    else:
        return obj

def save_json(result,file_name):
    # Convert the evaluation result to a JSON-serializable format
    serializable_evaluation = convert_to_serializable(result)
    # print(serializable_evaluation)

    # Save the serializable dictionary to a JSON file
    with open(file_name+'.json', 'w') as json_file:
        json.dump(serializable_evaluation, json_file, indent=4)


def duplicate_checker(df,name):
    
    dc = DuplicateChecker(df=df)
    results = dc.evaluate()
    print(type(results))
    save_json(results,dir_path+"analysis_files/duplicate_checker_"+name[:-4])
    return dir_path+"analysis_files/duplicate_checker_"+name[:-4]+'.json'
    
def missing_checker(df,name):
    mp = MissingsProfiler(df=df, random_state=42)
    results = mp.evaluate()
    r = list(results.items())
    r.insert(0, ('null_count', mp.null_count().to_dict())) 
    save_json(dict(r),dir_path+"analysis_files/missing_checker_"+name[:-4])
    return dir_path+"analysis_files/missing_checker_"+name[:-4]+'.json'

   
@app.get("/")
async def root():
    return {"FastAPI": "Hello World "}


@app.post("/upload_file")
def upload_file(file: UploadFile): 
    
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Unsupported file type")

    try:
        file_path = f"upload_files/{file.filename}"
       
        file_bytes = BytesIO(file.file.read())
        
        df = pd.read_csv(file_bytes)
        df.to_csv(file_path, index=False)
        
        # Prepare metadata
        file_metadata = {
            "file_name": file.filename,
            "file_size": file.file.tell(),
            "file_path": dir_path+file_path,
            "file_mime_type": file.content_type
        }

        # Insert metadata into the database
        insert_file_metadata(
            file_metadata["file_name"],
            file_metadata["file_size"],
            file_metadata["file_path"],
            file_metadata["file_mime_type"]
        )

        return file_metadata 
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid {file.content_type} file: {str(e)}")

@app.post("/analyse/{file_id}")
async def analyse_by_id(file_id: int):
    try:
        file_path = fetch_file_metadata_by_id(file_id)
        df =pd.read_csv(file_path["fileLocation"])
        
        duplicate_checkerfile = duplicate_checker(df,file_path["fileName"])
        missing_checkerfile = missing_checker(df,file_path["fileName"])
        
        insert_file_names ( missing_checkerfile, duplicate_checkerfile, file_id )
        
        return file_path, missing_checkerfile, duplicate_checkerfile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_files_data/{file_id}")
async def get_files(file_id: int):
    try:
        files_metadata = fetch_file(file_id)
        return files_metadata
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_all_files")
async def get_all_files():
    try:
        files_metadata = fetch_all_file()
        return files_metadata
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

