import dropbox

from dropbox_config import ACCESS_TOKEN, ACCOUNT_ID, NAMESPACE_ID, REFRESH_TOKEN, APP_KEY, APP_SECRET

def get_dropbox_team_client():
    return dropbox.DropboxTeam(oauth2_refresh_token=REFRESH_TOKEN, app_key=APP_KEY, app_secret=APP_SECRET)

def get_dropbox_admin_client(namespace=NAMESPACE_ID):
    dbx = get_dropbox_team_client()
    dbx_admin = dbx.as_admin(ACCOUNT_ID)
    path_root = dropbox.common.PathRoot.namespace_id(namespace)
    return dbx_admin.with_path_root(path_root)

def get_dropbox_user_client(namespace=NAMESPACE_ID):
    dbx = get_dropbox_team_client()
    dbx_user = dbx.as_user(ACCOUNT_ID)
    # return dbx_user
    path_root = dropbox.common.PathRoot.namespace_id(namespace)
    return dbx_user.with_path_root(path_root)

def get_dropbox_at_base_path(namespace=NAMESPACE_ID):
    dbx_team = get_dropbox_team_client()
    dbx = dbx_team.as_admin(ACCOUNT_ID)
    path_root = dropbox.common.PathRoot.namespace_id(namespace)
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
        print(member.profile.email, member.profile.account_id)


# Function to get or create a shared link for a file
def get_or_create_shared_link(dbx, path):
    try:
        # Check if a shared link already exists
        shared_links = dbx.sharing_list_shared_links(path=path).links

        # If a shared link exists, return the first one
        if shared_links:
            return shared_links[0].url

        # If no link exists, create a new shared link
        shared_link = dbx.sharing_create_shared_link_with_settings(path)
        return shared_link.url

    except dropbox.exceptions.ApiError as e:
        print(f"API error while creating a link for {path}: {e}")
        return None

# Function to list files and folders only in the base root of the team space
def list_files_and_folders(dbx, path='', recursive=True, create_links=True):
    if path == '/':
        path = ''
    items = []
    try:
        print(f"Listing files and folders in path: {path}")
        # Get the list of files and folders in the current path (base root)
        result = dbx.files_list_folder(path, recursive=recursive, include_media_info=True)

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


    return items