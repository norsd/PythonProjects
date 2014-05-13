#coding: utf-8
__author__ = 'delon_000'

import threading
import wx
import wx.grid as  gridlib

class MyForm(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Grid with Popup Menu")

        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        self.grid = gridlib.Grid(panel)
        self.grid.CreateGrid(1,3)
        grid = self.grid
        grid.SetColLabelValue(0, u"账户")
        grid.SetColLabelValue(1, u"动态权益")
        grid.SetColLabelValue(2, u"持仓")


        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND, 5)
        panel.SetSizer(sizer)
    def SetAccount(self,a_account,a_position,a_cash):
        self.grid.SetCellValue(0, 0, a_account)
        self.grid.SetCellValue(0,1, str(a_position))
        self.grid.SetCellValue(0,2, str(a_cash))


_p = 1
_c = 23
def printit():
    if _bEnd:
        return
    global _p
    global _c
    threading.Timer(5.0, printit).start()
    form.SetAccount(u"测试账号", _p , _c)
    _p = _p+1
    _c = _c+20

# Run the program
if __name__ == "__main__":
    _bEnd = False
    app = wx.PySimpleApp()
    form = MyForm()
    printit()
    frame = form.Show()
    app.MainLoop()
    _bEnd = True