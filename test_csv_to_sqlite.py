#!/usr/bin/env python3
# claude sonnet 4
"""
Test suite for csv_to_sqlite.py
Automates the homework example and validates functionality
"""

import os
import sys
import sqlite3
import subprocess
import tempfile
import csv

def run_command(cmd):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

def test_basic_functionality():
    """Test the basic functionality as shown in homework example"""
    print("Testing basic functionality (homework example)...")
    
    # Clean up any existing test database
    if os.path.exists("data.db"):
        os.remove("data.db")
    
    # Test 1: Process zip_county.csv
    print("Processing zip_county.csv...")
    returncode, stdout, stderr = run_command("python3 csv_to_sqlite.py data.db data/zip_county.csv")
    if returncode != 0:
        print(f"Failed to process zip_county.csv: {stderr}")
        return False
    print("zip_county.csv processed successfully")
    
    # Test 2: Process county_health_rankings.csv
    print("Processing county_health_rankings.csv...")
    returncode, stdout, stderr = run_command("python3 csv_to_sqlite.py data.db data/county_health_rankings.csv")
    if returncode != 0:
        print(f"Failed to process county_health_rankings.csv: {stderr}")
        return False
    print("county_health_rankings.csv processed successfully")
    
    # Test 3: Validate database contents
    print("Validating database contents...")
    try:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        
        # Check zip_county table
        cursor.execute("SELECT COUNT(*) FROM zip_county")
        zip_count = cursor.fetchone()[0]
        expected_zip_count = 54553
        if zip_count != expected_zip_count:
            print(f"zip_county row count mismatch: expected {expected_zip_count}, got {zip_count}")
            return False
        print(f"zip_county has correct row count: {zip_count}")
        
        # Check county_health_rankings table
        cursor.execute("SELECT COUNT(*) FROM county_health_rankings")
        health_count = cursor.fetchone()[0]
        expected_health_count = 303864
        if health_count != expected_health_count:
            print(f"county_health_rankings row count mismatch: expected {expected_health_count}, got {health_count}")
            return False
        print(f"county_health_rankings has correct row count: {health_count}")
        
        # Check schemas
        cursor.execute("PRAGMA table_info(zip_county)")
        zip_schema = cursor.fetchall()
        expected_zip_columns = ['zip', 'default_state', 'county', 'county_state', 'state_abbreviation', 
                               'county_code', 'zip_pop', 'zip_pop_in_county', 'n_counties', 'default_city']
        actual_zip_columns = [col[1] for col in zip_schema]
        if actual_zip_columns != expected_zip_columns:
            print(f"zip_county schema mismatch")
            print(f"    Expected: {expected_zip_columns}")
            print(f"    Actual: {actual_zip_columns}")
            return False
        print("zip_county schema is correct")
        
        cursor.execute("PRAGMA table_info(county_health_rankings)")
        health_schema = cursor.fetchall()
        expected_health_columns = ['state', 'county', 'state_code', 'county_code', 'year_span', 'measure_name', 
                                  'measure_id', 'numerator', 'denominator', 'raw_value', 
                                  'confidence_interval_lower_bound', 'confidence_interval_upper_bound', 
                                  'data_release_year', 'fipscode']
        actual_health_columns = [col[1] for col in health_schema]
        if actual_health_columns != expected_health_columns:
            print(f"county_health_rankings schema mismatch")
            print(f"    Expected: {expected_health_columns}")
            print(f"    Actual: {actual_health_columns}")
            return False
        print("county_health_rankings schema is correct")
        
        # Verify all columns are TEXT type
        for col in zip_schema:
            if col[2] != 'TEXT':
                print(f"zip_county column {col[1]} is not TEXT type: {col[2]}")
                return False
        for col in health_schema:
            if col[2] != 'TEXT':
                print(f"county_health_rankings column {col[1]} is not TEXT type: {col[2]}")
                return False
        print("All columns are TEXT type")
        
        conn.close()
        
    except Exception as e:
        print(f"Database validation failed: {e}")
        return False
    
    print("Basic functionality test PASSED!")
    return True

