# -*- coding: cp1252 -*-
#!/usr/bin/python
# Input / Output for the induction simulation

#Optionen:
# Option 1: import pylab siehe unten. Importiert Schnittstelle mit MatLab
# Kurvenzeichnungen
# Option 2: Non-MI-Mean-Out siehe unten. Per Default wird Non-MI-Mean nicht eingezeichnet.
#Wenn Non-MI-Mean-Out ausgeklammert wird, wird Non-MI-Mean eingezeichnet.
#Option 3: siehe unter "Simulation Class": "def greyscale". Strichstärken ändern.
#Option 4: in Klasse "def Sim(Parameters)": für Worlddeceived den betrogenen MI
#am Index ändern.
#Option 5: CHAOSKORREKTUR
# chaotische Verläufe treten bei Eventfrquencies nicht auf, weil Eventfrequencies
#historische Attribute sind.  Anders zB bei Populationshäufigkeiten etc.
#Option 6: Eventfrequency nur ausdrucken in orange, ohne im Logging.

from __future__ import generators
import copy, time
import wx
from PyPlotter import Gfx, wxGfx, psGfx, Graph, Colors
import Induction
# neuer Import
## import pylab

# Non-MI-Mean-Out siehe unten

class SimWindow(wxGfx.Driver, Gfx.Window):
   
    def __init__(self, exampleDict, size=(500, 400),
                 title="wxGraph", app=None):
        if app != None:
            self.app = app
        else:
            self.app = wx.App() # PySimpleApp()
            
        self.sim = None
        self.oldGfxSize = (100, 200)
        self.exampleDict = exampleDict
            
        self.win = wx.Frame(None, -1, title)#, style=
                           #wxSYSTEM_MENU|wxCAPTION|wxMINIMIZE_BOX|
                           #wxNO_FULL_REPAINT_ON_RESIZE)
        self.win.SetSize(size)
        self.menuBar = wx.MenuBar()
        menu = wx.Menu()
        keys = self.exampleDict.keys()
        keys.sort()
        self.idDict = {}
        id = 1000
        for k in keys:
            id += 1
            item = wx.MenuItem(menu, id, k)
            self.idDict[id] = self.exampleDict[k]
            menu.AppendItem(item)
            wx.EVT_MENU(self.win, id, self.OnExample)
        self.menuBar.Append(menu, "Examples")
        
        menu = wx.Menu()
        self.logItem = wx.MenuItem(menu, 2001, "Logging on",
                          "Turn simulation log on."+\
                          "(Slows down the simulation!)", wx.ITEM_CHECK)
        self.doLogging = True
        menu.AppendItem(self.logItem)
        self.logItem.Check(self.doLogging)        
        self.bwItem = wx.MenuItem(menu, 2003, "Black & White", "",
                                 wx.ITEM_CHECK)
        self.blackwhite = False
        menu.AppendItem(self.bwItem)    

        self.hardruleItem = wx.MenuItem(menu, 2004, "Hardrule", "",
                                       wx.ITEM_CHECK)
        menu.AppendItem(self.hardruleItem)
        self.deceivedOIItem = wx.MenuItem(menu, 2005, "World Deception", "",
                                         wx.ITEM_CHECK)
        menu.AppendItem(self.deceivedOIItem)
        self.meanValueItem = wx.MenuItem(menu, 2006, "Show Mean Values", "",
                                        wx.ITEM_CHECK)
        self.showMeanValues = True
        menu.AppendItem(self.meanValueItem)
        self.meanValueItem.Check(self.showMeanValues)
        self.logScaleItem = wx.MenuItem(menu, 2007, "Logarithmic Scale", "",
                                       wx.ITEM_CHECK)
        self.logScale = False
        menu.AppendItem(self.logScaleItem)
        self.absoluteSuccessItem = wx.MenuItem(menu, 2009, "Absolute Success", "",
                                              wx.ITEM_CHECK)
        self.absoluteSuccess = False
        menu.AppendItem(self.absoluteSuccessItem)
        self.shuffleDrawItem = wx.MenuItem(menu, 2008, "Overlapping Graphs Visible", "",
                                          wx.ITEM_CHECK)
        self.shuffleDraw = False
        menu.AppendItem(self.shuffleDrawItem)
        self.menuBar.Append(menu, "Preferences")
        wx.EVT_MENU(self.win, 2001, self.OnLogging)
        wx.EVT_MENU(self.win, 2004, self.OnHardrule)
        wx.EVT_MENU(self.win, 2003, self.OnBlackWhite)
        wx.EVT_MENU(self.win, 2005, self.OnDeceivedOI)
        wx.EVT_MENU(self.win, 2006, self.OnShowMeanValues)
        wx.EVT_MENU(self.win, 2007, self.OnLogScale)
        wx.EVT_MENU(self.win, 2008, self.OnShuffleDraw)
        wx.EVT_MENU(self.win, 2009, self.OnAbsoluteSuccess)

