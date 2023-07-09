import os

# Check if a folder is empty or nonexistent
# @param folder_path: The path to the folder
# @return True if the folder is empty or nonexistent, False otherwise
def is_folder_empty_or_nonexistent(folder_path):
    if not os.path.exists(folder_path):
        return True  # Folder path does not exist
    elif not os.path.isdir(folder_path):
        return False  # The path exists but is not a folder
    else:
        # Check if the folder is empty
        return len(os.listdir(folder_path)) == 0
    
# Check the path is a folder
# @param folder_path: The path to the folder
# @return True if the path is a folder, False otherwise
def is_folder(folder_path):
    if not os.path.exists(folder_path):
        return False  # Folder path does not exist
    elif not os.path.isdir(folder_path):
        return False  # The path exists but is not a folder
    else:
        return True