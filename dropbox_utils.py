import dropbox

from dropbox_config import ACCESS_TOKEN, ACCOUNT_ID, NAMESPACE_ID

def get_dropbox_team_client():
    dbx = dropbox.DropboxTeam(ACCESS_TOKEN)
    return dbx

def get_dropbox_admin_client():
    dbx = get_dropbox_team_client()
    dbx_admin = dbx.as_admin(ACCOUNT_ID)
    path_root = dropbox.common.PathRoot.namespace_id(NAMESPACE_ID)
    return dbx_admin.with_path_root(path_root)

def get_dropbox_at_base_path():
    dbx_team = dropbox.DropboxTeam(ACCESS_TOKEN)
    dbx_admin = dbx_team.as_admin(ACCOUNT_ID)
    path_root = dropbox.common.PathRoot.namespace_id(NAMESPACE_ID)
    dbx_admin =  dbx_admin.with_path_root(path_root)

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
def list_files_and_folders(dbx_admin, path=''):
    items = []
    try:
        # Get the list of files and folders in the current path (base root)
        result = dbx_admin.files_list_folder('', recursive=True)

        # Iterate over entries in the current path
        for entry in result.entries:
            # Append the file/folder details to the items list
            items.append({
                'name': entry.name,
                'path_display': entry.path_display,
                'is_folder': isinstance(entry, dropbox.files.FolderMetadata),
                'size': getattr(entry, 'size', None),
                'client_modified': getattr(entry, 'client_modified', None),
                'server_modified': getattr(entry, 'server_modified', None)
            })

        # Check if there are more items to fetch
        while result.has_more:
            print(f"Items fetched so far: {len(items)}")
            result = dbx_admin.files_list_folder_continue(result.cursor)
            for entry in result.entries:
                items.append({
                    'name': entry.name,
                    'path_display': entry.path_display,
                    'is_folder': isinstance(entry, dropbox.files.FolderMetadata),
                    'size': getattr(entry, 'size', None),
                    'client_modified': getattr(entry, 'client_modified', None),
                    'server_modified': getattr(entry, 'server_modified', None)
                })

    except dropbox.exceptions.ApiError as e:
        print(f"API error while accessing path {path}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return items