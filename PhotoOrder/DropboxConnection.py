__author__ = 'Sarge'

import dropbox
import configparser

class DropboxConnection:

    def __init__(self, config):
        self.config = config
        self.appKey = 'cbj8qjebfdmd3k6'
        self.appSecret = 'yk8kyoss2t6ov2n'

    def authenticate(self):
        self.flow = dropbox.client.DropboxOAuth2FlowNoRedirect(self.appKey, self.appSecret)
        self.authorizeUrl = self.flow.start()
        return self.authorizeUrl

    def authorize(self, code):
        self.code = code
        self.accessToken, self.userId = self.flow.finish(self.code)
        self.config.setAccessToken(self.accessToken)
        self.config.writeConfig()
        self.client = dropbox.client.DropboxClient(self.accessToken)

    def setConnection(self, accessToken):
        self.accessToken = accessToken
        self.client = dropbox.client.DropboxClient(self.accessToken)