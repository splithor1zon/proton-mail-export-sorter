import os
import json
import shutil

def main():
    """
    Main function to sort ProtonMail export email files into folders based on labels. This script serves as an extension of the Proton Mail Export Tool.

    Steps:
    1. Input the directory of the ProtonMail export email files.
    2. Load the labels.json file from the provided directory.
    3. Print the folders directory as a table.
    4. Create a "sorted" folder in the directory and create the folder structure with the folder names in the format "Name - ID".
    5. Iterate over each .eml file, read its corresponding .json file, and copy the .eml file into the corresponding folders according to the IDs.
    6. Print statistics of copied files for each directory.
    7. Ask whether to delete empty folders.
    """
    email_directory = input("Please enter the directory of the protonmail export email files: ")
    if not os.path.isdir(email_directory):
        print("The provided directory does not exist.")
        return
    
    labels_file_path = os.path.join(email_directory, "labels.json")
    if not os.path.isfile(labels_file_path):
        print("The labels.json file does not exist in the provided directory.")
        return
    
    # Load labels.json file
    with open(labels_file_path, 'r', encoding='utf-8') as labels_file:
        labels = json.load(labels_file)
    
    # Extract folder IDs and Names
    folders = {folder['ID']: folder['Name'] for folder in labels['Payload']}
    
    # Print folders directory in a readable way
    print("Folders Directory:")
    print(f"{'Name':<40} {'ID'}")
    print("-" * 50)
    for folder_id, folder_name in folders.items():
        print(f"{folder_name:<40} {folder_id}")
    
    sorted_folder_path = os.path.join(email_directory, "sorted")
    if os.path.exists(sorted_folder_path):
        overwrite = input("The 'sorted' folder already exists. Do you want to overwrite it? (yes/no): ")
        if overwrite.lower() != 'yes':
            print("Exiting without making changes.")
            return
        shutil.rmtree(sorted_folder_path)
    
    os.makedirs(sorted_folder_path)
    
    # Create folder structure
    for folder_id, folder_name in folders.items():
        folder_path = os.path.join(sorted_folder_path, f"{folder_name} - {folder_id}")
        os.makedirs(folder_path)
    
    # Iterate over each .eml file and copy to corresponding folders
    total_files = len([f for f in os.listdir(email_directory) if f.endswith(".eml")])
    processed_files = 0
    
    for file_name in os.listdir(email_directory):
        if file_name.endswith(".eml"):
            eml_file_path = os.path.join(email_directory, file_name)
            json_file_path = eml_file_path.replace(".eml", ".metadata.json")
            
            if not os.path.isfile(json_file_path):
                print(f"Warning: The corresponding .metadata.json file for {file_name} does not exist.")
                continue
            
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                email_data = json.load(json_file)
            
            label_ids = email_data['Payload'].get('LabelIDs', [])
            for label_id in label_ids:
                if label_id in folders:
                    destination_folder = os.path.join(sorted_folder_path, f"{folders[label_id]} - {label_id}")
                    shutil.copy(eml_file_path, destination_folder)
            
            processed_files += 1
            if processed_files % 100 == 0:
                print(f"Processed {processed_files} out of {total_files}")
    
    # Print copy statistics
    print("\nCopy Statistics:")
    for folder_id, folder_name in folders.items():
        folder_path = os.path.join(sorted_folder_path, f"{folder_name} - {folder_id}")
        file_count = len(os.listdir(folder_path))
        print(f"{folder_name} - {folder_id}: {file_count} files copied")
    
    # Ask whether to delete empty folders
    delete_empty = input("\nDo you want to delete empty folders? (yes/no): ")
    if delete_empty.lower() == 'yes':
        for folder_id, folder_name in folders.items():
            folder_path = os.path.join(sorted_folder_path, f"{folder_name} - {folder_id}")
            if not os.listdir(folder_path):
                os.rmdir(folder_path)
                print(f"Deleted empty folder: {folder_name} - {folder_id}")

if __name__ == "__main__":
    main()

