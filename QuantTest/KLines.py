__author__ = 'di_shen_sh@163.com'

import pymongo

class KLines:
    #MongoClient mc
    def __init__(self, a_mc, a_varietyid, a_seconds):
        self._str_varietyid = a_varietyid
        self._int_seconds = a_seconds
        self._mc = a_mc
        self._str_colname = "KLine[{0},{1}seconds]".format(a_varietyid, a_seconds)
        self._col = a_mc.DataCenterCache[self._str_colname]

    @property
    def Count(self):
        return self._col.count()

    @property
    def VarietyId(self):
        return self._str_varietyid