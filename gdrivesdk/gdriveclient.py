import time
from gdrivesdk.authorize import GoogleAuthorize
from apiclient import discovery


class GDriveClient:
    GDRIVE_MAXIMUM_QUOTA_FOR_SECOND = 8

    def __init__(self, args):
        self.args = args
        self.service = self.initialize_gdrive_service()
        self.currently_used_quota = 0
        self.last_request_received_time = int(time.time())

    def initialize_gdrive_service(self):
        http = GoogleAuthorize(self.args).authorize()
        return discovery.build('drive', 'v3', http=http)

    def create_folder(self, folder_name, parent_folder_id=None):
        print("Creating folder with folder name '{0}'".format(folder_name))
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
        }
        if parent_folder_id is not None:
            file_metadata['parents'] = [parent_folder_id]

        self._wait_for_request_to_be_allowed()
        file = self.service.files().create(body=file_metadata, fields='id').execute()

        folder_id = file.get('id')
        print("Folder '{0}' successfully created".format(folder_name))
        return folder_id

    def share_folder(self, folder_id, permissions):
        self._wait_for_request_to_be_allowed()
        self.service.permissions().create(fileId=folder_id, body=permissions, fields='id',
                                          sendNotificationEmail=False).execute()

    def unshare_folder(self, folder_id, email_id):
        permission_id = self._get_permissions_id_for_folder_associated_with_email_id(folder_id, email_id)
        self._delete_permission_on_folder(folder_id, permission_id)

    def _get_permissions_id_for_folder_associated_with_email_id(self, folder_id, email_id):
        self._wait_for_request_to_be_allowed()
        response = self.service.permissions().list(fileId=folder_id,
                                                   fields='permissions(id,role,emailAddress)').execute()
        for permission in response.get('permissions', []):
            if permission.get('role') != 'owner' and permission.get('emailAddress') == email_id:
                return permission.get('id')

    def _delete_permission_on_folder(self, folder_id, permission_id):
        self._wait_for_request_to_be_allowed()
        self.service.permissions().delete(fileId=folder_id, permissionId=permission_id).execute()

    def delete_folder(self, folder_id):
        self._wait_for_request_to_be_allowed()
        self.service.files().delete(fileId=folder_id).execute()

    def search_and_return_folder_info(self, search_query):
        folder_info = {}
        search_query = "mimeType = 'application/vnd.google-apps.folder' and {0}".format(search_query)
        page_token = None
        while True:
            self._wait_for_request_to_be_allowed()
            response = self.service.files().list(q=search_query, spaces='drive',
                                                 fields='nextPageToken, files(id, name)',
                                                 pageToken=page_token).execute()

            for file in response.get('files', []):
                folder_info[file.get('name')] = file.get('id')
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return folder_info

    def _wait_for_request_to_be_allowed(self):
        self.currently_used_quota += 1
        current_epoch_time = int(time.time())
        if current_epoch_time - self.last_request_received_time > 0:
            self.currently_used_quota = 1
        if self._is_quota_exceeded():
            time.sleep(1)
            self.currently_used_quota = 1

    def _is_quota_exceeded(self):
        return self.currently_used_quota >= GDriveClient.GDRIVE_MAXIMUM_QUOTA_FOR_SECOND
