'''
File for common utility functions
'''

configPath = 'ds.config'
import configparser
import os

def getConfig():
    config = configparser.ConfigParser()
    config.read(configPath)
    prop = config._sections['DATA SHARE']
    return prop

def checkCreateDir(dirPath):
    if not os.path.exists(dirPath):
        os.mkdir(dirPath)
