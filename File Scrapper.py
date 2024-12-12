#File Scrapper
# This function takes a source directory and a destination directory, walks through all subdirectories of the source, 
# and copies all files to the destination directory, ignoring the original folder structure. 
# If files with the same name already exist in the destination, they are renamed to avoid overwriting.
import os
import shutil
import pandas as pd

def copy_files(source_paths, dest_dir, ignore_file_types):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    records = []

    # Loop through each specified source path
    for source_dir in source_paths:
        for root, _, files in os.walk(source_dir):
            for file in files:
                # Ignore specified file types
                if any(file.lower().endswith(file_type) for file_type in ignore_file_types):
                    print(f"Skipped file: {file}")
                    continue

                source_file_path = os.path.join(root, file)
                dest_file_path = os.path.join(dest_dir, file)
                
                counter = 1
                while os.path.exists(dest_file_path):
                    filename, extension = os.path.splitext(file)
                    dest_file_path = os.path.join(dest_dir, f"{filename}_{counter}{extension}")
                    counter += 1

                shutil.copy2(source_file_path, dest_file_path)

                file_size = os.path.getsize(source_file_path)
                file_type = os.path.splitext(file)[1]

                # Log file details
                records.append({
                    'File Name': file,
                    'Source Path': source_file_path,
                    'Destination Path': dest_file_path,
                    'File Type': file_type,
                    'File Size (bytes)': file_size
                })

                print(f"Copied file: {source_file_path} to {dest_file_path}")

    # Include existing files in dest_dir in the log
    for file in os.listdir(dest_dir):
        file_path = os.path.join(dest_dir, file)
        file_size = os.path.getsize(file_path)
        file_type = os.path.splitext(file)[1]
        records.append({
            'File Name': file,
            'Source Path': 'Already in destination',
            'Destination Path': file_path,
            'File Type': file_type,
            'File Size (bytes)': file_size
        })

    # Create a DataFrame to track the transfer information
    df = pd.DataFrame(records)
    
    # Save the DataFrame to an Excel file in the destination directory
    excel_path = os.path.join(dest_dir, 'file_transfer_log.xlsx')
    df.to_excel(excel_path, index=False)

    try:
        os.startfile(dest_dir)
    except Exception as e:
        print(f"Error opening directory: {e}")
    
    print("CODE COMPLETED")

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    records = []

    # Loop through each specified source path
    for source_dir in source_paths:
        for root, _, files in os.walk(source_dir):
            for file in files:
                source_file_path = os.path.join(root, file)
                dest_file_path = os.path.join(dest_dir, file)
                
                counter = 1
                while os.path.exists(dest_file_path):
                    filename, extension = os.path.splitext(file)
                    dest_file_path = os.path.join(dest_dir, f"{filename}_{counter}{extension}")
                    counter += 1

                shutil.copy2(source_file_path, dest_file_path)

                file_size = os.path.getsize(source_file_path)
                file_type = os.path.splitext(file)[1]

                # Log file details
                records.append({
                    'File Name': file,
                    'Source Path': source_file_path,
                    'Destination Path': dest_file_path,
                    'File Type': file_type,
                    'File Size (bytes)': file_size
                })

                print(f"Copied file: {source_file_path} to {dest_file_path}")

    # Include existing files in dest_dir in the log
    for file in os.listdir(dest_dir):
        file_path = os.path.join(dest_dir, file)
        file_size = os.path.getsize(file_path)
        file_type = os.path.splitext(file)[1]
        records.append({
            'File Name': file,
            'Source Path': 'Already in destination',
            'Destination Path': file_path,
            'File Type': file_type,
            'File Size (bytes)': file_size
        })

    # Create a DataFrame to track the transfer information
    df = pd.DataFrame(records)
    
    # Save the DataFrame to an Excel file in the destination directory
    excel_path = os.path.join(dest_dir, 'file_transfer_log.xlsx')
    df.to_excel(excel_path, index=False)

    try:
        os.startfile(dest_dir)
    except Exception as e:
        print(f"Error opening directory: {e}")
    print("CODE COMPLETED")

