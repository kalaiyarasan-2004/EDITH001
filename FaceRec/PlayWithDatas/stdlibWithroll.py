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
    roll_no_column = None
    for column in actual_columns:
        if column.strip().lower() == 'student_name':
            student_name_column = column
        elif column.strip().lower() == 'roll no':
            roll_no_column = column

    if student_name_column is None or roll_no_column is None:
        print("Error: 'student_name' or 'roll no' column not found in the Excel file.")
        return None

    # Get a list of student names from the DataFrame
    student_names = df[student_name_column].tolist()
    roll_numbers = df[roll_no_column].tolist()

    # Find all matches for the input name with a score of 75 or higher using fuzzy matching
    matches = process.extract(student_name, student_names, limit=None)
    good_matches = [match for match in matches if match[1] >= 75]
    
    if not good_matches:
        print("No close matches found.")
        return None
    
    print("\nMatches found:")
    for i, match in enumerate(good_matches):
        student_index = student_names.index(match[0])
        roll_number = roll_numbers[student_index]
        print(f"{i+1}. Name: {match[0]}, Roll No: {roll_number}, Score: {match[1]}")

    return good_matches, student_name_column

# Main function
def main(student_name):
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
        #student_name = input("Enter the student's name (or 'exit' to quit): ")

        if student_name.lower() == 'exit':
            break

        # Search for the student
        good_matches, student_name_column = search_student(df, student_name)

        if good_matches:
            while True:
                try:
                    match_number = int(input("Enter the number corresponding to the correct student (or 0 to cancel): "))
                    if match_number == 0:
                        return 0
                    if 1 <= match_number <= len(good_matches):
                        selected_match = good_matches[match_number - 1][0]
                        result = df[df[student_name_column] == selected_match]
                        print("\nStudent Information:")
                        if 'student_name' in result.columns and 'Roll No' in result.columns and 'Student Mobile' in result.columns:
                            print(result[['student_name', 'Roll No', 'Student Mobile']].to_string(index=False))
                            print("1.Department\n2.DOB\n3.Language\n4.BloodGrp\n5.District\n6.Temp Address\n7.Perment Address\n8.Parent Detials")
                            while(True):
                                get_data=int(input("\nEnter the number"))
                                if get_data==0:
                                    return
                                elif get_data == 1:
                                    if 'Course' in result.columns:
                                        print(result[['Course']].to_string(index=False))
                                elif get_data == 2:
                                    if 'DOB' in result.columns:
                                        print(result[['DOB']].to_string(index=False))
                                elif get_data == 3:
                                    if 'Mother Tongue' in result.columns:
                                        print(result[['Mother Tongue']].to_string(index=False))
                                elif get_data == 4:
                                    if 'Blood Group' in result.columns:
                                        print(result[['Blood Group']].to_string(index=False))
                                elif get_data == 5:
                                    if 'Perm. District' in result.columns and 'Temp. District' in result.columns:
                                        print(result[['Perm. District','Temp. District']].to_string(index=False))
                                elif get_data == 7:
                                    if 'Permanent Address' in result.columns:
                                        print(result[['Permanent Address']].to_string(index=False))
                                elif get_data == 6:
                                    if 'Temporary Address' in result.columns:
                                        print(result[['Temporary Address']].to_string(index=False))
                                elif get_data == 8:
                                    if 'Fathers Name' in result.columns and 'Mothers Name' in result.columns and 'Fathers mobile' in result.columns and 'Mothers mobile no' in result.columns:
                                        print(result[['Fathers Name','Mothers Name','Fathers mobile','Mothers mobile no']].to_string(index=False))
                                
                        else:
                            print("Error: One or more required columns not found in the Excel file.")
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(good_matches)}.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        else:
            print("Student not found.")

if __name__ == "__main__":
    main()
