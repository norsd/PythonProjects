# -*- coding: utf-8 -*-
__author__ = 'Administrator'

import datetime
import os
import pymongo
import sys

#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from norlib.XML import XML2PythonObject
from pymongo import MongoClient
from urllib.request import urlopen


def _Write(date, varietycode):
    #doc = urlopen('http://www.cffex.com.cn/fzjy/ccpm/201407/31/IF.xml')
    strDate = date.strftime('%Y%m/%d/')
    url = 'http://www.cffex.com.cn/fzjy/ccpm/' + strDate + varietycode + '.xml'
    doc = urlopen(url)
    print(url)
    content = doc.read().decode('GB2312')

    parser = XML2PythonObject.Xml2Obj()
    r = parser.Parse(content)

    datas = r["data"]
    infos = {}
    for data in datas:
        vid = data.getAttribute("Text") + ".CFE"
        cate = data.getAttribute("Value")
        info = infos[vid] = infos.get(vid, {})
        info["VarietyId"] = vid
        items = None
        if cate == "0":
            items = info["VolumeRanks"] = info.get("VolumeRanks", [])
        if cate == "1":
            items = info["LongPositionRanks"] = info.get("LongPositionRanks", [])
        if cate == "2":
            items = info["ShortPositionRanks"] = info.get("ShortPositionRanks", [])
        item = {}
        item["PartyName"] = data["shortname"].Value
        item["PartyId"] = data["partyid"].Value
        item["Volume"] = int(data["volume"].Value)
        item["VarVolume"] = int(data["varVolume"].Value)
        item["Rank"] = int(data["rank"].Value)
        item["RankCategory"] = int(cate)
        items.append(item)

    mc = MongoClient('mongodb://localhost:27017/')
    db = mc.PositionInfo
    #date = datetime.datetime(2014, 7, 31, 0, 0, 0, 0)
    for vid in infos:
        infos[vid]["_id"] = date
        #db[vid].insert([infos[vid]])
        db[vid].update({"_id": date}, infos[vid], True)

_Write(datetime.datetime.today(), "IF")
_Write(datetime.datetime.today(), "TF")





