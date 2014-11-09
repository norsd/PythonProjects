__author__ = 'di_shen_sh@163.com'

import pymongo
import KLines

class DataCenter:
    #'mongodb://localhost:27017/'
    def __init__(self, a_connection='mongodb://localhost:27017/'):
        self._str_connect = a_connection
        self._mc = pymongo.MongoClient(a_connection)
        self._str_db = 'DataCenterCache'

    def __getattr__(self, item):
        if item not in self.__dict__ and type(item) is str:
            return KLinesCollection("{0}.CFE".format(item), self._mc)
        return self.__dict__[item]

class KLinesCollection:
     #MongoClient mc
     def __init__(self, a_varietyid, a_mc):
         self._str_varietyid = a_varietyid
         self._mc = a_mc
     def __getitem__(self, a_seconds):
        print(a_seconds)
        return KLines.KLines(self._mc, self._str_varietyid, a_seconds)



