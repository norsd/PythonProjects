__author__ = 'y'

from dateutil import tz


def UtcToLocal(arg_dtime):
    from_zone = tz.gettz('UTC')
    #to_zone = tz.gettz('CST')
    to_zone = tz.tzlocal()
    # Tell the datetime object that it's in UTC time zone
    utc = arg_dtime.replace(tzinfo=from_zone)
    # Convert time zone
    return utc.astimezone(to_zone)
