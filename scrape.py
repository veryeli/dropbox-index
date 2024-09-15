import dropbox
import pandas as pd

from dropbox_config import NAMESPACE_ID
from dropbox_utils import get_dropbox_personal_client, list_files_and_folders

# Initialize Dropbox client with team access
dbx = get_dropbox_personal_client()

# Verify the namespace ID format
if not NAMESPACE_ID:
    raise ValueError("The NAMESPACE_ID is not defined. Please check your configuration.")

# Set the Dropbox-API-Path-Root header to the team space root
try:
    path_root = dropbox.common.PathRoot.namespace_id(NAMESPACE_ID)
except Exception as e:
    print(f"Error setting path root with namespace ID {NAMESPACE_ID}: {e}")
    exit()

# Apply the path root to the Dropbox client
dbx = dbx.with_path_root(path_root)

print("Successfully set the path root for the Dropbox client.")

# Fetch all files and folders in the team folder
files_and_folders = list_files_and_folders(dbx)

# Convert to a DataFrame
df = pd.DataFrame(files_and_folders)

# Save to Excel file
df.to_excel('dropbox_team_folder_files_and_folders.xlsx', index=False)

print("Spreadsheet saved as dropbox_team_folder_files_and_folders.xlsx")