import pandas as pd
import numpy as np
import json
from io import BytesIO
import traceback

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
        print("in insert_file_metadata try")
    except Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to insert data: {e}")
    finally:
        cursor.close()
        connection.close()
   
   # Function to fetch file metadata from the database

def insert_analysisFile(analysis_file,analysis_json,ID):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        query = """
       UPDATE file_details SET analysis_file = %s,  analysis = %s WHERE fileID = %s;
        """
        
        cursor.execute(query, (analysis_file,analysis_json,ID))
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
        traceback.print_exc()

        print("Error:", e)
        raise

def combine_analysis(missing_values,duplicate_values):
    
    comnined_dict = {
        "missing_values": missing_values,
        "duplicate_values": duplicate_values
    }
   

    return comnined_dict 

def save_json(result, file_name):
    try:
        # Ensure the result is passed correctly to convert_to_serializable
        serialized_result = convert_to_serializable(result)
        print("Serialized Result:", type(serialized_result))
        # Save the serializable dictionary to a JSON file
        with open(file_name + '.json', 'w') as json_file:
            json.dump(serialized_result, json_file, indent=4)
    except Exception as e:
        print("Error:", e)
        traceback.print_exc()

        raise



def duplicate_checker(df,name):
    
    dc = DuplicateChecker(df=df)
    results = dc.evaluate()

    return results
    
def missing_checker(df,name):
    mp = MissingsProfiler(df=df, random_state=42)
    results = mp.evaluate()
    r = list(results.items())
    r.insert(0, ('null_count', mp.null_count().to_dict())) 
   
    return dict(r)
   
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
       
        print(file_metadata)
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
        
        duplicate_values = duplicate_checker(df,file_path["fileName"])
        missing_values = missing_checker(df,file_path["fileName"])
        
        combine_analysis_json = combine_analysis (missing_values,duplicate_values)
        file_name = dir_path+'analysis_files/analyysis_'+file_path["fileName"][:-4]
        save_json(combine_analysis_json,file_name)
        analysis_json_str = json.dumps(convert_to_serializable(combine_analysis_json))
        
        insert_analysisFile ( file_name, analysis_json_str, file_id )
        
        return file_path, file_name
    except Exception as e:
        print(e)
        traceback.print_exc()

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

