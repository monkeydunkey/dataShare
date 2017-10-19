"""The init command."""


from json import dumps

from .base import Base
import configparser
import os
import shutil


class init(Base):
    """Initialize the config file and setup the required files"""


    def initializeConfig(self):
        configVals = ['cloud data storage', 'local data folder', 'shallow depth',
                      'modification identification method', 'supported data types',
                      'cachedir', 'baseurlpath']
        toSkip = [5]
        defaultVals = ['S3', 'Data', '3', 'Time', "csv, tsv", ".dataShareCache", ""]
        print('Setting up the config file')
        print('To skip press enter')
        config = configparser.ConfigParser()
        config['DATA SHARE'] = {}
        for i, c in enumerate(configVals):
            if i not in toSkip:
                inp = raw_input(c + ' ')
                if not inp:
                    inp = defaultVals[i]
                #inp = inp if c != "Supported Data Types" else map(lambda x: x.strip(), inp.split(','))
            else:
                inp = defaultVals[i]
            config['DATA SHARE'][c] = inp
        with open('ds.config', 'w') as configfile:
            config.write(configfile)
        return config

    def addToGitIgnore(self, toAdd):
        if os.path.exists('.git'):
            #the folder is a git repo
            with open('.gitignore', 'a') as git:
                git.write(toAdd)

    def initializeCache(self, cacheDir):
        if os.path.exists(cacheDir):
            #folder already exists deleting it to start new
            shutil.rmtree(cacheDir)
        os.makedirs(cacheDir)
        self.addToGitIgnore(cacheDir)

    #def initializeDataTrackingFile(self, trackingFile):


    def run(self):
        config = self.initializeConfig()
        print('Setting up the cache file')
        self.initializeCache(config._sections['DATA SHARE']['cachedir'])
