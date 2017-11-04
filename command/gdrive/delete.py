import csv
from gdrivesdk.gdriveclient import GDriveClient


class Delete(object):
    PYTHON_COURSE_FOLDER_NAME = 'python_course'

    def __init__(self, args):
        self._validate_arguments(args)
        self.year = args.year
        self.type = args.type
        self.data = args.data
        self.file = args.file
        self.all = args.all
        self.gdrive_client = GDriveClient(args)

    def _validate_arguments(self, args):
        if args.year is None:
            raise Exception('Year not passed')
        if args.type is None:
            raise Exception('Type of folder not passed')
        if not args.all:
            if args.file is None and args.data is None:
                raise Exception('Data or file is not passed to create shared folders')
        else:
            if args.file is not None or args.data is not None:
                raise Exception('Data or file option should not be provided as -a/--all is set')

    def execute(self):
        type_id = self._check_expected_folders_are_created_and_return_type_id()
        folder_info = self.gdrive_client.search_and_return_folder_info("'{0}' in parents".format(type_id))

        if self.all:
            self._delete_all_folders(folder_info)
        else:
            self._delete_folders_based_on_entries(folder_info)

    def _check_expected_folders_are_created_and_return_type_id(self):
        python_course_folder_id = self._check_folder_is_created_and_return_id(Delete.PYTHON_COURSE_FOLDER_NAME, 'root')
        year_folder_id = self._check_folder_is_created_and_return_id(self.year, python_course_folder_id)
        return self._check_folder_is_created_and_return_id(self.type, year_folder_id)

    def _check_folder_is_created_and_return_id(self, folder_name, parent_folder_id):
        folder_id = self._get_folder_id_in_parent_folder(folder_name, parent_folder_id)
        if folder_id is None:
            raise Exception("Folder '{}' not found".format(folder_name))
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

    def _delete_all_folders(self, folder_info):
        for folder_name,folder_id in folder_info.items():
            self.gdrive_client.delete_folder(folder_id)
            print("Deleted folder '{0}'".format(folder_name))

    def _delete_folders_based_on_entries(self, folder_info):
        entries = self._get_entries()

        for entry in entries:
            folder_name = entry['uniqueId']
            if folder_name in folder_info:
                folder_id = folder_info[folder_name]
                self.gdrive_client.delete_folder(folder_id)
                print("Deleted folder '{0}'".format(folder_name))
            else:
                print("Folder '{0}' not found. Skipping Delete".format(folder_name))

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