##        menu = wx.Menu()
##        item = wx.MenuItem(menu, 3001, "Quality plot of current graph")
##        menu.AppendItem(item)
##        self.menuBar.Append(menu, "Extras")
##        EVT_MENU(self.win, 3001, self.OnQualityPlot)
        
        self.win.SetMenuBar(self.menuBar)
        self.logItem.Check(self.doLogging)
        #self.bwItem.Check(self.blackwhite)
        
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.notebook = wx.Notebook(self.win, -1, size=size)
        #self.nbSizer = wx.NotebookSizer(self.notebook)
        wx.EVT_NOTEBOOK_PAGE_CHANGED(self.notebook, -1, self.OnNotebook)

        self.gfxPage = wx.Panel(self.notebook, -1, style=wx.NO_BORDER)
        self.notebook.AddPage(self.gfxPage, "Graph")

        self.logPage = wx.Panel(self.notebook, -1, style=wx.NO_BORDER)
        ffont = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL)
        tAttr = wx.TextAttr(wx.Colour(0,0,0)) #, font = ffont)
        tAttr.SetFont(ffont)        
        self.logbook = wx.TextCtrl(self.logPage, -1,
               style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_DONTWRAP|wx.TE_RICH)
        self.logbook.SetDefaultStyle(tAttr)
        self.notebook.AddPage(self.logPage, "Log")
        
        self.logSizer = wx.BoxSizer(wx.VERTICAL)
        self.logSizer.Add(self.logbook, 1, wx.EXPAND)
        self.logButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(self.logPage, -1, "Save Log...")
        self.logButtonSizer.Add(btn, 1)
        wx.EVT_BUTTON(btn, -1, self.OnSaveLog)
        self.logSizer.Add(self.logButtonSizer)
        self.logPage.SetAutoLayout(1)
        self.logPage.SetSizer(self.logSizer)
        self.logSizer.Fit(self.logPage)
        self.logSizer.SetSizeHints(self.logPage)

        self.topSizer = wx.BoxSizer(wx.VERTICAL)
        self.gfxArea = wx.Window(self.gfxPage, -1, size=size)
        self.gfxArea.SetSizeHints(200, 100, 1600, 1200)

        controls = [("< Zoom", self.OnZoomOut),
                    ("Zoom >", self.OnZoomIn),
                    (" ", self.OnNOP),
                    ("Save Image...", self.OnSave),
                    ("Postscript...", self.OnPrint)]

        self.bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        for control in controls:
            label, cmd = control
            if label != " ":
                btn = wx.Button(self.gfxPage, -1, label)
                self.bottomSizer.Add(btn, 1, wx.ALIGN_LEFT)
                wx.EVT_BUTTON(btn, -1, cmd)
            else:
                spacer = wx.StaticText(self.gfxPage, -1, label)
                self.bottomSizer.Add(spacer, 1, wx.ALIGN_LEFT)

        self.topSizer.Add(self.gfxArea, 1, wx.EXPAND)
        self.topSizer.Add(self.bottomSizer, 0)
        self.gfxPage.SetAutoLayout(1)
        self.gfxPage.SetSizer(self.topSizer)
        self.topSizer.Fit(self.gfxPage)
        self.topSizer.SetSizeHints(self.gfxPage)

        self.mainSizer.Add(self.notebook, 1, wx.EXPAND)
        self.win.SetAutoLayout(1)
        self.win.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.win)
        self.mainSizer.SetSizeHints(self.win)
        
        csize = self.gfxArea.GetClientSize()        
        self.buffer = wx.EmptyBitmap(csize.width, csize.height)
        dc = wx.BufferedDC(None, self.buffer)
        self.app.SetTopWindow(self.win)
        
        self.refreshFlag = True
        self.resizedFlag = False
        self.zoomPivot = (0,0)
        self.dragPen = wx.Pen(wx.Colour(0,0,0), 2, wx.SHORT_DASH)
        self.dragBrush = wx.Brush(wx.Colour(0,0,0), wx.TRANSPARENT)
        
        wx.EVT_PAINT(self.win, self.OnPaint)
        wx.EVT_IDLE(self.win, self.OnIdle)
        wx.EVT_SIZE(self.win, self.OnSize)

        wx.EVT_LEFT_DOWN(self.gfxArea, self.OnLeftDown)
        wx.EVT_LEFT_UP(self.gfxArea, self.OnLeftUp)
        wx.EVT_MOTION(self.gfxArea, self.OnMotion)
        
        wxGfx.Driver.__init__(self, dc)

        self.win.SetSize(size)
        #self.nbSizer.Fit(self.notebook)
        self.win.Show(1)        
        self.win.Refresh()     

    def logAppend(self, text):
        self.logbook.AppendText(text)

    def clearLog(self):
        self.logbook.Clear()

    def OnPaint(self, event):
        self.refreshFlag = True
        event.Skip()

    def OnIdle(self, event):
        if self.refreshFlag:
            if self.resizedFlag:
                size = self.gfxArea.GetClientSize()
                if size != self.oldGfxSize:
                    self.buffer = wx.EmptyBitmap(size.width, size.height)
                    dc = wx.BufferedDC(None, self.buffer)
                    self.changeDC(dc)
                    self.clear()
                    self.sim.resizedCallback()
                    self.oldGfxSize = size
                    self.resizedFlag = False
            dc = wx.ClientDC(self.gfxArea)
            dc.BeginDrawing()
            dc.Blit(0, 0, self.w, self.h, self.getDC(), 0, 0)
            dc.EndDrawing()
            self.refreshFlag = False

    def refresh(self):
        #self.win.Refresh()
        #self.win.Update()
        #self.refreshFlag = True
        #self.app.ProcessIdle()
        #self.refreshFlag = True
        self.refreshFlag = True
        #self.app.ProcessIdle()
        self.OnIdle(None)
        #self.win.Refresh()
        #self.win.Update()

    def quit(self):
        self.win.Close()
        
    def waitUntilClosed(self):
        self.app.MainLoop()

    def OnExample(self, event):
        id = event.GetId()
        apply(self.sim.Sim, self.idDict[id])
    
    def OnLogging(self, event):
        if self.logItem.IsChecked():
            self.doLogging = True
        else:
            self.doLogging = False
            self.clearLog()

    def OnHardrule(self, event):
        if self.hardruleItem.IsChecked():
            Induction.hardrule = True
        else:
            Induction.hardrule = False

    def OnBlackWhite(self, event):
        if self.bwItem.IsChecked():
            self.blackwhite = True
        else:
            self.blackwhite = False        

    def OnDeceivedOI(self, event):
        if self.deceivedOIItem.IsChecked():
            self.sim.worldDeception = True
        else:
            self.sim.worldDeception = False

    def OnShowMeanValues(self, event):
        if self.meanValueItem.IsChecked():
            self.showMeanValues = True
        else:
            self.showMeanValues = False
        
    def OnLogScale(self, event):
        if self.logScaleItem.IsChecked():
            self.logScale = True
        else:
            self.logScale = False
        self.sim.changeScale(self.logScale)
        self.refresh()
        
    def OnShuffleDraw(self, event):
        if self.shuffleDrawItem.IsChecked():
            self.shuffleDraw = True
        else:
            self.shuffleDraw = False
        self.sim.changeDrawMode(self.shuffleDraw)
        self.refresh()

    def OnAbsoluteSuccess(self, event):
        if self.absoluteSuccessItem.IsChecked():
            self.absoluteSuccess = True
        else:
            self.absoluteSuccess = False

    def OnSize(self, event):
        self.resizedFlag = True
        self.refreshFlag = True
        event.Skip()

    def OnNotebook(self, event):
        nb = event.GetSelection()
        str = self.notebook.GetPageText(nb)
        if str == "Graph":
            #print str
            self.refreshFlag = True
        event.Skip()

    def OnNOP(self, event):
        pass

    def OnZoomIn(self, event):
        self.sim.zoomIn()

    def OnZoomOut(self, event):
        self.sim.zoomOut()

    def OnPrint(self, event):
        fD = wx.FileDialog(None, message = "Please select a file name:",
                          wildcard = "*.ps",
                          style =wx.SAVE|wx.OVERWRITE_PROMPT|wx.CHANGE_DIR)
        result = fD.ShowModal()
        if result != wx.ID_CANCEL:
            fName = fD.GetFilename()
            if fName[-3:] != ".ps": fName = fName + ".ps"
            self.sim.writePostscript(fName)
        fD.Destroy()
        self.refreshFlag = True

    def OnSave(self, event):
        fD = wx.FileDialog(None, message = "Please select a file name:",
                          wildcard = "*.png",
                          style =wx.SAVE|wx.OVERWRITE_PROMPT|wx.CHANGE_DIR)
        result = fD.ShowModal()
        if result != wx.ID_CANCEL:
            fName = fD.GetFilename()
            if fName[-4:] != ".png": fName = fName + ".png"
            image = wx.ImageFromBitmap(self.buffer)
            # wx.Image_AddHandler(wx.PNGHandler())
            image.SaveFile(fName, wx.BITMAP_TYPE_PNG)
        fD.Destroy()
        self.refreshFlag = True

    def OnSaveLog(self, event):
        fD = wx.FileDialog(None, message = "Please select a file name:",
                          wildcard = "*.txt",
                          style =wx.SAVE|wx.OVERWRITE_PROMPT|wx.CHANGE_DIR)
        result = fD.ShowModal()
        if result != wx.ID_CANCEL:
            fName = fD.GetFilename()
            if fName[-4:] != ".txt": fName = fName + ".txt"
            try:
                f = open(fName, "w")
                f.write(self.logbook.GetValue())
                f.close()
            except IOError:
                print "IOError!!!"
        fD.Destroy()        

    def OnLeftDown(self, event):
        self.zoomPivot = event.GetPositionTuple()
        self.gfxArea.CaptureMouse()

    def OnLeftUp(self, event):
        if self.gfxArea.HasCapture():
            x2, y2 = event.GetPositionTuple()            
            self.gfxArea.ReleaseMouse()
            dc = wx.ClientDC(self.gfxArea)
            dc.BeginDrawing()
            dc.Blit(0, 0, self.w, self.h, self.dc, 0, 0)
            dc.EndDrawing()
            x1, y1 = self.zoomPivot
            y1 = self.h-y1; y2 = self.h-y2
            self.sim.zoom(min(x1,x2), min(y1,y2), max(x1,x2), max(y1,y2))

    def OnMotion(self, event):
        if event.Dragging() and event.LeftIsDown():
            dc = wx.ClientDC(self.gfxArea)
            dc.BeginDrawing()
            dc.Blit(0, 0, self.w, self.h, self.dc, 0, 0)
            dc.SetPen(self.dragPen)
            dc.SetBrush(self.dragBrush)
            x1, y1 = self.zoomPivot
            x2, y2 = event.GetPositionTuple()
            w = abs(x2-x1+1);  h = abs(y2-y1+1)
            x = min(x1, x2);  y = min(y1, y2)
            dc.DrawRectangle(x, y, w, h)
            dc.EndDrawing()

