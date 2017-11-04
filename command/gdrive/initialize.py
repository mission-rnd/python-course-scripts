from gdrivesdk.gdriveclient import GDriveClient


class Initialize(object):
    PYTHON_COURSE_FOLDER_NAME = 'python_course'

    def __init__(self, args):
        self._validate_arguments(args)
        self.year = args.year
        self.folder = args.folder
        self.gdrive_client = GDriveClient(args)

    def _validate_arguments(self, args):
        if args.year is None:
            raise Exception('Year not passed')
        if args.folder is None:
            raise Exception('Folder name is not passed')

    def execute(self):
        python_course_folder_id = self._create_python_course_folder()
        year_folder_id = self._create_year_folder_in_python_course_folder(python_course_folder_id)
        new_folder_id = self._create_new_folder_in_year_folder(year_folder_id)
        return new_folder_id

    def _create_python_course_folder(self):
        python_course_folder_id = self._get_folder_id_in_parent_folder(Initialize.PYTHON_COURSE_FOLDER_NAME, 'root')
        if python_course_folder_id is None:
            python_course_folder_id = self.gdrive_client.create_folder(Initialize.PYTHON_COURSE_FOLDER_NAME)
        return python_course_folder_id

    def _create_year_folder_in_python_course_folder(self, python_course_folder_id):
        year_folder_id = self._get_folder_id_in_parent_folder(self.year, python_course_folder_id)
        if year_folder_id is None:
            year_folder_id = self.gdrive_client.create_folder(self.year, python_course_folder_id)
        return year_folder_id

    def _create_new_folder_in_year_folder(self, year_folder_id):
        new_folder_id = self._get_folder_id_in_parent_folder(self.folder, year_folder_id)
        if new_folder_id is None:
            new_folder_id = self.gdrive_client.create_folder(self.folder, year_folder_id)
        return new_folder_id

    def _get_folder_id_in_parent_folder(self, folder_name, parent_folder_id):
        search_query = "name = '{0}' and '{1}' in parents".format(folder_name, parent_folder_id)
        folder_info = self.gdrive_client.search_and_return_folder_info(search_query)
        if len(folder_info) == 1:
            print('Found folder {0} which is either created or exists in trash'.format(folder_name))
            return folder_info[folder_name]
        elif len(folder_info) == 0:
            return None
        raise Exception("More than one {0} folders are found".format(folder_name))
