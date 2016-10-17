#!/usr/bin/python
# -*- coding: utf-8 -*-
import configparser
from pathlib import Path

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

#Python2
#class MyClass(BaseClass):
#    __metaclass__ = Singleton

#Python3
class AppProject(metaclass=Singleton):
    def __init__(self):
        #super(AppProject, self).__init__() 
        self.mFilePath = u''
        self.mDBFolder = u'db'
        self.mSimFolder = u'sim'
        pass

    def reset(self):
        self.mFilePath = u''
        self.mDBFolder = u''
        self.mSimFolder = u'sim'
        
    def save(self):
        if self.mFilePath !='' and Path( self.mFilePath ).exists():      
            config = configparser.ConfigParser()
            config['Paths'] = {'DB': self.mDBFolder,
                              'Sim': self.mSimFolder}
    
            with open(self.mFilePath, 'w') as projectfile:
                config.write(projectfile)


    def load(self):
        config = configparser.ConfigParser()
        if self.mFilePath !='' and  Path( self.mFilePath ).exists():
            config.read(self.mFilePath)
            self.mDBFolder = config['Paths']['DB']
            self.mSimFolder = config['Paths']['Sim'] 
            
    def creatFolder(self):
        profile = Path( self.mFilePath )
        if self.mFilePath !='' and  profile.exists():
            dirPath = (profile.parent / self.mDBFolder)
            if not dirPath.exists() :
                dirPath.mkdir()
            dirPath = (profile.parent / self.mSimFolder)
            if not dirPath.exists() :
                dirPath.mkdir() 
                
    def getDBPath(self,dfFileName):
        profile = Path( self.mFilePath )
        if self.mFilePath !='' and  profile.exists():
            return str( profile.parent / self.mDBFolder / dfFileName )
        else:
            return u''
        