##    def OnQualityPlot(self, event):
##        self.sim.QualityPlot()
        

########################################################################
#
#   Simulation class
#
########################################################################

def ProxyPenGenerator(penList=[]):
    for pen in penList:
        yield pen
    if penList != []: print "Warning: pen list seems to be too short!"
    for c in Colors.colors:
        yield Gfx.Pen(c)


##def (pen):
##    c = pen.color
##    p = copy.copy(pen)
##    av = (c[0]+c[1]+c[2]) / 3
##    if c[0] > c[1] and c[0] > c[2]:
##        #pen.linePattern = Gfx.DOTTED
##        p.lineWidth = Gfx.MEDIUM
##    elif c[2] > c[0] and c[2] > c[1]:
##        #pen.linePattern = Gfx.DASHED
##        p.lineWidth = Gfx.MEDIUM
##    else:
##        #pen.linePattern = Gfx.CONTINUOUS
##        p.lineWidth = Gfx.MEDIUM
##    p.color = (av, av, av)
##    return p

def greyscale(pen):
    c = pen.color
    p = copy.copy(pen)
    av = (c[0]+c[1]+c[2])/3
    if c[0] > c[1] and c[0] > c[2]:
        dark = av/2
        p.color = (dark, dark, dark)
# hier MI ändern von Medium auf Thin   
        p.lineWidth = Gfx.THIN
    elif c[2] > c[0] and c[2] > c[1]:
        bright = av*0.3 + 0.5
        p.color = (bright, bright, bright)
