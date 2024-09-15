import dropbox

from dropbox_config import ACCESS_TOKEN, ACCOUNT_ID, NAMESPACE_ID, REFRESH_TOKEN, APP_KEY, APP_SECRET

def get_dropbox_team_client():
    return dropbox.DropboxTeam(oauth2_refresh_token=REFRESH_TOKEN, app_key=APP_KEY, app_secret=APP_SECRET)

def get_dropbox_admin_client():
    dbx = get_dropbox_team_client()
    dbx_admin = dbx.as_admin(ACCOUNT_ID)
    path_root = dropbox.common.PathRoot.namespace_id(NAMESPACE_ID)
    return dbx_admin.with_path_root(path_root)

def get_dropbox_at_base_path():
    dbx_team = get_dropbox_team_client()
    dbx = dbx_team.as_admin(ACCOUNT_ID)
    path_root = dropbox.common.PathRoot.namespace_id(NAMESPACE_ID)
    dbx =  dbx.with_path_root(path_root)
    return dbx

def print_namespaces():
    dbx = get_dropbox_team_client()
    namespaces = dbx.team_namespaces_list()
    for ns in namespaces.namespaces:
        print(ns.name, ns.namespace_id)

def print_members():
    dbx = get_dropbox_team_client()
    members = dbx.team_members_list()
    for member in members.members:
        print(member)

# Function to list files and folders only in the base root of the team space
def list_files_and_folders(dbx, path=''):
    items = []
    try:
        # Get the list of files and folders in the current path (base root)
        result = dbx.files_list_folder(path, recursive=False, include_media_info=True)

        # Iterate over entries in the current path
        for entry in result.entries:
            # Append the file/folder  to the items list
            items.append(entry)

        # Check if there are more items to fetch
        while result.has_more:
            print(f"Items fetched so far: {len(items)}")
            result = dbx.files_list_folder_continue(result.cursor)
            for entry in result.entries:
                items.append(entry)
    except dropbox.exceptions.AuthError:
        # TODO: save the progress so far
        print('Reauthenticating and starting over')
        dbx = get_dropbox_admin_client()
        return list_files_and_folders(dbx, path)
    except dropbox.exceptions.ApiError as e:
        print(f"API error while accessing path {path}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return items