import os

def create_research_structure(idNum, entry_name):
    filename = str(idNum) + "_" + entry_name.strip()
    print(f"Creating research structure for: {filename}")
    if not entry_name.strip():
        print("Invalid name. Exiting.")
        return

    # Create the main folder
    research_root = "Research"
    pathFilename = os.path.join(research_root, filename)
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
            f.write("\label{research:"+ entry_name + "}")

    else:
        print(f"File {file_path} already exists. Skipping file creation.")

    print(f"Research folder structure for '{filename}' created successfully.")

if __name__ == "__main__":
    id = int(input("Enter the starting ID number: "))
    entry_name = input("Enter the name of the Research entry: ")
    create_research_structure(id, entry_name)