# MIs alle unter 0.5, also dunkel: non-Mis alle über 0.5, also heller
#OI ausgezeichnet durch Thin schwarz
    else:
        p.color = (0.0, 0.0, 0.0)
        p.lineWidth = Gfx.THIN 
    return p

def greyscaleMean(pen):
    p = copy.copy(pen)
    c = p.color
    av = (c[0]+c[1]+c[2])/3
    p.color = (av, av, av)
    return p
    


class Simulation:
    def __init__(self, exampleDict, winTitle = "Induction Simulation",
                 eventFunction = lambda : getRandomEvent(2.0/3.0)):   
        self.win = SimWindow(exampleDict, size=(950,700), title=winTitle)
        self.win.sim = self
        self.graph = Graph.Cartesian(self.win, 1, 0.0, 1000, 1.0,
                                     "Graph", "Round (time)", "Success Rate",
                                     styleFlags = \
                                     Graph.DEFAULT_STYLE) 
        self.shortNameDict = {}
        self.worldDeception = False


    def run(self):
        self.win.waitUntilClosed()


    def Sim(self, title, predictorList, penList = [], rounds = 500,
            eventFunction = lambda : Induction.getRandomEvent(2.0/3.0)):
        self.graph.reset(1, 0.0, rounds, 1.0)
        if self.win.absoluteSuccess:
            self.graph.setLabels(yaxis="Absolute Success")
        else:
            self.graph.setLabels(yaxis="Success Rate")
        self.graph.setTitle(title)
        self.zoomlist = [(1, 0.0, rounds, 1.0)]
        self.zoomPos = 0
        self.predictorList = copy.deepcopy(predictorList)
        self.world = Induction.World(eventFunction)
        for predictor in self.predictorList:
            self.world.register(predictor)
        if self.worldDeception:
            # Hier bei [0] moegliche Veraenderung des Betrogenen MI eintragen
            self.world.worldDeceived = self.world.miList[0]
        penBox = ProxyPenGenerator(penList)
        for predictor in self.predictorList:
            pen = penBox.next()
            pen.lineWidth = Gfx.MEDIUM
            if self.win.blackwhite:  p = greyscale(pen)
            else: p = pen
            # print pen.lineWidth
            self.graph.addPen(str(predictor), p)
        pen = penBox.next()
        pen.lineWidth = Gfx.MEDIUM
        #if self.win.blackwhite:  greyscale(pen)        

        Np = len(self.world.getPredictorList())
        Nmi = len(self.world.miList)
        Nn_mi = len(self.world.non_miList)
        
        self.win.clearLog()
        self.fmtStr = "%5i:| " + \
                      "%1.2f "*(Np) + \
                      "|" + " %4s"*Nmi + \
                      " ||" + "%4s|"*Nn_mi + "\n" 
        s0 = "Round | "
        s0+= ("Success Rates"+" "*100)[:5*Np] + "|"
        s0+= (" Favorites"+" "*100)[:5*Nmi] + " ||"
        s0+= ("Deceivers"+" "*100)[:5*Nn_mi]
        self.win.logAppend(s0+"\n")
        s = "      | "
        for p in self.world.getPredictorList():
            s += "%4s " % self.shortName(p)
        s += "|"        
        for mi in self.world.miList:
            s += " %4s" % self.shortName(mi)
        s += " ||"
        for p in self.world.non_miList:
            s += "%4s|"  % self.shortName(p)
        self.win.logAppend(s+"\n")
        self.win.logAppend("-"*len(s)+"\n")

