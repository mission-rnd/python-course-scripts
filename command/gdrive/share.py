import csv
from gdrivesdk.gdriveclient import GDriveClient


class Share(object):
    PYTHON_COURSE_FOLDER_NAME = 'python_course'

    def __init__(self, args):
        self._validate_arguments(args)
        self.year = args.year
        self.type = args.type
        self.data = args.data
        self.file = args.file
        self.gdrive_client = GDriveClient(args)

    def _validate_arguments(self, args):
        if args.year is None:
            raise Exception('Year not passed')
        if args.file is None and args.data is None:
            raise Exception('Data or file is not passed to create shared folders')
        if args.type is None:
            raise Exception('Type of folder not passed')

    def execute(self):
        type_id = self._check_expected_folders_are_created_and_return_type_id()
        folder_info = self.gdrive_client.search_and_return_folder_info("'{0}' in parents".format(type_id))
        entries = self._get_entries()

        for entry in entries:
            share_folder_name = entry['uniqueId']
            email_id_to_share = entry['emailId']
            if share_folder_name in folder_info:
                print("Share folder '{0}' is already created or exists in trash".format(share_folder_name))
                share_folder_id = folder_info[share_folder_name]
            else:
                print("Share folder '{0}' is not found. Creating one".format(share_folder_name))
                share_folder_id = self.gdrive_client.create_folder(share_folder_name, type_id)

            permissions = {'type': 'user','role': 'writer', 'emailAddress': email_id_to_share}
            self.gdrive_client.share_folder(share_folder_id, permissions)
            print("Shared folder '{0}' with email {1} with writer permissions".
                  format(share_folder_name, email_id_to_share))

    def _check_expected_folders_are_created_and_return_type_id(self):
        python_course_folder_id = self._check_folder_is_created_and_return_id(Share.PYTHON_COURSE_FOLDER_NAME, 'root')
        year_folder_id = self._check_folder_is_created_and_return_id(self.year, python_course_folder_id)
        return self._check_folder_is_created_and_return_id(self.type, year_folder_id)

    def _check_folder_is_created_and_return_id(self, folder_name, parent_folder_id):
        folder_id = self._get_folder_id_in_parent_folder(folder_name, parent_folder_id)
        if folder_id is None:
            raise Exception("Folder '{0}' not found".format(folder_name))
        return folder_id

    def _get_folder_id_in_parent_folder(self, folder_name, parent_folder_id):
        search_query = "name = '{0}' and '{1}' in parents".format(folder_name, parent_folder_id)
        folder_info = self.gdrive_client.search_and_return_folder_info(search_query)
        if len(folder_info) == 1:
            print('Found folder {0} which is either created or exists in trash'.format(folder_name))
            return folder_info[folder_name]
        elif len(folder_info) == 0:
            return None
        raise Exception("More than one {0} folders are found".format(folder_name))

    def _get_entries(self):
        if self.file:
            entries = self._get_student_data_from_file()
        else:
            split_data = self.data.split(',')
            entries = [{'uniqueId': split_data[0], 'emailId': split_data[1]}]
        return entries

    def _get_student_data_from_file(self):
        with open(self.file) as csv_file:
            reader = csv.DictReader(csv_file)
            entries = []
            for row in reader:
                entries.append(row)
        return entries
