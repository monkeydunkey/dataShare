"""The commit command."""


from json import dumps

from .base import Base
import configparser
import os
from utilities import getConfig, checkCreateDir
from datetime import datetime
import time
from shutil import copyfile

class add(Base):
    """Stage the files so that they are ready for commit"""
    def __init__(self, options, *args, **kwargs):
        super(add, self).__init__(options, *args, **kwargs)
        self.configPath = 'ds.config'
        self.stageFile = 'STAGE'
        self.localCommitLog = 'LOCAL'
        self.dataDir = 'cache'
        self.messageDelimeter = ' :: '

    def init_check(self):
        return True if os.path.exists(self.configPath) else False

    def getFilesToCommit(self, config):
        files = []
        with open(os.path.join(config['cachedir'], self.stageFile), 'r') as stage:
            files = stage.readlines()
        return files

    def commitHashValue(self, config):
        if config['modification identification method'].lower() == 'time':
            return time.mktime(datetime.now().timetuple())
        else:
            raise 'Modification method not implemented'

    def moveFileToCache(self, config, filename, hashValue):
        cacheDataPath = os.path.join(config['cachedir'], self.dataDir)
        checkCreateDir(cacheDataPath)
        commitFileFolderPath = os.path.join(cacheDataPath, filename)
        checkCreateDir(commitFileFolderPath)
        fileExt = filename.split('.')[-1]
        copyfile(filename, os.path.join(commitFileFolderPath, str(hashValue) + '.' + fileExt))

    def validateToCommitFiles(self, config, files):
        prevHashValue = 0
        localCommitFilePath = os.path.join(config['cachedir'], self.localCommitLog)
        if os.path.isfile(localCommitFilePath):
            f = open(localCommitFilePath, 'r')
            commits = f.readlines()
            f.close
            if commits:
                prevHashValue, message = commits[-1].split(self.messageDelimeter)
        return filter(lambda x: True if os.path.getmtime(x) > prevHashValue else False, files)

    def addCommitToLocal(self, config, hashValue, message):
        with open(os.path.join(config['cachedir'], self.localCommitLog), 'a') as commitFile:
            commitFile.write(str(hashValue) + self.messageDelimeter + message)

    def cleanup(self, config):
        open(os.path.join(config['cachedir'], self.stageFile), 'w').close()

    def run(self):
        if not self.init_check():
            raise 'Data Share Directory not initialized. Use dataShare Init to initialize a directory'
        config = getConfig()
        message = self.options['<message>']
        print 'Commit Message', message
        try:
            files = self.getFilesToCommit(config)
            hashValue = self.commitHashValue(config)
            validFiles = self.validateToCommitFiles(config, files)
            if not validFiles:
                raise 'There is nothing new to commit'
            else:
                for f in validFiles:
                    self.moveFileToCache(config, f, hashValue)
                self.addCommitToLocal(config, hashValue, message)
                self.cleanup(config)
        except Exception as e:
            print e.message
            raise