# Zur Mittelwertberechnung      
        if self.win.showMeanValues:
            p1 = Gfx.Pen((0.3, 0.0, 0.6), lineWidth=Gfx.THICK,
                         linePattern=Gfx.CONTINUOUS)
            p2 = Gfx.Pen((0.0, 0.0, 0.0), lineWidth=Gfx.THICK,
                         linePattern=Gfx.CONTINUOUS)
            if self.win.blackwhite:
                p1 = greyscaleMean(p1); p1.lineWidth = Gfx.THICK
                p2 = greyscaleMean(p2); p2.lineWidth = Gfx.THICK
# Non-MI-Mean-Out: folgende Zeile auskommentieren, um non-MI-mean anzuzeigen                
            p1 = Graph.DONT_DRAW_PEN
            self.graph.addPen("non_miMean", p1)           
            self.graph.addPen("miMean", p2)
# Mittelwerberechnung Ende


#Option 6:
#        p = Gfx.Pen((0.8, 0.5, 0.0), lineWidth=Gfx.MEDIUM,  \
#        linePattern=Gfx.CONTINUOUS)
#        self.graph.addPen("Event Frequency", p)   

        self.calcNdraw(1, rounds)


    def calcNdraw(self, a, b):
        last_xPixel = -1
        for n in range(a, b+1):
            xPixel = self.graph._scaleX(n)
            if xPixel > last_xPixel:
                last_xPixel = xPixel
                plotFlag = True
            else:  plotFlag = False
