__author__ = 'di_shen_sh@163.com'

class KLineData:
    def __init__(self, a_varietyid, a_dtime, a_open, a_high, a_low, a_close, a_volume):
        self._varietyid = a_varietyid
        self._dtime = a_dtime
        self._open = a_open
        self._high = a_high
        self._low = a_low
        self._close = a_close
        self._volume = a_volume

    @property
    def Close(self):
        return self._close

    @property
    def High(self):
        return self._high

    @property
    def Low(self):
        return self._low

    @property
    def Open(self):
        return self._open

    @property
    def Time(self):
        return self._dtime

    @property
    def VarietyId(self):
        return self._varietyid

    @property
    def Volume(self):
        return self._volume