def test_error_handling():
    """Test error handling and validation"""
    print("Testing error handling...")
    
    # Test 1: Missing arguments
    print("Testing missing arguments...")
    returncode, stdout, stderr = run_command("python3 csv_to_sqlite.py")
    if returncode == 0:
        print("Should fail with missing arguments")
        return False
    print("Correctly handles missing arguments")
    
    # Test 2: Invalid database extension
    print("Testing invalid database extension...")
    returncode, stdout, stderr = run_command("python3 csv_to_sqlite.py test.txt data/zip_county.csv")
    if returncode == 0:
        print("Should fail with invalid database extension")
        return False
    print("Correctly validates database extension")
    
    # Test 3: Invalid CSV extension
    print("Testing invalid CSV extension...")
    returncode, stdout, stderr = run_command("python3 csv_to_sqlite.py test.db data/zip_county.txt")
    if returncode == 0:
        print("Should fail with invalid CSV extension")
        return False
    print("Correctly validates CSV extension")
    
    # Test 4: Non-existent CSV file
    print("Testing non-existent CSV file...")
    returncode, stdout, stderr = run_command("python3 csv_to_sqlite.py test.db nonexistent.csv")
    if returncode == 0:
        print("Should fail with non-existent file")
        return False
    print("Correctly handles non-existent files")
    
    print("Error handling test PASSED!")
    return True

def test_table_naming():
    """Test table naming logic"""
    print("Testing table naming logic...")
    
    # Create a temporary CSV file with special characters in name
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        writer = csv.writer(f)
        writer.writerow(['col1', 'col2'])
        writer.writerow(['data1', 'data2'])
        temp_csv = f.name
    
    try:
        # Test with the temporary file
        temp_db = "test_naming.db"
        if os.path.exists(temp_db):
            os.remove(temp_db)
        
        returncode, stdout, stderr = run_command(f"python3 csv_to_sqlite.py {temp_db} {temp_csv}")
        if returncode != 0:
            print(f"Failed to process temporary CSV: {stderr}")
            return False
        
        # Check that table was created with correct name
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        conn.close()
        
        if len(tables) != 1:
            print(f"Expected 1 table, found {len(tables)}")
            return False
        
        table_name = tables[0][0]
        expected_base = os.path.splitext(os.path.basename(temp_csv))[0].lower()
        if table_name != expected_base:
            print(f"Table name mismatch: expected {expected_base}, got {table_name}")
            return False
        
        print("Table naming logic works correctly")
        
        # Cleanup
        os.remove(temp_db)
        
    finally:
        os.remove(temp_csv)
    
    print("Table naming test PASSED!")
    return True

def display_database_info():
    """Display database information like the homework example"""
    print("\n📊 Database Information (like homework example):")
    
    if not os.path.exists("data.db"):
        print("data.db not found")
        return
    
    try:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        
        # Display zip_county info
        print("\n  📋 zip_county table:")
        cursor.execute("SELECT sql FROM sqlite_master WHERE name='zip_county'")
        schema = cursor.fetchone()[0]
        print(f"    Schema: {schema}")
        cursor.execute("SELECT COUNT(*) FROM zip_county")
        count = cursor.fetchone()[0]
        print(f"    Row count: {count}")
        
        # Display county_health_rankings info
        print("\n  📋 county_health_rankings table:")
        cursor.execute("SELECT sql FROM sqlite_master WHERE name='county_health_rankings'")
        schema = cursor.fetchone()[0]
        print(f"    Schema: {schema}")
        cursor.execute("SELECT COUNT(*) FROM county_health_rankings")
        count = cursor.fetchone()[0]
        print(f"    Row count: {count}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error reading database: {e}")

def main():
    """Run all tests"""
    print("Starting CSV to SQLite Test Suite")
    print("=" * 50)
    
    all_passed = True
    
    # Run tests
    if not test_basic_functionality():
        all_passed = False
    
    if not test_error_handling():
        all_passed = False
    
    if not test_table_naming():
        all_passed = False
    
    # Display results
    display_database_info()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("ALL TESTS PASSED! Your csv_to_sqlite.py script is working correctly!")
        print("Ready for homework submission!")
    else:
        print("Some tests failed. Please review the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
