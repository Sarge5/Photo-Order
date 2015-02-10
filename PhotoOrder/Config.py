__author__ = 'Sarge'

import configparser


class Config:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.initEmptyValues('DATABASE_CONFIG', 'db_server')
        self.initEmptyValues('DATABASE_CONFIG', 'db_name')
        self.initEmptyValues('DATABASE_CONFIG', 'db_user')
        self.initEmptyValues('DATABASE_CONFIG', 'db_pass')
        self.initEmptyValues('DATABASE_CONFIG', 'db_port')

    def initEmptyValues(self, section, option):
        if section in self.config:
            pass
        else:
            self.config[section] = {}
        if option in self.config[section]:
            pass
        else:
            self.config[section][option] = ''

    def getAccessToken(self):
        if 'DROPBOX_CONFIG' in self.config:
            if 'access_token' in self.config['DROPBOX_CONFIG']:
                return self.config['DROPBOX_CONFIG']['access_token']
            else:
                return -1
        else:
            return -1

    def setAccessToken(self, accessToken):
        self.config['DROPBOX_CONFIG']['access_token'] = accessToken

    def getDBServer(self):
        return self.config['DATABASE_CONFIG']['db_server']

    def setDBServer(self, dbServer):
        self.config['DATABASE_CONFIG']['db_server'] = dbServer

    def getDBName(self):
        return self.config['DATABASE_CONFIG']['db_name']

    def setDBName(self, dbName):
        self.config['DATABASE_CONFIG']['db_name'] = dbName

    def getDBUser(self):
        return self.config['DATABASE_CONFIG']['db_user']

    def setDBUser(self, dbUser):
        self.config['DATABASE_CONFIG']['db_user'] = dbUser

    def getDBPass(self):
        return self.config['DATABASE_CONFIG']['db_pass']

    def setDBPass(self, dbPass):
        self.config['DATABASE_CONFIG']['db_pass'] = dbPass

    def getDBPort(self):
        return self.config['DATABASE_CONFIG']['db_port']

    def setDBPort(self, dbPort):
        self.config['DATABASE_CONFIG']['db_port'] = dbPort

    def writeConfig(self):
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)