import VoltageTest1 as vt

import wx
import UniversalLibrary as UL

n = 0; #step number
magField = []
magnetization = [] #for both, the index position will be the certain step, so the full list will be of len n
curr = [];

app = wx.App(False)
frame = vt.Main(None, 'Small Editor')

while not vt.Main(isItClosed()):
    if vt.Main.wasCurrentUpdated():
        curr.append(vt.Main.getCurrent())


app.MainLoop()

answer = input("Do you want the current array?")
if answer == "y" or answer == "yes":
    print(curr)