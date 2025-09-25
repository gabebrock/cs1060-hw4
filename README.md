---
title: Homework 4
subtitle: County Health API
author: Gabriel Brock
date: 29 September 2025
subject: CS1060
---

# CSV to SQL data processing

`csv_to_sqlite.py` is a Python script that converts a CSV file into an SQLite database.

The script takes two command-line arguments:

- The name of the SQLite database file
- The name of the CSV file

and creates a table in a SQL database TABLE based on the name of the CSV file. The TABLE is created with columns based on the headers of the CSV file. The data from the CSV file is then inserted into the TABLE.

The script also handles BOM (Byte Order Mark) characters in the CSV file. The user should use the script to convert the CSV files located in `/data`, `county_health_rankings.csv`, and `zip_county.csv`, to SQL tables in a database, `data.db`.

## SQL Converter test
`test_csv_to_sqlite.py` is a Python script that tests the `csv_to_sqlite.py` converter. It tests the converter with a sample CSV file based on the test in the homework and checks if the output is as expected.

# API 

# County Health Data API Documentation

This API provides access to county health data based on ZIP codes and health measures. The API is built with Flask and deployed on Render.

## Base URL

API is available through Render at:
```
https://cs1060-hw4-unoq.onrender.com
```

For local development:
```
http://localhost:5001
```

## Authentication

No authentication is required for this API.

## Endpoints

### GET /

Returns basic information about the API.

**Response:**
```json
{
  "message": "County Health Data API",
  "endpoint": "/county_data",
  "method": "POST",
  "required_fields": ["zip", "measure_name"],
  "valid_measures": [
    "Violent crime rate",
    "Unemployment",
    "Children in poverty",
    "Diabetic screening",
    "Mammography screening",
    "Preventable hospital stays",
    "Uninsured",
    "Sexually transmitted infections",
    "Physical inactivity",
    "Adult obesity",
    "Premature Death",
    "Daily fine particulate matter"
  ]
}
```

### POST /county_data

Retrieves county health data for a specific ZIP code and health measure.

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "zip": "02138",
  "measure_name": "Adult obesity"
}
```

**Parameters:**
- `zip` (required): 5-digit ZIP code as a string
- `measure_name` (required): Health measure name (must be one of the valid measures listed above)
- `coffee` (optional): If set to "teapot", returns HTTP 418 error (Easter egg)

**Success Response (200):**
```json
[
  {
    "confidence_interval_lower_bound": "0.22",
    "confidence_interval_upper_bound": "0.24",
    "county": "Middlesex County",
    "county_code": "17",
    "data_release_year": "2012",
    "denominator": "263078",
    "fipscode": "25017",
    "measure_id": "11",
    "measure_name": "Adult obesity",
    "numerator": "60771.02",
    "raw_value": "0.23",
    "state": "MA",
    "state_code": "25",
    "year_span": "2009"
  },
  {
    "confidence_interval_lower_bound": "0.224",
    "confidence_interval_upper_bound": "0.242",
    "county": "Middlesex County",
    "county_code": "17",
    "data_release_year": "2014",
    "denominator": "1143459.228",
    "fipscode": "25017",
    "measure_id": "11",
    "measure_name": "Adult obesity",
    "numerator": "266426",
    "raw_value": "0.233",
    "state": "MA",
    "state_code": "25",
    "year_span": "2010"
  }
]
```

## Error Responses

### 400 Bad Request
Returned when required parameters are missing or invalid.

**Missing parameters:**
```json
{
  "error": "Both 'zip' and 'measure_name' are required"
}
```

**Invalid ZIP code format:**
```json
{
  "error": "ZIP code must be a 5-digit string"
}
```

**Invalid measure name:**
```json
{
  "error": "Invalid measure_name. Must be one of: [list of valid measures]"
}
```

**Invalid JSON:**
```json
{
  "error": "Invalid JSON"
}
```

### 404 Not Found
Returned when no data is found for the specified ZIP code and measure combination, or when accessing an invalid endpoint.

```json
{
  "error": "No data found for the specified ZIP code and measure"
}
```

### 418 I'm a teapot
Returned when the Easter egg parameter is provided.

```json
{
  "error": "I'm a teapot"
}
```

### 500 Internal Server Error
Returned when there's a database or server error.

```json
{
  "error": "Database error: [error details]"
}
```

## Valid Health Measures

The API accepts the following health measures:

- Violent crime rate
- Unemployment
- Children in poverty
- Diabetic screening
- Mammography screening
- Preventable hospital stays
- Uninsured
- Sexually transmitted infections
- Physical inactivity
- Adult obesity
- Premature Death
- Daily fine particulate matter

## Example Usage

### Using cURL

**Basic request:**
```bash
curl -H "Content-Type: application/json" \
  -d '{"zip": "02138", "measure_name": "Adult obesity"}' \
  https://cs1060-hw4-unoq.onrender.com/county_data
