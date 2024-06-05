# RESTful API Documentation

## Upload a File

**Endpoint**: `/files`

**Method**: `POST`

**Description**: Uploads a CSV file to the server and stores its metadata in the database.

## Analyze a File

**Endpoint**: `/files/{file_id}/analysis`

**Method**: `POST`

**Description**: Analyzes a file for missing and duplicate values and stores the analysis results.

## Get File Metadata

**Endpoint**: `/files/{file_id}`

**Method**: `GET`

**Description**: Fetches metadata for a specific file based on the provided file ID.

## Get File Analysis

**Endpoint**: `/files/{file_id}/analysis`

**Method**: `GET`

**Description**: Fetches the analysis data for a specific file based on the provided file ID.

## Get All Files Metadata

**Endpoint**: `/files`

**Method**: `GET`

**Description**: Fetches all data from database for all files.

---

This documentation provides a clear overview of the endpoints, their purposes, expected requests, and responses, which will help developers interact with your API effectively.
