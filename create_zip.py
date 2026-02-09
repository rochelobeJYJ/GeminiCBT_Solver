
import zipfile
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Updated folder name
DIST_DIR = os.path.join(SCRIPT_DIR, 'dist', 'GeminiCBT_solver')
# Updated zip name without version
ZIP_FILENAME = os.path.join(SCRIPT_DIR, 'GeminiCBT_solver.zip')

def zip_folder_contents(folder_path, output_zip):
    if not os.path.exists(folder_path):
        print(f"Error: Folder {folder_path} does not exist.")
        return

    if os.path.exists(output_zip):
        os.remove(output_zip)
        print(f"Removed existing {output_zip}")

    print(f"Zipping contents of {folder_path} to {output_zip}...")
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Compute arcname relative to the root of the folder
                arcname = os.path.relpath(file_path, folder_path)
                print(f"Adding {arcname}")
                zipf.write(file_path, arcname)
    
    print("\nZip created successfully!")
    print(f"Location: {output_zip}")

if __name__ == "__main__":
    if os.path.exists(DIST_DIR):
        zip_folder_contents(DIST_DIR, ZIP_FILENAME)
    else:
        print(f"Build directory {DIST_DIR} not found. Did the build finish?")
