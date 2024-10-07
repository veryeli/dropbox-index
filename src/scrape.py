import dropbox
import pandas as pd

from dropbox_config import NAMESPACE_ID
from dropbox_utils import get_dropbox_user_client, list_files_and_folders
OUTPUT_PATH = 'output/dropbox_team_folder_files_and_folders.xlsx'

def scrape(namespace_id=NAMESPACE_ID, output_path=OUTPUT_PATH, dir_path=''):
    if not output_path:
        output_path = OUTPUT_PATH
    if not namespace_id:
        namespace_id = NAMESPACE_ID
    # Initialize Dropbox client with team access
    dbx = get_dropbox_user_client(namespace_id)
    # Verify the namespace ID format

    # Fetch all files and folders in the team folder
    files_and_folders = list_files_and_folders(dbx)


    # Convert to a DataFrame
    df = pd.DataFrame(files_and_folders)

    # Save to Excel file
    df.to_excel(output_path, index=False)

    print(f"Spreadsheet saved as {output_path}")