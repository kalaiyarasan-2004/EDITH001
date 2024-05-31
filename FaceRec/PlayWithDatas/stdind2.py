import pandas as pd
from fuzzywuzzy import process
import os

# Function to read multiple Excel files and combine the data into a single DataFrame
def load_data_from_multiple_files(file_paths):
    data_frames = []
    for file_path in file_paths:
        try:
            df = pd.read_excel(file_path)
            data_frames.append(df)
        except FileNotFoundError:
            print(f"The file {file_path} was not found.")
        except Exception as e:
            print(f"An error occurred while reading {file_path}: {e}")
    
    # Combine all DataFrames into a single one
    if data_frames:
        combined_df = pd.concat(data_frames, ignore_index=True)
        return combined_df
    else:
        print("No data found in the provided files.")
        return None

# Function to search for a student by a fuzzy match on their name
def search_student(df, student_name):
    # Get the actual column names in the DataFrame
    actual_columns = df.columns.tolist()

    # Identify the correct column name for 'student_name' (case insensitive)
    student_name_column = None
    for column in actual_columns:
        if column.strip().lower() == 'student_name':
            student_name_column = column
            break

    if student_name_column is None:
        print("Error: 'student_name' column not found in the Excel file.")
        return None

    # Get a list of student names from the DataFrame
    student_names = df[student_name_column].tolist()

    # Find all matches for the input name with a score of 80 or higher using fuzzy matching
    matches = process.extract(student_name, student_names, limit=None)
    good_matches = [match for match in matches if match[1] >= 75]
    
    if not good_matches:
        print("No close matches found.")
        return None
    
    print("\nMatches found:")
    for match in good_matches:
        print(f"Name: {match[0]}, Score: {match[1]}")
    
    getdata=int(input("Enter the sutdent no:"))
    if getdata == 1:
        print(f"Name: {match[0]}, Score: {match[1]}")

    # Retrieve the students' details using the good matches
    results = df[df[student_name_column].isin([match[0] for match in good_matches])]
    
    if not results.empty:
        # Return specific columns: 'student_name', 'Students Mobile number', 'Date of Birth (Date/Month/Year)'
        if 'student_name' in results.columns and 'Roll No' in results.columns and 'Student Mobile' in results.columns:
            return results[['student_name', 'Roll No', 'Student Mobile']]
        else:
            print("Error: One or more required columns not found in the Excel file.")
            return None
    else:
        return None

# Main function
def main():
    # Paths to the Excel files
    file_paths = [
                      # Add more file paths as needed
        'CIVIL-22.xlsx',
        'AI&DS-22.xlsx',
        'CSD-22.xlsx',
        'CSE-22.xlsx','CST-22.xlsx','CSE(CS)-22.xlsx','ECE-22.xlsx',
        'EEE-22.xlsx','ETE-22.xlsx','IT-22.xlsx','MECH-22.xlsx'# Include your provided file
    ]

    # Load the student data from multiple files
    df = load_data_from_multiple_files(file_paths)
    if df is None:
        return

    while True:
        # Input student name to search
        student_name = input("Enter the student's name (or 'exit' to quit): ")

        if student_name.lower() == 'exit':
            break

        # Search for the student
        result = search_student(df, student_name)

        if result is not None:
            print("\nStudent Information:")
            print(result.to_string(index=False))
        else:
            print("Student not found.")
        
if __name__ == "__main__":
    main()
