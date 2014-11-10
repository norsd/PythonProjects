__author__ = 'di_shen_sh@163.com'

import pymongo
from MiniKLine import *
from norlib.DateTime import *
from sys import *

class MiniKLineCollection:
    #MongoClient mc
    def __init__(self, a_mc, a_varietyid, a_seconds):
        self._str_varietyid = a_varietyid
        self._int_seconds = a_seconds
        self._mc = a_mc
        self._str_colname = "MiniKLine[{0},{1}seconds]".format(a_varietyid, a_seconds)
        self._col = a_mc.DataCenterCache[self._str_colname]

    def getdatas(self, a_begin=19000101, a_end=50000101, a_count=maxsize):
        ret = []
        begin = todatetime(a_begin)
        end = todatetime(a_end)
        i = 0
        for t in self._col.find({"_id": {"$gte": begin, "$lte": end}}):
            if i >= a_count:
                break
            ret.append(MiniKLineData(self._str_varietyid, addhours(t["_id"], 8), t["OpenPrice"], t["HighPrice"], t["LowPrice"], t["ClosePrice"], t["Volume"]))
            i += 1
        return ret


    @property
    def Count(self):
        return self._col.count()

    @property
    def VarietyId(self):
        return self._str_varietyid