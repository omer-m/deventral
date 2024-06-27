## Data Quality Endpoints

This project provides endpoints to upload and analyze CSV files for data quality issues using the FastAPI framework. 

The main functionalities include uploading files, checking for missing values, and detecting duplicate records.

## Folder Structure

```
app
    ├── analysis_files
    ├── upload_files
    └── main.py
```

- `analysis_files`: This folder contains the analysis results in JSON format.
- `upload_files`: This folder contains the uploaded CSV files.
- `main.py`: The main FastAPI application file containing the endpoints and logic.

## Endpoints
### Upload File
- **POST /upload_file**

    Upload a CSV file.

    **Request Parameter:**
    - `file`: UploadFile

    **Response:**
    - JSON object containing file metadata.

### Analyze File by ID
- **POST /analyse/{file_id}**

    Analyze a file for duplicates and missing values.

    **Path Parameter:**
    - `file_id` (int): ID of the file to be analyzed.

    **Response:**
    - JSON object containing file metadata and paths to the analysis results.

### Get File Data by ID
- **GET /get_files_data/{file_id}**

    Retrieve metadata for a specific file by ID.

    **Path Parameter:**
    - `file_id` (int): ID of the file.

    **Response:**
    - JSON object containing file metadata.


## Requirements

- Python 3.8+
- FastAPI
- Pandas
- NumPy
- MySQL Connector
- YData Quality Library

## Setup and Installation

1. **Clone the repository**

2. **Create a virtual environment and activate it:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```sh
   pip install -r requirements.txt
   ```


4. **Run the application:**

   ```sh
   uvicorn app.main:app --reload
   ```