```

**Easter egg request:**
```bash
curl -H "Content-Type: application/json" \
  -d '{"zip": "02138", "measure_name": "Adult obesity", "coffee": "teapot"}' \
  https://cs1060-hw4-unoq.onrender.com/county_data
```

## Deployment on Render

This API is configured to deploy on Render using the included `render.yaml` configuration file.

### Deployment Steps:

1. **Connect Repository:** Link your GitHub repository to Render
2. **Service Configuration:** Render will automatically detect the `render.yaml` file
3. **Environment:** Python 3.11.0
4. **Build Command:** `pip install -r requirements.txt`
5. **Start Command:** `gunicorn index:app`

### Database Setup:

Ensure your `data.db` file is included in your repository. The API expects:
- A `zip_county` table with ZIP code to county mappings
- A `county_health_rankings` table with health data
- Proper foreign key relationships between tables

### Environment Variables:

No additional environment variables are required for basic functionality.

## Database Schema

The API expects the following database structure:

### zip_county table:
- `zip`: 5-digit ZIP code
- `county_code`: County FIPS code
- Additional county information fields

### county_health_rankings table:
- `fipscode`: County FIPS code (links to zip_county.county_code)
- `measure_name`: Health measure name
- `measure_id`: Numeric measure identifier
- `county`: County name
- `state`: State abbreviation
- `state_code`: State FIPS code
- `raw_value`: Raw measurement value
- `confidence_interval_lower_bound`: Lower bound of confidence interval
- `confidence_interval_upper_bound`: Upper bound of confidence interval
- `numerator`: Numerator value
- `denominator`: Denominator value
- `data_release_year`: Year the data was released
- `year_span`: Year span of the data

## Testing Your API

### Test Cases to Run in Postman:

1. **Valid Request Test:**
   - ZIP: "02138"
   - Measure: "Adult obesity"
   - Expected: 200 response with data array

2. **Easter Egg Test:**
   - ZIP: "02138"
   - Measure: "Adult obesity"
   - Coffee: "teapot"
   - Expected: 418 response

3. **Missing Parameters Test:**
   - Only ZIP provided
   - Expected: 400 response

4. **Invalid ZIP Format Test:**
   - ZIP: "123" (not 5 digits)
   - Expected: 400 response

5. **Invalid Measure Test:**
   - Valid ZIP but invalid measure name
   - Expected: 400 response

6. **No Data Found Test:**
   - ZIP: "99999" (non-existent)
   - Expected: 404 response

### Sample Test Commands:

```bash
# Test valid request
curl -H "Content-Type: application/json" \
  -d '{"zip": "02138", "measure_name": "Adult obesity"}' \
  https://cs1060-hw4-unoq.onrender.com/county_data

# Test Easter egg
curl -H "Content-Type: application/json" \
  -d '{"zip": "02138", "measure_name": "Adult obesity", "coffee": "teapot"}' \
  https://cs1060-hw4-unoq.onrender.com/county_data

# Test missing parameters
curl -H "Content-Type: application/json" \
  -d '{"zip": "02138"}' \
  https://cs1060-hw4-unoq.onrender.com/county_data

# Test invalid ZIP
curl -H "Content-Type: application/json" \
  -d '{"zip": "123", "measure_name": "Adult obesity"}' \
  https://cs1060-hw4-unoq.onrender.com/county_data
```

## Troubleshooting

### Common Issues:

1. **Database not found:** Ensure `data.db` is in the same directory as `index.py`
2. **No data returned:** Verify ZIP code exists in your dataset
3. **Invalid measure name:** Check spelling and capitalization of measure names
4. **CORS issues:** Add CORS headers if accessing from a web browser

### Logs and Debugging:

When deployed on Render, check the service logs for detailed error messages. The API includes comprehensive error handling and logging for debugging purposes.
