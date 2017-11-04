import os
import httplib2
from oauth2client import client
from oauth2client.file import Storage
from oauth2client import tools


class GoogleAuthorize(object):
    CLIENT_SECRETS_FILE_LOCATION = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'client_secret.json')
    CREDENTIAL_STORE_LOCATION = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'store.json')
    SCOPES = 'https://www.googleapis.com/auth/drive'
    APPLICATION_NAME = ''

    def __init__(self, args):
        self.args = args

    def get_credentials(self):
        store = Storage(GoogleAuthorize.CREDENTIAL_STORE_LOCATION)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(GoogleAuthorize.CLIENT_SECRETS_FILE_LOCATION, GoogleAuthorize.SCOPES)
            flow.user_agent = GoogleAuthorize.APPLICATION_NAME
            credentials = tools.run_flow(flow, store, self.args)
        return credentials

    def authorize(self):
        credentials = self.get_credentials()
        return credentials.authorize(httplib2.Http())

