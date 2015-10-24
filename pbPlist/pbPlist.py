import os

from .pbParser import PBParser

class PBPlist(object):
    
    def __init__(self, file_path):
        self.root = None
        if self.__checkFile(file_path) == True:
            parser = PBParser(self.file_path)
            self.root = parser.read()
    
    def __checkFile(self, file_path):
        can_access_file = os.path.exists(file_path)
        if can_access_file == True:
            self.file_path = file_path
        return can_access_file