__author__ = 'y'

from datetime import *
from dateutil import tz

def todatetime(a_numberOr_datetime):
    a = a_numberOr_datetime
    if type(a) is int:
        t = datetime(a//10000, a%10000//100, a%100)
    elif type(a) is datetime:
        t = a
    else:
        raise "无法将对象{0}转化为一个dateimte".format(a)
    return t


def addhours(a_dtime, a_addhours):
    t = a_dtime + timedelta(0, a_addhours*60*60)
    return t


def tolocal(a_dtimeUTC):
    from_zone = tz.gettz('UTC')
    #to_zone = tz.gettz('CST')
    to_zone = tz.tzlocal()
    # Tell the datetime object that it's in UTC time zone
    utc = a_dtimeUTC.replace(tzinfo=from_zone)
    # Convert time zone
    return utc.astimezone(to_zone)

