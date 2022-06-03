import pathlib
import pandas as pd
import dropbox
from dropbox.exceptions import AuthError

DROPBOX_ACCESS_TOKEN = 'sl.BIjUEMJp3qM_zAcCS6wR8CspfTAvQ3hEzBN4fBvVR1YSYnwUfx_fd-lZpP6dkaQlNSM31Qmux7er64GiidGqg7z2cmgG5KYd3Cbh3xAY1Vow28KyoHMjH0Y8Yy-sSHSZsDaJTFc'

def dropbox_connect():
    """Create a connection to Dropbox."""

    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    except AuthError as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    return dbx

def dropbox_list_files(path):
    """Return a Pandas dataframe of files in a given Dropbox folder path in the Apps directory.
    """

    dbx = dropbox_connect()

    try:
        files = dbx.files_list_folder(path).entries
        files_list = []
        for file in files:
            if isinstance(file, dropbox.files.FileMetadata):
                metadata = {
                    'name': file.name,
                    'path_display': file.path_display,
                    'client_modified': file.client_modified,
                    'server_modified': file.server_modified
                }
                files_list.append(metadata)

        df = pd.DataFrame.from_records(files_list)
        return df.sort_values(by='server_modified', ascending=False)

    except Exception as e:
        print('Error getting list of files from Dropbox: ' + str(e))


result = dropbox_list_files('https://www.dropbox.com/sh/0kvc0xgau2mu2oo/AAC5x_sHoacxiQQ8nHjlWyVLa?dl=0')
print(result)