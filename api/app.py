# flask api implementation
# claude sonnet 4

from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Valid measure names as specified in homework
VALID_MEASURES = [
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

@app.route('/county_data', methods=['POST'])
def county_data():
    try:
        # check for the Easter egg first (supersedes other behavior)
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
            
        if data.get('coffee') == 'teapot':
            return jsonify({"error": "I'm a teapot"}), 418
        
        # validate required fields
        zip_code = data.get('zip')
        measure_name = data.get('measure_name')
        
        if not zip_code or not measure_name:
            return jsonify({"error": "Both 'zip' and 'measure_name' are required"}), 400
        
        # validate zip code format (5 digits)
        if not (isinstance(zip_code, str) and len(zip_code) == 5 and zip_code.isdigit()):
            return jsonify({"error": "ZIP code must be a 5-digit string"}), 400
        
        # validate measure_name
        if measure_name not in VALID_MEASURES:
            return jsonify({"error": f"Invalid measure_name. Must be one of: {VALID_MEASURES}"}), 400
        
        # connect to database
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # enable column access by name
        cursor = conn.cursor()
        
        # query to join zip_county and county_health_rankings tables
        # first get county info from zip, then get health data for that county
        query = """
        SELECT rank.*
        FROM zip_county zipc
        JOIN county_health_rankings rank ON zipc.county_code = rank.fipscode 
        WHERE zipc.zip = ? AND rank.measure_name = ?
        """
        
        cursor.execute(query, (zip_code, measure_name))
        results = cursor.fetchall()
        
        conn.close()
        
        #  check if any results found
        if not results:
            return jsonify({"error": "No data found for the specified ZIP code and measure"}), 404
        
        # convert results to list of dictionaries
        response_data = []
        for row in results:
            response_data.append(dict(row))
        
        return jsonify(response_data), 200
        
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "County Health Data API",
        "endpoint": "/county_data",
        "method": "POST",
        "required_fields": ["zip", "measure_name"],
        "valid_measures": VALID_MEASURES
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001) # run on port 5001 to avoid conflict with MacOS command center