#Option 5: CHAOSKORREKTUR:
#extrem steile Fluktuationen könnten dadurch evtl. nicht eingezeichnet werden.
#wenn man das nicht will, setzt man "poltFlag" auch unter "else" auf "True".
            self.prepareLog()         
            self.world.nextRound() 
            pList = self.world.getPredictorList()
            if plotFlag:
                for predictor in pList:
                    if self.win.absoluteSuccess:
                        self.graph.addValue(str(predictor), n, \
                                            predictor.success)                        
                    else:
                        self.graph.addValue(str(predictor), n, \
                                            predictor.successRate)
#Option 6
#            self.graph.addValue("Event Frequency", n, \
#            self.world.relFrequency)

# Mittelwertberechnung
            if self.win.showMeanValues and plotFlag:
                if not self.win.absoluteSuccess:  av = self.world.non_miMean
                else:  av = self.world.non_miMean * self.world.round
                self.graph.addValue("non_miMean", n, av)
                if not self.win.absoluteSuccess:  av = self.world.miMean
                else: av = self.world.miMean * self.world.round
                self.graph.addValue("miMean", n, av)
                # print self.world.non_miMean, self.world.miMean, len(self.world.non_miList)
# Mittelwertberechnung Ende

            if n % ((b-a) / 10) == 0:  self.win.refresh()
            if self.win.doLogging: self.updateLog()
        if (self.graph.styleFlags & Graph.SHUFFLE_DRAW) or \
           (self.graph.styleFlags & Graph.EVADE_DRAW):
            self.graph.redrawGraph()
        self.win.refresh()
        
        
    def changeScale(self, logScale):
        if logScale:
            self.graph.setStyle(self.graph.styleFlags|Graph.LOG_X, redraw=True)
        else:
            self.graph.setStyle(self.graph.styleFlags & ~Graph.LOG_X, redraw=True)
            
    def changeDrawMode(self, shuffleDraw):
        if shuffleDraw:
            self.graph.setStyle(self.graph.styleFlags|Graph.SHUFFLE_DRAW, redraw=True)
        else:
            self.graph.setStyle(self.graph.styleFlags & ~Graph.SHUFFLE_DRAW, redraw=True)
        
    def shortName(self, predictor):
        if predictor:
            return predictor.shortName(3)
        else: return " - "
