import wx

"""app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
frame = wx.Frame(None, wx.ID_ANY, "Kepco 50-8M Control") # A Frame is a top-level window.
frame.Show(True)     # Show the frame.
app.MainLoop()"""

voltage = 0;
current = 0;
class Main(wx.Frame):
    def __init__(self, parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(800,800))
        #self.control = wx.TextCtrl(self)
        self.CreateStatusBar()
        self.InitUI()
        '''Button Stuff'''
        
        #y = self.ask(message = 'Enter the voltage here')
        #print y
        
        
        '''Exit menu stuff'''
        filemenu = wx.Menu()
        ex = filemenu.Append(wx.ID_EXIT, "&Exit", "Exit the program")
        self.Bind(wx.EVT_MENU, self.OnExit, ex)
        
        menubar=wx.MenuBar()
        menubar.Append(filemenu,"&File")
        
        self.SetMenuBar(menubar);
        self.Show(True)
        
    def InitUI(self):   
        
        pnl = wx.Panel(self)
        self.btnV = wx.Button(pnl, 20, "Set Voltage Input", (50,50))
        self.btnA = wx.Button(pnl, 20, "Set Current Input",(200,50))
        self.quote = wx.StaticText(pnl, label ="Voltage And Current Control", pos=(0,0))
        #self.textField = wx.TextCtrl(self, pos=(50,150));
       

        self.btnV.Bind(wx.EVT_BUTTON, self.OnVoltagePress)
        self.btnA.Bind(wx.EVT_BUTTON, self.OnCurrentPress)
        
        self.txtV = wx.TextCtrl(pnl,pos = (50, 150) , size =(140,30))
        self.txtV.SetValue("Volts")
        
        self.txtA = wx.TextCtrl(pnl,pos = (200, 150) , size =(140,30))
        self.txtA.SetValue("Amperes")

        self.SetSize((500, 400))
        self.SetTitle('Kepco 50-8M Control')
        self.Centre()
        self.Show(True)          
    
    def OnExit(self, event):
        self.Close(True)
    def OnVoltagePress(self,event):
        vString =self.txtV.GetValue();
        print(vString);
    def OnCurrentPress(self,event):
        aString =self.txtA.GetValue();
        print(aString);
    def ask(parent=None, message='voltage here', default_value=' '):
        dlg = wx.TextEntryDialog(parent,message,defaultValue = default_value)
        dlg.ShowModal()
        result = dlg.GetValue()
        dlg.Destroy()
        return result;

app = wx.App(False);
frame = Main(None, 'Small Editor')
app.MainLoop()

