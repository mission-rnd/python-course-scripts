from command.gdrive.initialize import Initialize
from command.gdrive.share import Share
from command.gdrive.unshare import UnShare
from command.gdrive.delete import Delete


class GDriveCommand(object):
    def __init__(self, parser, args):
        self.parser = parser
        self.args = args

    def parse_args(self):
        try:
            func_to_execute = {
                'initialize': self._execute_initialize_command,
                'share': self._execute_share_command,
                'unshare': self._execute_unshare_command,
                'delete': self._execute_delete_command,
            }[self.args.gdrive]

            func_to_execute()
        except Exception as e:
            self.parser.error(e)

    def _execute_initialize_command(self):
        Initialize(self.args).execute()

    def _execute_share_command(self):
        Share(self.args).execute()

    def _execute_unshare_command(self):
        UnShare(self.args).execute()

    def _execute_delete_command(self):
        Delete(self.args).execute()