##        name = str(predictor)
##        try:
##            return self.shortNameDict[name]
##        except KeyError:
##            if len(name) <= 3:
##                s = ""
##                for c in name:
##                    if c != " ": s += c
##                while len(s) < 3: s += " "
##                self.shortNameDict[name] = s
##                return s
##            else:
##                s = ""
##                for c in name:
##                    if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ*" or \
##                        ((not "." in name) and (c in "0123456789")):
##                        s += c
##                if len(s) == 0: s = name[:3]
##                else:
##                    while len(s) < 3:  s += " "
##                self.shortNameDict[name] = s[-3:]
##                return s[-3:]

    def prepareLog(self):
        data = []
        for mi in self.world.miList:
            s = self.shortName(mi.fav)
            if s == "   ": print mi.fav
            if isinstance(mi, Induction.InvertMIColl):
                if mi.invert: s = "~"+s
            elif isinstance(mi, Induction.DeceptionDetectionMixin):
                if mi.fav and mi.deceived(mi.fav):
                    s = "*"+s
            data.append(s)
        for d in self.world.non_miList:
            s = " "
            if d in self.world.ultdeceivers:
                s += "u"
            if d in self.world.deceivers:
                s += "d"
            s = (s+"     ")[:4]
            data.append(s)
        self.miData = data
        
    def updateLog(self):
        data = [self.world.round]
        # data.append(self.world.OI.successRate)
        # data.append(0.0)
        for p in self.world.getPredictorList():
            data.append(p.successRate)
        data.extend(self.miData)
