import wx
import wx
class ExampleFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        panel = wx.Panel(self)
        clearButton = wx.Button(self, wx.ID_CLEAR, "Clear")
        self.Bind(wx.EVT_BUTTON, self.OnClear, clearButton)
        self.Show()
    def OnClear():
        print("fuckl")

app = wx.App(False)
ExampleFrame(None)
app.MainLoop()
