#coding: utf-8
__author__ = 'delon_000'

import threading
import wx
import wx.grid as  gridlib

from WindPy import w
import numpy as np
import time

w.start()

class MyForm(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Grid with Popup Menu")

        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        self.grid = gridlib.Grid(panel)
        self.grid.CreateGrid(1,2)
        grid = self.grid
        grid.SetColLabelValue(0, "USDCAD")
        grid.SetColLabelValue(1, "EURUSD")
        #设置Column
        self.dtColumnIndex = {"USDCAD.FX":0,"EURUSD.FX":1}

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND, 5)
        panel.SetSizer(sizer)
    def SetAccount(self,USDCAD,EURUSD):
        self.grid.SetCellValue(0, 0, str(USDCAD))
        self.grid.SetCellValue(0,1,str(EURUSD))
    def SetPrice(self,code,price):
        ci = self.dtColumnIndex[code]
        self.grid.SetCellValue(0, ci, str(price))

def DemoWSQCallback(Tick):
    USDCAD=Tick.Data[0][0]
    EURUSD=Tick.Codes[0]
    #form.SetAccount(USDCAD,EURUSD)
    form.SetPrice(Tick.Codes[0], Tick.Data[0][0])
    if not g_dt.has_key(Tick.Codes[0]): g_dt[Tick.Codes[0]] = []
    g_dt[Tick.Codes[0]].append(Tick.Data[0][0])

g_dt={}
# Run the program
if __name__ == "__main__":

    w.start()
    app = wx.PySimpleApp()
    form = MyForm()
    data=w.wsq(["USDCAD.FX","EURUSD.FX"],"rt_last",func=DemoWSQCallback)
    frame = form.Show()
    app.MainLoop()
    print g_dt