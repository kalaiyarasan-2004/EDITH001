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

    # Find the best match for the input name using fuzzy matching
    best_match, score = process.extractOne(student_name, student_names)
    
    if score < 60:
        print("No close match found.")
        return None
    
    print(f"Best match: {best_match} with a score of {score}")

    # Retrieve the student's details using the best match
    result = df[df[student_name_column] == best_match]

    if not result.empty:
        # Return specific columns: 'student_name', 'Students Mobile number', 'Date of Birth (Date/Month/Year)'
        if 'student_name' in result.columns and 'Roll No' in result.columns and 'Student Mobile' in result.columns:
            return result[['student_name', 'Roll No', 'Student Mobile']]
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
