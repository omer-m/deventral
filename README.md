## Data Quality Endpoints

This project provides endpoints to upload and analyze CSV files for data quality issues using the FastAPI framework. 

The main functionalities include uploading files, checking for missing values, and detecting duplicate records.

## Folder Structure


```
app/
├── config/
│   ├── __init__.py   # An empty file marking the directory as a Python package.
│   └── database.py   # Contains configuration settings and code related to the database.
│
├── models/
│   ├── __init__.py
│   └── scheme.py     # Defines data models and schemas used in the application.
│
├── api_routes/
│   ├── __init__.py
│   └── route.py      # Contains API route definitions, specifying endpoints and operations.
│
├── utils/
│   ├── __init__.py
│   ├── analysis.py         # Houses utility functions for data analysis using ydata-quality library.
│   └── file_operations.py  # Contains utility functions for file operations like saving and inserting records in the database.
│
└── main.py            # Entry point for the application.
```


## Endpoints


### Upload a File

- **Endpoint**: `/files`
- **Method**: `POST`
- **Description**: Uploads a CSV file to the server and stores its metadata in the database.

### Analyze a File

- **Endpoint**: `/files/{file_id}/analysis`
- **Method**: `POST`
- **Description**: Analyzes a file for missing and duplicate values and stores the analysis results.

### Get File data

- **Endpoint**: `/files/{file_id}`
- **Method**: `GET`
- **Description**: Fetches metadata and Analysis for a specific file based on the provided file ID.

### Get File Analysis

- **Endpoint**: `/files/{file_id}/analysis`
- **Method**: `GET`
- **Description**: Fetches the analysis data for a specific file based on the provided file ID.

### Get All Files 

- **Endpoint**: `/files`
- **Method**: `GET`
- **Description**: Fetches all data from the database for all files.


## Requirements

- Python 3.8+
- FastAPI
- Pandas
- NumPy
- Mongodb Atlas
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

