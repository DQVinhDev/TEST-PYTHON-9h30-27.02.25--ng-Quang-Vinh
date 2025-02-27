# User Guide for CSV File Upload Application

## Introduction

This application allows users to upload a CSV file containing sales data and perform queries to retrieve information from the uploaded data.

## Installation

1. Ensure that you have Python and pip installed.
2. Install the required libraries using the following command:
   ```bash
   pip install Flask pandas
   ```

## Running the Application

To run the application, use the following command in the terminal:

```bash
python idb_upload_csv.py
```

The application will run on `http://127.0.0.1:8000`.

## Uploading a CSV File

To upload a CSV file, you can use the web interface or send a POST request to the `/upload/` endpoint with the CSV file.

### Example of a POST Request

```
POST /upload/
Content-Type: multipart/form-data

file: [CSV file]
```

## Retrieving Sales Data

After uploading the CSV file, you can retrieve the data by sending a GET request to the `/sales/` endpoint with optional query parameters for filtering:

- `start_date`: Start date (format: YYYY-MM-DD)
- `end_date`: End date (format: YYYY-MM-DD)
- `region`: Region

### Example of a GET Request

```
GET /sales/?start_date=2023-01-01&end_date=2023-12-31&region=North
```

## Response

Responses from the requests will be returned in JSON format, including information about total sales, average sales, transaction count, and matching records.

## Errors

If an error occurs during file upload or data querying, the application will return an error code and the corresponding error message.

## Unit Testing

To ensure the application functions correctly, you can run unit tests. Follow these steps:

1. Cd to the test folder `cd test`.
2. Use the following command to run the tests:
   ```bash
   pytest test_idb_upload_csv.py
   ```
3. Ensure that your test cases cover various scenarios, including successful uploads and error handling.