def delete_unimportant_files(log_file_path, dest_dir):
    # Load the Excel sheet into a DataFrame
    df = pd.read_excel(log_file_path)
    print(df)
    # Filter for files marked as 'N' in the 'Include' column
    df['Include'] = df['Include'].str.strip().str.upper()
    files_to_delete = df[df['Include'] == 'N']
    print(f"Number of files to delete: {len(files_to_delete)}")
    #print(df)
    print(df.iloc[17:20])
    #df.info()
    # Loop through the filtered files and delete them
    for index, row in files_to_delete.iterrows():
        file_path = row['Destination Path']

        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file: {file_path}. Reason: {e}")
        else:
            print(f"File not found: {file_path}")

    print("File deletion process completed.")

def move_important_files(log_file_path, source_dir):
    # Load the Excel sheet into a DataFrame
    df = pd.read_excel(log_file_path)
    
    # Filter for files marked as 'Y' in the 'Include' column
    df['Include'] = df['Include'].str.strip().str.upper()
    files_to_move = df[df['Include'] == 'Y']
    
    print(f"Number of files to move: {len(files_to_move)}")
    
    # Loop through the filtered files and move them to the source directory
    for index, row in files_to_move.iterrows():
        file_path = row['Source Path']  # Source path (corrected)
        file_name = row['File Name']
        new_file_path = os.path.join(dest_dir, file_name)  # New destination path

        if os.path.exists(file_path):
            shutil.copy(file_path, new_file_path)  # Copy from source to destination
            print(f"Copied file: {file_path} to {new_file_path}")
        else:
            print(f"File not found: {file_path}")

    print("File copy process completed.")


# Specify an array of source directories
source_paths = [
    r"S:\ITS\Pipeline Integrity\Cathodic Protection\Districts\Drayton Valley\2023",
    r"S:\ITS\Pipeline Integrity\Cathodic Protection\Districts\Drayton Valley\2022",
    r"S:\ITS\Pipeline Integrity\Cathodic Protection\Districts\Drayton Valley\2021",
    r"S:\ITS\Pipeline Integrity\Cathodic Protection\Districts\Drayton Valley\2020",
    r"S:\ITS\Pipeline Integrity\Cathodic Protection\Districts\Drayton Valley\2019",
    r"S:\ITS\Pipeline Integrity\Cathodic Protection\Districts\Drayton Valley\2018",
    r"S:\ITS\Pipeline Integrity\Cathodic Protection\Districts\Drayton Valley\2017",
    r"S:\ITS\Pipeline Integrity\Cathodic Protection\Districts\Drayton Valley\2016",
    r"S:\ITS\Pipeline Integrity\Cathodic Protection\Districts\Drayton Valley\2015",
    r"S:\ITS\Pipeline Integrity\Cathodic Protection\Districts\Drayton Valley\2014",
]
ignore_file_types = ['.jpg', '.png','.JPG','.msg']  # Add file types you want to ignore (case-insensitive)
log_file_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'Drayton AS Package', 'file_transfer_log2.xlsx')
dest_dir = os.path.join(os.path.expanduser('~'), 'Downloads', 'Drayton AS Package')
source_dir = r"S:\ITS\Pipeline Integrity\Cathodic Protection\Districts\Drayton Valley"
#copy_files(source_paths, dest_dir, ignore_file_types)
#delete_unimportant_files(log_file_path, dest_dir)
#move_important_files(log_file_path, source_dir)

# just lists all files in a path
def list_files_in_directory(directory_path):
    # List to store file details
    file_records = []

    # Walk through the directory and subdirectories
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)  # Get file size in bytes
            file_extension = os.path.splitext(file)[1]  # Get file extension

            # Append file details to the list
            file_records.append({
                'File Name': file,
                'File Path': file_path,
                'File Size (bytes)': file_size,
                'File Extension': file_extension
            })

    # Create a Pandas DataFrame from the file records
    df = pd.DataFrame(file_records)

    return df

directory_path = r'S:\ITS\Pipeline Integrity\Cathodic Protection'  # Replace with your directory path
file_list_df = list_files_in_directory(directory_path)

print(file_list_df)