"""The add command."""


from json import dumps

from .base import Base
import configparser
import os
import shutil


class Add(Base):
    """Stage the files so that they are ready for commit"""
    def __init__(self, options, *args, **kwargs):
        super(Add, self).__init__(options, *args, **kwargs)
        self.configPath = 'ds.config'
        self.stageFile = 'STAGE'


    def getConfig(self):
        config = configparser.ConfigParser()
        config.read(self.configPath)
        prop = config._sections['DATA SHARE']
        return prop

    def init_check(self):
        return True if os.path.exists(self.configPath) else False

    def add(self, config, files):
        stageFilePath = os.path.join(config['cachedir'], self.stageFile)
        with open(stageFilePath, 'a') as s:
            s.write('\n'.join(files))

    def run(self):
        if not self.init_check():
            raise 'Data Share Directory not initialized. Use dataShare Init to initialize a directory'
        config = self.getConfig()
        supportedFileFormat = map(lambda x: x.strip(), config['supported data types'].split(','))
        files = self.options['<files>']
        print('Checkig the files to ensure all the added file are of the supported format')
        toAdd  = filter(lambda x: True if x.split('.')[-1] in supportedFileFormat else False, files)
        self.add(config, toAdd)
