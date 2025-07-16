import os

def create_diary_structure(idNum, entry_name):
    # Create filename with ID number and entry name
    filename = str(idNum) + "_" + entry_name.strip()
    print(f"Creating diary structure for: {filename}")
    if not entry_name.strip():
        print("Invalid name. Exiting.")
        return

    # Create the main folder
    diary_root = "prototype"
    pathFilename = os.path.join(diary_root, filename)
    os.makedirs(pathFilename, exist_ok=True)

    # Create a subfolder called 'media' inside the main folder
    media_path = os.path.join(pathFilename, "media")
    os.makedirs(media_path, exist_ok=True)

    # Create a file inside the main folder with the same name
    file_path = os.path.join(pathFilename, f"{filename}.tex")
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("\section{}")
            f.write("\n")
            f.write("\label{prototype:"+ entry_name + "}")
            # f.write("\n")
            # f.write("\n")
            # f.write("\paragraph{Overview:}")
            # f.write("\n")
            # f.write("\n")
            # f.write("\paragraph{Achievements, Thoughts and Ideas:}")
            # f.write("\n")
            # f.write("\n")
            # f.write("\paragraph{What did I learn?}")
            # f.write("\n")
            # f.write("\n")
            # f.write("\paragraph{What was challenging?}")
            # f.write("\n")
            # f.write("\n")
            # f.write("\paragraph{Plans for next week:}")

    else:
        print(f"File {file_path} already exists. Skipping file creation.")

    print(f"Diary folder structure for '{filename}' created successfully.")

if __name__ == "__main__":
    # Read entries from DiaryEntries.txt
    id = int(input("Enter the starting ID number: "))
    entry_name = input("Enter the name of the prototype entry: ")
    create_diary_structure(id, entry_name)