#        s2 = ""
#        mi = self.world.miList[0]
#        for p in self.world.non_miList:
#            if mi.deceived(p):
#               s2 += p.name+","
        try:
            self.win.logAppend(self.fmtStr % tuple(data)) #+s2
        except TypeError:
            print self.fmtStr
            print data
            raise AssertionError
            

    def zoom(self, sx1, sy1, sx2, sy2):
        if self.graph == None: return
        if sx1 != sx2 and sy1 != sy2:
            x1, y1 = self.graph.peek(sx1, sy1)
            x2, y2 = self.graph.peek(sx2, sy2)
            if y1 < 0.0: y1 = 0.0
            if y2 > 1.0: y2 = 1.0
            if x1 < 1: x1 = 1
            if x1 >= 1 and x2 >= 1 and y1 >= 0.0 and y1 <= 1.0 and \
               y2 >= 0.0 and y2 <= 1.0:
                x1 = int(x1);  x2 = int(x2)+1
                self.zoomlist = self.zoomlist[0:self.zoomPos+1]
                self.zoomlist.append((x1, y1, x2, y2))
                self.zoomPos = len(self.zoomlist)-1
                self.graph.adjustRange(x1, y1, x2, y2)
                self.win.refresh()

    def zoomIn(self):
        if self.graph == None: return        
        if self.zoomPos < len(self.zoomlist)-1:
            self.zoomPos += 1
            x1, y1, x2, y2 = self.zoomlist[self.zoomPos]
            self.graph.adjustRange(x1, y1, x2, y2)
            self.win.refresh()

    def zoomOut(self):
        if self.graph == None: return        
        if self.zoomPos > 0:
            self.zoomPos -= 1
            x1, y1, x2, y2 = self.zoomlist[self.zoomPos]
            self.graph.adjustRange(x1, y1, x2, y2)
            self.win.refresh()
        else:
            x1, y1, x2, y2 = self.zoomlist[0]
            oldX2 = x2
            if self.win.logScale:  x2 *= 10
            else:  x2 *= 2
            self.zoomlist.insert(0, (x1, y1, x2, y2))
            self.graph.adjustRange(x1, y1, x2, y2)
            self.win.refresh()
            self.calcNdraw(oldX2+1,x2)            

    def resizedCallback(self):
        if self.graph == None: return        
        self.graph.resizedGfx()

    def printGraph(self, dc):
        if self.graph == None: return        
        gfx = wxGfx.Driver(dc)
        oldGfx = self.graph.changeGfx(gfx)
        self.graph.changeGfx(oldGfx)

    
##    def QualityPlot(self):
##        # draw markers
####        density = 20; delta = 0; step = max(1,density/len(self.graph.penOrder))
####        for name in self.graph.penOrder:
####            xvalues = [p[0] for p in self.graph.values[name]]
####            yvalues = [p[1] for p in self.graph.values[name]]
####            xmvals = xvalues[delta::density]
####            ymvals = yvalues[delta::density]
####            delta = (delta+step) % density
####            if name.find("mean") >= 0:
####                style = "k:"
####            elif name.find("OI") >= 0 or name.find("Object") >= 0:
####                style = "w:o"
####            elif name.find("MI") >= 0 or name.find("Meta") >= 0:
####                style = "w:d"
####            else:
####                style = "w:s"
####            pylab.plot(xmvals, ymvals, style)
##            
##        # draw lines
##        for name in self.graph.penOrder:
##            xvalues = [p[0] for p in self.graph.values[name]]
##            yvalues = [p[1] for p in self.graph.values[name]]
##            if name.find("Mean") >= 0:
##    #wenn Name "Mean" enthält            
##                #style = "k-"
##                if name.find("non") >= 0:
##                    style = "k-o"
##                    xvalues = xvalues[5::10]
##                    yvalues = yvalues[5::10]
###fängt bei 5.Wert an, nimmt jeden 10. Punkt           
##                else:
##                    style = "k-s"
##                    xvalues = xvalues[::10]
##                    yvalues = yvalues[::10]
##            elif name.find("MI") >= 0 or name.find("Meta") >= 0:
##                style = "k-"
##            elif name.find("OI") >= 0 or name.find("Object") >= 0:
##                style = "k--"
##            else:
##                style = "k:"
##            pylab.plot(xvalues, yvalues, style)
##
##        # Hier würde er die legende schreiben, die aber verdeckt.
##        # pylab.legend(tuple(self.graph.penOrder))
##        pylab.show()

    def writePostscript(self, fileName):
        """Saves the graph as postscript file."""
        ps = psGfx.Driver()
        oldGfx = self.graph.changeGfx(ps)
        ps.save(fileName)
        self.graph.changeGfx(oldGfx)
        

########################################################################
#
#   Test
#
########################################################################

if __name__ == "__main__":
    sim = Simulation({"Test 1": ("Demonstration of the Meta Inductivist",
                                 [Induction.ObjectInductivist(),
                                  Induction.AmplitudeOscillator(0.3, 0.85),
                                  Induction.MetaInductivist()],
                                 [],
                                 500,
                                 lambda : Induction.getRandomEvent(2.0/3.0)),
                     })

    sim.run()

    
