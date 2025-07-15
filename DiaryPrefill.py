import os
import re

def natural_sort_key(text):
    """
    Convert a string into a list of mixed strings and integers for natural sorting.
    This will sort numbers numerically instead of lexicographically.
    """
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', text)]

def scan_diary_folders_and_update_tex():
    """
    Scans for every folder in the /Diary subfolder and appends each folder name 
    to the Diary.tex latex file in the format: "\\input{Diary/FOLDERNAME/FOLDERNAME.tex}"
    """
    
    # Define paths
    diary_folder = "/Users/Henry/Desktop/EPQReport/Diary"
    diary_tex_file = "/Users/Henry/Desktop/EPQReport/Diary/Diary.tex"
    
    # Check if diary folder exists
    if not os.path.exists(diary_folder):
        print(f"Error: Diary folder not found at {diary_folder}")
        return
    
    # Get all subdirectories in the Diary folder
    subfolders = []
    for item in os.listdir(diary_folder):
        item_path = os.path.join(diary_folder, item)
        # Only include directories, exclude files like Diary.tex and Diary.aux
        if os.path.isdir(item_path):
            subfolders.append(item)
    
    if not subfolders:
        print("No subfolders found in the Diary directory.")
        return
    
    # Read current content of Diary.tex
    try:
        with open(diary_tex_file, 'r') as file:
            current_content = file.read()
    except FileNotFoundError:
        print(f"Error: Diary.tex file not found at {diary_tex_file}")
        return
    
    # Find existing input statements to avoid duplicates
    existing_inputs = []
    for line in current_content.split('\n'):
        if line.strip().startswith('\\input{Diary/'):
            existing_inputs.append(line.strip())
    
    # Generate new input statements for folders that don't already have them
    new_inputs = []
    # Use natural sorting instead of regular sorting
    for folder in sorted(subfolders, key=natural_sort_key):
        input_statement = f"\\input{{Diary/{folder}/{folder}.tex}}"
        if input_statement not in existing_inputs:
            new_inputs.append(input_statement)
    
    # If there are new inputs to add, append them to the file
    if new_inputs:
        with open(diary_tex_file, 'a') as file:
            for input_statement in new_inputs:
                file.write(f"\n{input_statement}")
        
        print(f"Added {len(new_inputs)} new input statements to Diary.tex:")
        for input_statement in new_inputs:
            print(f"  {input_statement}")
    else:
        print("No new folders found. All existing folders already have input statements in Diary.tex.")
    
    # Display all found folders in proper numeric order
    print(f"\nFound {len(subfolders)} folder(s) in Diary directory:")
    for folder in sorted(subfolders, key=natural_sort_key):
        print(f"  {folder}")

if __name__ == "__main__":
    scan_diary_folders_and_update_tex()