# RESTful API Documentation

## Endpoints Summary

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

---

This documentation provides a clear overview of the endpoints, their purposes, expected requests, and responses, which will help developers interact with your API effectively.

## Project Directory Structure


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


This structure outlines the organization of the project's directories and files, helping developers understand where to find specific components and functionalities.
