import UniversalLibrary as UL
import wx
import visa
import math as m
import matplotlib.pyplot as grapher

voltage=0
current=0
Conv = 0;
BoardNum = 0
Chan = 3
Gain = 20
var = 1.05
EngUnits=0;
VtoA = 0.34
MAXCURRENT = 4;
MINCURRENT = -4
fixed = False;

if not fixed:
    global MINCURRENT;
    MINCURRENT = 0;

endpt = 3;
stepSize = 10.0;
currentStepSize = 0.2 # MUST REDEFINE

isClosed = False
curUp = False
currentList = list()
magList = list() #list holding magnetization values - may be redefined below in a method that will print them all out at once
BList = list() #list holding magnetic field values
KList = list() #holds Keithley readings
PeakList = list() #holds the endpts that the loop flips at

rm=visa.ResourceManager()
k=rm.open_resource('GPIB0::2::INSTR')



        
class Main(wx.Frame):
    
    
    def __init__(self, parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(1000,1000))
        #self.control = wx.TextCtrl(self)
        self.CreateStatusBar()
        self.InitUI()
        self.checkGain();
        self.InitKeithley()
        
        '''Exit menu stuff'''
        filemenu = wx.Menu()
        ex = filemenu.Append(wx.ID_EXIT, "&Exit", "Exit the program")
        self.Bind(wx.EVT_MENU, self.OnExit, ex)
        
        menubar=wx.MenuBar()
        menubar.Append(filemenu,"&File")
        
        self.SetMenuBar(menubar);
        self.Show(True)
        """Keithley setup right here"""
        rm=visa.ResourceManager()
        k=rm.open_resource('GPIB0::2::INSTR')
        k.query("*IDN?")
        
    def InitUI(self):   
        
        pnl = wx.Panel(self, size = (500,400))
        self.btnV = wx.Button(pnl, 20, "Set Voltage Input", (50,50))
        self.btnA = wx.Button(pnl, 20, "Set Current Input",(200,50))
        self.quote = wx.StaticText(pnl, label ="Hysteresis Loop TestCode 1", pos=(5,5))
        #self.textField = wx.TextCtrl(self, pos=(50,150));
       
        self.btnCurrentList = wx.Button(pnl, 20, "Get Current Array", (500,100))
        self.btnAllLists = wx.Button(pnl, 20, "Get All Arrays", (500,150))
        self.btnCurrentList.Bind(wx.EVT_BUTTON, self.OnCurrentListPress)
        self.btnAllLists.Bind(wx.EVT_BUTTON,self.OnAllListPress)        
        
        self.btnV.Bind(wx.EVT_BUTTON, self.OnVoltagePress)
        self.btnA.Bind(wx.EVT_BUTTON, self.OnCurrentPress)
        
        #hysteresis section
        self.btnStartLoop = wx.Button(pnl, 20, "Start Hysteresis Loop", (50,400))
        self.btnStartLoop.Bind(wx.EVT_BUTTON, self.OnStartLoopPress)
        self.labelHStart = wx.TextCtrl(pnl, pos = (50,450), size = (140,40), style=wx.TE_READONLY)
        self.btnReadKeithley = wx.Button(pnl,20, "Read Keithley Value",(500,200))
        self.btnReadKeithley.Bind(wx.EVT_BUTTON, self.onReadKeithleyPress)
        self.btnStrtCurrFluc = wx.Button(pnl, 20, "Start Loop for Current Fluctuation", (300,400))
        self.btnStrtCurrFluc.Bind(wx.EVT_BUTTON, self.OnStartFlucLoopPress)
        
        
        self.txtV = wx.TextCtrl(pnl,pos = (50, 150) , size =(140,30))
        self.txtV.SetValue("Volts")
        self.txtA = wx.TextCtrl(pnl,pos = (200, 150) , size =(140,30))
        self.txtA.SetValue("Amperes")

        self.labelV = wx.TextCtrl(pnl, pos = (50,220), size = (280,35),style=wx.TE_READONLY)
        self.labelV.SetValue("Voltage is 0 V");
        self.labelA = wx.TextCtrl(pnl, pos=(50,270), size = (280,35),style=wx.TE_READONLY)
        self.labelA.SetValue("Current is 0 A");
        
        self.SetSize((800,800))
        self.SetTitle('Kepco 50-8M Control')
        self.Centre()
        
        self.Show(True)          
    
    #Keithley related methods
    def query(self, message):
        global k
        return k.query(str(message))
    def write(self, message):
        global k
        k.write(str(message))
    def InitKeithley(self):
        print(self.query("*IDN?"))
        #self.write("*rst;status:preset;*cls")
        #self.updateVoltage(0)
    
    #Label Updates    
    def vLabelUpdate(self,volt,boole):
        if boole:
            self.labelV.SetValue(str(volt))
        else:
            self.labelV.SetValue("Voltage is "+str(volt)+" V")
    def aLabelUpdate(self,amp, boole):
        if boole:
            self.labelA.SetValue(str(amp))
        else:
            self.labelA.SetValue("Current is "+str(amp)+" A")
    def HStartUpdate(self,message):
        self.labelHStart.SetValue(str(message))   
        
    #Setting and Getting Global vars    
    def getVoltage(self):
        global voltage
        return voltage;
    def setVoltage(self, volt):
        global voltage
        voltage = volt;
    def setCurrent(self, amp):
        global current
        current = amp;
    def getCurrent(self):
        global current
        return current;    
    def addCurrentVal(self, val):
        global currentList
        currentList.append(val)
    def setEndpt(self, val):
        global endpt
        endpt = val;
    def getEndpt(self):
        global endpt
        return endpt
    def flipStep(self):
        global currentStepSize
        currentStepSize=-1*currentStepSize;
    
    #Functions involving list values
    def addPeak(self,val):
        global PeakList
        PeakList.append(val)
    def getMagField(self, index):
        global magList
        return magList[index]
    def addMagField(self,val):
        global magList
        magList.append(val)
    def addPresentCurrent(self,val):
        global currentList
        currentList.append(val)
    def addBField(self,val):
        global BList
        BList.append(val)
    def addKeithleyReading(self):
        global KList
        data =self.query(":FETCH?");
        KList.append(data[:13])        
   
    #Printing lists 
    def printCurrentList(self):
        global currentList
        print(currentList);
    def printMagList(self):
        global magList
        print(magList);
    def printBList(self):
        global BList
        print(BList);
    def printPeakList(self):
        global PeakList
        print(PeakList);
    def printKList(self):
        global KList
        print(KList);    
    
    #Button press functions
    def OnVoltagePress(self,event):
        vString =self.txtV.GetValue();
        print(vString);
        self.updateVoltage(float(vString));
    def OnCurrentPress(self,event):
        aString =self.txtA.GetValue();
        print(aString)
        self.updateCurrent(float(aString));
    def OnCurrentListPress(self,event):
            global currentList
            print(currentList)
    def OnAllListPress(self,event):
        self.printAll();
    def onReadKeithleyPress(self,event):
        print(self.query(':FETCh?'))# returns voltage and type (DC or AC), the wrong time and date, some txt string, and the location of the source of measurement (external, etc.)
        #temp = self.query(':FETCh?');
        #temp = temp[:temp.index(",")];
        #print(temp)
    def OnStartLoopPress(self,event):
        """
        This is where the code for the loop needs to go - All of it. It should have a check to see if it at the end magnetization, and if so, turn around
        Next issue: how to make it turn around - if endpt is even/odd or changed, have a global value change from positive to negative, and have current go
        change by this value - will ensure that the change is correct
        
        use a while loop here to keep increasing value until saturation magnetic field is reached - using compEndpt to return true or false
        """
        
        self.HStartUpdate("Starting")
        self.updateCurrent(0.0);
        
        if(self.getEndpt()>0):
            print("endpt var is good")#should check to see if it's at the endpoint; if so, endpt = endpt-1
        print("working");
        print(self.query("*IDN?")) 
    def OnStartFlucLoopPress(self,event):
        time = 50;
        time1=time;
        self.write(":SCAN:COUNT:INFINITE")
        while time>0:
            self.addKeithleyReading()
            time=time-1
            self.write(":SCAN:TIMER 0.001")
        if time==0:
            self.vLabelUpdate("Done", True)
        self.printKList();
        
        #self.graph(time1)
    def OnExit(self, event):
        self.updateVoltage(0);
        self.Close(True)
    
    def graph(self,time):
        global KList;
        timeList = list()
        dataList = list()
        n=1
        while time>0:
            timeList.append(n)
            n=n+1;
        for reading in KList:
            if reading[9:10]=="+":
                r = reading[3:-5]*m.pow(10,float(reading[reading.index("+")+1:]))
                dataList.append(r)
            else:
                r = reading[3:-5]*m.pow(10,-1*float(reading[reading.index("+")+1:]))
                dataList.append(r)
        grapher.plot(timeList,dataList)
        grapher.show()
        
    
    def checkGain(self):
        global Gain,var,Conv
        if(Gain==20):
            Conv = 10.0/9*var
        elif(Gain==23):
            Conv = (10.0-0.19)/17
        elif(Gain==15):
            Conv = 5.0/13
    def updateVoltage(self,volt):
        global voltage, EngUnits,BoardNum,Chan,Gain,Conv,VtoA;
        if self.isVoltageInRange(volt):
            self.setVoltage(volt);
            EngUnits = self.getVoltage();
            DataValue = UL.cbFromEngUnits(BoardNum, Gain, EngUnits*Conv, 0)
            UL.cbAOut(BoardNum, Chan, Gain, DataValue)
            self.vLabelUpdate(voltage,False);
            self.aLabelUpdate(voltage*VtoA,False)
        else:
            self.vLabelUpdate("Your voltage is too high: It must be between "+str(4/VtoA)+" and "+str(-4/VtoA) +"Amps",True)
    def updateCurrent(self,amp):
        global current, EngUnits,BoardNum,Chan,Gain,Conv,VtoA, curUp;
        if self.isCurrentInRange(amp):
            self.setCurrent(amp);
            EngUnits = self.getCurrent()/VtoA;
            DataValue = UL.cbFromEngUnits(BoardNum, Gain, EngUnits*Conv, 0)
            UL.cbAOut(BoardNum, Chan, Gain, DataValue)
            self.aLabelUpdate(current,False);
            self.vLabelUpdate(current/VtoA,False)
            self.addCurrentVal(current)
            curUp = True;
            curUp = False;
        else:
            self.aLabelUpdate("Your current is too high: It must be between 4 and -4 Amps",True)
        
    def wasCurrentUpdated(self):
        global curUp;
        return curUp;    
        
    def isItClosed(self):
        global isClosed
        return isClosed
    def isCurrentInRange(self, val):
        global MAXCURRENT,MINCURRENT
        if val<=MAXCURRENT and val >=MINCURRENT:
            return True;
        else:
            return False
    def isVoltageInRange(self, val):
        global MAXCURRENT,MINCURRENT, VtoA
        if val*VtoA<=MAXCURRENT and val*VtoA >=MINCURRENT:
            return True;
        else:
            return False
    
    #all the functions involving the APD
    def compEndpt(self):
        global KList
        print("This is for test output")

        i = len(KList)-1;
        if len(KList) >1:
            if m.abs(KList[i]-KList[i-1]) <0.001:
                self.flipStep();
                self.addPeak(self.getMagField(-1))
                self.setEndpt(self.getEndpt -1)
                return True
            else:
                self.addKeithleyReading()
                self.addPresentCurrent(self.getCurrent())
                self.addMagField(0) #filler value - probably something with the Keithley reading interaction
        else:
            return False
        """this will compare values coming from the Keithley to see if the values are the same
        Probably will use array of values from Keithley to and compare the ith and the ith-1, and have it be close (if abs(array(i)-array(i-1))<=1),
        put the current value at this time into a special place, and then reverse as per a var. If this var is hit twice, break;
        it can return false or something to make it keep going
        
        IF TRUE, ENDPT IS REACHED
        """
        
        if self.getEndpt()<=0:
            while self.getCurrent() != 0:
                self.setCurrent(self.getCurrent()-currentStepSize)
                self.addCurrentVal(self.getCurrent()) #gets current values into the list while dropping the current -need to get info from Keithley into this method as well
    def printAll(self):
        self.printCurrentList()
        self.printMagList()
        self.printBList()
        self.printPeakList()
        self.printKList()
            


app = wx.App(False);
frame = Main(None, 'Small Editor')
app.MainLoop()



