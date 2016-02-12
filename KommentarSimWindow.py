# -*- coding: cp1252 -*-
#!/usr/bin/python
# Input / Output for the induction simulation

#Kommentar zeigt Verlauf an: Step-Nr. ist Schrittnummer

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

#?? Frage: was müsste man ändern, wenn man zusätzlich (i) Eventfrequency
#(zwecks worldDeception nötig),
# (ii) cond. success rates der non_MIs,  
# ausdruckt? Kann man Buttons einführen? ZB einen Button "Eventfrequency"?
#Einen Button: additional success rates?
#Alternative1: Wenn man das per default hat hat,
#könnte man durch "Strichstärke durchsichtig" das wieder löschen??
#Alternative2: das simulieren durch spezielle Voraussager

#?? Zumindest Grobbeschreibung von SimWindiw wäre nötig. Wo liegt Ausdruckbefehl?
#Vielleicht woanders, zB in "GraphPy"?

from __future__ import generators
import copy, time
# generators: daraus Befehl "yield": , copy: legt Kopien von Objekten an
# "copy.copy" und "copy.deepcopy" (mit allen Referenzen), "time" wird gar nicht benötigt

from wxPython.wx import *
# wxPython: Paket für graphische Benutzeroberfläche; ganz wichtig
# * heisst dass alles daraus importiert wird ohne "wxPython.---"-Vorstring.

from PyPlotter import Gfx, wxGfx, Graph, Colors

#Befehle aus diesen Files unten kann ich mit "Gfx.---", "Graph.----" etc erkennen.
# Gfx in PyPlotterDir enthält ein Graphic Interface, in dem z.B Farben,
# Linienstärken etc. definiert werden.
# wxGfx stellt die Anbindung für das x.Windows-System her.
# Graph zeichnet Kordinatensystemn auf Screen, berechnet Regionen, transformiert es
# zeichnet Punkte ein, usw.
# Colors importiert eine grosse Menge verschiedener Farben.

import Induction  #importiert das Induktionsprogramm


# import pylab
#Hinweis zu """-Auskommentierung: muss richtig eingerückt sein.
#Das macht aus Kommentar eigentlich einen String, kein Kimmentar.
#Kann ausgelesen werden mit Help-Modul
"""Teichnen einen MatLabähnlichen SchwarzweissPlot.
ist nur am InstitutsPC installiert- das ist nun numpy
matplotlib in sitepackages in Lib von Python24 installiert.
Haben beide je über 10 MB.
Die Installations- und deinstallationsprogramme sind
im Hauptordner Python24.

Auch im "SaveImage" Button kann ein png Bild und mit "Postscript" Button ein ps Bild
erzeugt werden.

???? Postscript funktioniert nicht!  
""" 

class SimWindow(wxGfx.Driver, Gfx.Window):
   
#Step2: die Klasse SimWindow wird erzeugt, indem sie initialisiert wird.
    #Dabei werden alle Parameter realisiert, die das Bild und die Menü-Items aufbauen.

    def __init__(self, exampleDict, size=(500, 400),
                 title="wxGraph", app=None):
        if app != None:
            self.app = app
        else:
            self.app = wxPySimpleApp()
            
#Funkitonsvariablen werden auf 0 gesetzt
        self.resizeCallback = lambda:0
        self.zoomCallback = lambda a,b,c,d:0
        self.zoomInCallback = lambda:0
        self.zoomOutCallback = lambda:0
        self.dumpPSCallback = lambda a:0
        self.simCallback = lambda a,b,c,d,e:0
        self.scaleCallback = lambda a:0
        self.drawModeCallback = lambda a:0
        self.sim = None
        self.oldGfxSize = (100, 200)
# alle Examples in exampleDict, baut Menü auf
        self.exampleDict = exampleDict
            
#jetzt folgen Befhele aus wxPython.wx
        self.win = wxFrame(None, -1, title)#, style=
                           #wxSYSTEM_MENU|wxCAPTION|wxMINIMIZE_BOX|
                           #wxNO_FULL_REPAINT_ON_RESIZE)
        self.win.SetSize(size)
        self.menuBar = wxMenuBar()
#Die Menues der gesamten Menuebar werden nacheinander aufgebaut
#ExampleMenue
        menu = wxMenu()
        keys = self.exampleDict.keys()
        keys.sort()
        self.idDict = {}
        id = 1000
        for k in keys:
            id += 1
            item = wxMenuItem(menu, id, k)
            self.idDict[id] = self.exampleDict[k]
            menu.AppendItem(item)
            EVT_MENU(self.win, id, self.OnExample)
#Bei Aufruf des Menuepunktes mit Identität "id" springt er auf "OnExample"       
        self.menuBar.Append(menu, "Examples")
        
#Optionsmenue
        menu = wxMenu()
# Menueitem wird erzeugt:
        self.logItem = wxMenuItem(menu, 2001, "Logging on",
                          "Turn simulation log on."+\
                          "(Slows down the simulation!)", wxITEM_CHECK)
        self.doLogging = True  
#Oben: Per Default doLogging True. Und: "wxITEM_CHeck": man kann auswählen 
#unten: Menueitem wird hinzugefügt
        menu.AppendItem(self.logItem)
        self.logItem.Check(self.doLogging)

        self.bwItem = wxMenuItem(menu, 2003, "Black & White", "",
                                 wxITEM_CHECK)
        self.blackwhite = False
        menu.AppendItem(self.bwItem)    
        #self.hiddenOIItem = wxMenuItem(menu, 2002, "Show Hidden OI","",
        #                               wxITEM_CHECK)
        self.hiddenOI = False
# hiddenOI noch drin, weil später irgendwo nach "hiddenOI" gefragt wird.
#Besser wenn alles zu hiddenOI ganz rauskäme.
        #menu.AppendItem(self.hiddenOIItem)

        self.hardruleItem = wxMenuItem(menu, 2004, "Hardrule", "",
                                       wxITEM_CHECK)
        menu.AppendItem(self.hardruleItem)

        self.deceivedOIItem = wxMenuItem(menu, 2005, "World Deception", "",
                                         wxITEM_CHECK)
        menu.AppendItem(self.deceivedOIItem)
#ausnahmsweise wird korrespondierende Boolesche variable erst in
    #Klasse "Simulation" definiert

        self.meanValueItem = wxMenuItem(menu, 2006, "Show Mean Values", "",
                                        wxITEM_CHECK)
        self.showMeanValues = True
        menu.AppendItem(self.meanValueItem)
        self.meanValueItem.Check(self.showMeanValues)

        self.logScaleItem = wxMenuItem(menu, 2007, "Logarithmic Scale", "",
                                       wxITEM_CHECK)
        self.logScale = False
        menu.AppendItem(self.logScaleItem)

        self.absoluteSuccessItem = wxMenuItem(menu, 2009, "Absolute Success", "",
                                              wxITEM_CHECK)
        self.absoluteSuccess = False
        menu.AppendItem(self.absoluteSuccessItem)

        self.shuffleDrawItem = wxMenuItem(menu, 2008, "Overlapping Graphs Visible", "",
                                          wxITEM_CHECK)
        self.shuffleDraw = False
        menu.AppendItem(self.shuffleDrawItem)
        self.menuBar.Append(menu, "Preferences")

#Nun unten: wenn id-Werte angesprungen werden, werden die in Klasse
# "Simulation" definierten On-Funktionen aufgerufen.
        EVT_MENU(self.win, 2001, self.OnLogging)
        EVT_MENU(self.win, 2002, self.OnHiddenOI)
        EVT_MENU(self.win, 2004, self.OnHardrule)
        EVT_MENU(self.win, 2003, self.OnBlackWhite)
        EVT_MENU(self.win, 2005, self.OnDeceivedOI)
        EVT_MENU(self.win, 2006, self.OnShowMeanValues)
        EVT_MENU(self.win, 2007, self.OnLogScale)
        EVT_MENU(self.win, 2008, self.OnShuffleDraw)
        EVT_MENU(self.win, 2009, self.OnAbsoluteSuccess)

#Menue für Quality Plot  "Extras"
        menu = wxMenu()
        item = wxMenuItem(menu, 3001, "Quality plot of current graph")
        menu.AppendItem(item)
        self.menuBar.Append(menu, "Extras")
        EVT_MENU(self.win, 3001, self.OnQualityPlot)
        
#Fenste kriegt Menue-Bar
        self.win.SetMenuBar(self.menuBar)

        # self.logItem.Check(self.doLogging)  steht schon oben
        #self.hiddenOIItem.Check(self.hiddenOI)
        #self.bwItem.Check(self.blackwhite)
        
# In den folgenden Sizer-Befehlen geht es um ANordnung der Elemente des
#Fensters, nebeneinander, untereinander usw.
        self.mainSizer = wxBoxSizer(wxVERTICAL)

#Das wxNotebook hat zwei Seiten, notebook.gfxPage ist Graphikseite,
# notebook.logPage ist Loggingseite. 
        self.notebook = wxNotebook(self.win, -1, size=size)
        #self.nbSizer = wxNotebookSizer(self.notebook)
        EVT_NOTEBOOK_PAGE_CHANGED(self.notebook, -1, self.OnNotebook)

        self.gfxPage = wxPanel(self.notebook, -1, style=wxNO_BORDER)
        self.notebook.AddPage(self.gfxPage, "Graph")

        self.logPage = wxPanel(self.notebook, -1, style=wxNO_BORDER)
        ffont = wxFont(10, wxMODERN, wxNORMAL, wxNORMAL)
        tAttr = wxTextAttr(wxColour(0,0,0)) #, font = ffont)
        tAttr.SetFont(ffont)        
        self.logbook = wxTextCtrl(self.logPage, -1,
               style=wxTE_READONLY|wxTE_MULTILINE|wxTE_DONTWRAP|wxTE_RICH)
        self.logbook.SetDefaultStyle(tAttr)
        self.notebook.AddPage(self.logPage, "Log")
        
        self.logSizer = wxBoxSizer(wxVERTICAL)
        self.logSizer.Add(self.logbook, 1, wxEXPAND)
        self.logButtonSizer = wxBoxSizer(wxHORIZONTAL)
        btn = wxButton(self.logPage, -1, "Save Log...")
        self.logButtonSizer.Add(btn, 1)
        EVT_BUTTON(btn, -1, self.OnSaveLog)
        self.logSizer.Add(self.logButtonSizer)
        self.logPage.SetAutoLayout(1)
        self.logPage.SetSizer(self.logSizer)
        self.logSizer.Fit(self.logPage)
        self.logSizer.SetSizeHints(self.logPage)

        self.topSizer = wxBoxSizer(wxVERTICAL)
        self.gfxArea = wxWindow(self.gfxPage, -1, size=size)
        self.gfxArea.SetSizeHints(200, 100, 1600, 1200)

        controls = [("< Zoom", self.OnZoomOut),
                    ("Zoom >", self.OnZoomIn),
                    (" ", self.OnNOP),
                    ("Save Image...", self.OnSave),
                    ("Postscript...", self.OnPrint)]

        self.bottomSizer = wxBoxSizer(wxHORIZONTAL)
        for control in controls:
            label, cmd = control
            if label != " ":
                btn = wxButton(self.gfxPage, -1, label)
                self.bottomSizer.Add(btn, 1, wxALIGN_LEFT)
                EVT_BUTTON(btn, -1, cmd)
            else:
                spacer = wxStaticText(self.gfxPage, -1, label)
                self.bottomSizer.Add(spacer, 1, wxALIGN_LEFT)

        self.topSizer.Add(self.gfxArea, 1, wxEXPAND)
        self.topSizer.Add(self.bottomSizer, 0)
        self.gfxPage.SetAutoLayout(1)
        self.gfxPage.SetSizer(self.topSizer)
        self.topSizer.Fit(self.gfxPage)
        self.topSizer.SetSizeHints(self.gfxPage)

        self.mainSizer.Add(self.notebook, 1, wxEXPAND)
        self.win.SetAutoLayout(1)
        self.win.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.win)
        self.mainSizer.SetSizeHints(self.win)
        
        csize = self.gfxArea.GetClientSize()        
        self.buffer = wxEmptyBitmap(csize.width, csize.height)
        dc = wxBufferedDC(None, self.buffer)
        self.app.SetTopWindow(self.win)
        
        self.refreshFlag = True
        self.resizedFlag = False
        self.zoomPivot = (0,0)
        self.dragPen = wxPen(wxColour(0,0,0), 2, wxSHORT_DASH)
        self.dragBrush = wxBrush(wxColour(0,0,0), wxTRANSPARENT)
        
        EVT_PAINT(self.win, self.OnPaint)
#OnIdle das Event wo nichts getan hat
        EVT_IDLE(self.win, self.OnIdle)
        EVT_SIZE(self.win, self.OnSize)

        EVT_LEFT_DOWN(self.gfxArea, self.OnLeftDown)
        EVT_LEFT_UP(self.gfxArea, self.OnLeftUp)
        EVT_MOTION(self.gfxArea, self.OnMotion)
        
        wxGfx.Driver.__init__(self, dc)

        self.win.SetSize(size)
        #self.nbSizer.Fit(self.notebook)
        self.win.Show(1)        
        self.win.Refresh()

#Step3: Hier ist die Initilaisierung der SimWindow Klasse abgeschlossen, und
#weitere Funktionen
#werden nach Bedarf aufgerufen. Die gehören alle zur Klasse SimWindow. 
# Die set---Callback Funktionen werden innerhalb Klasse "Simulation" aufgerufen.
#Sie fragen für Befehle aus "Simulation" bei der Klasse "SimWindow" nach, und
#diese Klsse teilt zugehörige Funktion/Prozedur mit.
#Ist umständlich. -- Hat eigentlich nur Sinn, wenn "SimWindow" mehrere
#SImulationsklasseninstanzen bedienen müsste.


    def setResizeCallback(self, callback):
        self.resizeCallback = callback

    def setZoomCallback(self, zoom, zoomIn, zoomOut):
        self.zoomCallback = zoom
        self.zoomInCallback = zoomIn
        self.zoomOutCallback = zoomOut

    def setPSCallback(self, callback):
        self.dumpPSCallback = callback

    def setSimCallback(self, callback):
        self.simCallback = callback

    def setScaleCallback(self, callback):
        self.scaleCallback = callback
        
    def setDrawModeCallback(self, callback):
        self.drawModeCallback = callback        

    def logAppend(self, text):
        self.logbook.AppendText(text)

    def clearLog(self):
        self.logbook.Clear()

    def OnPaint(self, event):
        self.refreshFlag = True
        event.Skip()

#gedacht ist hier: wenn nichts getan wird, und OnPait refresFlag gesetzt hat,
#wird Fenster neu gezeichnet
    def OnIdle(self, event):
        if self.refreshFlag:
            if self.resizedFlag:
                size = self.gfxArea.GetClientSize()
                if size != self.oldGfxSize:
                    self.buffer = wxEmptyBitmap(size.width, size.height)
                    dc = wxBufferedDC(None, self.buffer)
                    self.changeDC(dc)
                    self.clear()
                    self.resizeCallback()
                    self.oldGfxSize = size
                    self.resizedFlag = False
            dc = wxClientDC(self.gfxArea)
            dc.BeginDrawing()
            dc.Blit(0, 0, self.w, self.h, self.getDC(), 0, 0)
            dc.EndDrawing()
            self.refreshFlag = False

    def refresh(self):
        self.refreshFlag = True
        self.OnIdle(None)

    def quit(self):
        self.win.Close()
        
    def waitUntilClosed(self):
        self.app.MainLoop()
#nachdem Bild aufgebaut, wartet Programm solange bis Example eingegeben wird.

    def OnExample(self, event):
        id = event.GetId()
        apply(self.simCallback, self.idDict[id])
#OnExample ruft "simCallback auf
    
    def OnLogging(self, event):
        if self.logItem.IsChecked():
            self.doLogging = True
        else:
            self.doLogging = False
            self.clearLog()

    def OnHiddenOI(self, event):
        if self.hiddenOIItem.IsChecked():
            self.hiddenOI = True
        else:
            self.hiddenOI = False

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
        self.scaleCallback(self.logScale)
        self.refresh()
        
    def OnShuffleDraw(self, event):
        if self.shuffleDrawItem.IsChecked():
            self.shuffleDraw = True
        else:
            self.shuffleDraw = False
        self.drawModeCallback(self.shuffleDraw)
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

#"NOP" für "no operation"
    def OnNOP(self, event):
        pass

    def OnZoomIn(self, event):
        self.zoomInCallback()

    def OnZoomOut(self, event):
        self.zoomOutCallback()

#dieser Befehl soll Postscript-File herstellen; Menüpunkt
    def OnPrint(self, event):
        fD = wxFileDialog(None, message = "Please select a file name:",
                          wildcard = "*.ps",
                          style =wxSAVE|wxOVERWRITE_PROMPT|wxCHANGE_DIR)
        result = fD.ShowModal()
        if result != wxID_CANCEL:
            fName = fD.GetFilename()
            if fName[-3:] != ".ps": fName = fName + ".ps"
            wxGfx.DumpPostscript(self.win, fName,
                                 self.dumpPSCallback)
        fD.Destroy()
        self.refreshFlag = True

#Menüpunkt png Datei
    def OnSave(self, event):
        fD = wxFileDialog(None, message = "Please select a file name:",
                          wildcard = "*.png",
                          style =wxSAVE|wxOVERWRITE_PROMPT|wxCHANGE_DIR)
        result = fD.ShowModal()
        if result != wxID_CANCEL:
            fName = fD.GetFilename()
            if fName[-4:] != ".png": fName = fName + ".png"
            image = wxImageFromBitmap(self.buffer)
            # wxImage_AddHandler(wxPNGHandler())
            image.SaveFile(fName, wxBITMAP_TYPE_PNG)
        fD.Destroy()
        self.refreshFlag = True

    def OnSaveLog(self, event):
        fD = wxFileDialog(None, message = "Please select a file name:",
                          wildcard = "*.txt",
                          style =wxSAVE|wxOVERWRITE_PROMPT|wxCHANGE_DIR)
        result = fD.ShowModal()
        if result != wxID_CANCEL:
            fName = fD.GetFilename()
            if fName[-4:] != ".txt": fName = fName + ".txt"
            try:
                f = open(fName, "w")
                f.write(self.logbook.GetValue())
                f.close()
            except IOError:
                print "IOError!!!"
        fD.Destroy()        

#Zoomfunktionen mit der Maus
    def OnLeftDown(self, event):
        self.zoomPivot = event.GetPositionTuple()
        self.gfxArea.CaptureMouse()

    def OnLeftUp(self, event):
        if self.gfxArea.HasCapture():
            x2, y2 = event.GetPositionTuple()            
            self.gfxArea.ReleaseMouse()
            dc = wxClientDC(self.gfxArea)
            dc.BeginDrawing()
            dc.Blit(0, 0, self.w, self.h, self.dc, 0, 0)
            dc.EndDrawing()
            x1, y1 = self.zoomPivot
            y1 = self.h-y1; y2 = self.h-y2
            self.zoomCallback(min(x1,x2), min(y1,y2),
                              max(x1,x2), max(y1,y2))

    def OnMotion(self, event):
        if event.Dragging() and event.LeftIsDown():
            dc = wxClientDC(self.gfxArea)
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

    def OnQualityPlot(self, event):
        self.sim.QualityPlot()
        

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
    

#Step4: Unterklasse "Simulation" wird initialisiert. "setSimCallback" liest
#das jeweilige Example ein, wenn es aufgerufen wird.
# self.Sim(Parameters) führt Simulation durch  
class Simulation:
    def __init__(self, exampleDict, winTitle = "Induction Simulation",
                 eventFunction = lambda : getRandomEvent(2.0/3.0)):   
        self.win = SimWindow(exampleDict, size=(950,700), title=winTitle)
        self.win.sim = self
        self.win.setResizeCallback(self.resizedCallback)
        self.win.setZoomCallback(self.zoom, self.zoomIn, self.zoomOut)
        self.win.setPSCallback(lambda dc: self.printGraph(self, dc))
        self.win.setSimCallback(lambda t,p,l,r,e: self.Sim(t,p,l,r,e))
        self.win.setScaleCallback(self.changeScale)
        self.win.setDrawModeCallback(self.changeDrawMode)
        self.graph = Graph.Cartesian(self.win, 1, 0.0, 1000, 1.0,
                                     "Graph", "Round (time)", "Success Rate",
                                     styleFlags = \
                                     Graph.DEFAULT_STYLE) 
        self.shortNameDict = {}
        self.worldDeception = False


    def run(self):
        self.win.waitUntilClosed()
#wartet solange bis das Fenster wieder geschlossen wird.

#Step5: durch  "OnExample" wird die Klasse SetSimCallback und dann Sim aufgerufen:
# durch oben: self.win.setSimCallback(lambda t,p,l,r,e: self.Sim(t,p,l,r,e))
    def Sim(self, title, predictorList, penList = [], rounds = 500,
            eventFunction = lambda : Induction.getRandomEvent(2.0/3.0)):
# die Axen wird entsprechend den Menüvorgaben angepasst
        self.graph.reset(1, 0.0, rounds, 1.0)
        if self.win.absoluteSuccess:
            self.graph.setLabels(yaxis="Absolute Success")
        else:
            self.graph.setLabels(yaxis="Success Rate")
        self.graph.setTitle(title)
        self.zoomlist = [(1, 0.0, rounds, 1.0)]
        self.zoomPos = 0
        self.predictorList = copy.deepcopy(predictorList)
#nun wird die Klasse World aus Induction.py initialisiert bzw. erzeugt; siehe Step 6
        self.world = Induction.World(eventFunction)
#nun wird jeder predictor der predictorList aus dem Example bei der Klasse world
        #angemeldet, das führt zu Step 6 in Induction.py
        for predictor in self.predictorList:
            self.world.register(predictor)
        if self.worldDeception:
            self.world.worldDeceived = self.world.miList[0]
# Hier oben bei [0] moegliche Veraenderung des Betrogenen MI eintragen
#"0" ist die erste Stelle der miList; der wird betrogen, falls
# worldDeception an ist

#Step7:  nun werden den predictors die entprechenden zeichenfarben zugeordnet
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
        #if self.win.hiddenOI:
        #    self.graph.addPen(str(self.world.OI), pen)

        Np = len(self.world.getPredictorList())
        Nmi = len(self.world.miList)
        Nn_mi = len(self.world.non_miList)
        
#Step7-Fortsetzung: Hier wird die Legende der Logging-Ausgabe erzeugt,
#falls Logging an ist. Danach folgt Mittelwertfarbeneinstellung.
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
# p1 ist der Farbenwert von non_miMean; und p2 der von miMean
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

#Option 6: PrintEventfrequency
# p = Gfx.Pen((0.8, 0.5, 0.0), lineWidth=Gfx.MEDIUM,  \
# linePattern=Gfx.CONTINUOUS)
# self.graph.addPen("Event Frequency", p)   

#Step8: Jetzt erst beginnt die HAUPTschleife
        self.calcNdraw(1, rounds)
# hier ist die Definition der Klasse "Sim" erst zu Ende.

# im folgenden: a ist 1, und b ist rounds. 
    def calcNdraw(self, a, b):
        last_xPixel = -1
# eigentliche Hauptschleife: n, die Rundenzahl, geht alle Werte zwischen 1 und
# rounds durch   ?? warum steht hier b+1: weil "range" bis (b-1) geht.
        for n in range(a, b+1):
            xPixel = self.graph._scaleX(n)
#self.graph_scaleX(n) (n=Rundenzahl) kannein neuer oder noch der alte Pixel sein.
#ein neuer Pixel wird nur eingezeichnet aufgrund neuen Rundenwertes, wenn der
#Rundenwert einen ganzen Pixel weiter ist.
#das ist für alle predictors dieselbe Position an der x-Achse
            if xPixel > last_xPixel:
                last_xPixel = xPixel
                plotFlag = True
            else:  plotFlag = False
#Option 5: CHAOSKORREKTUR:
#extrem steile Fluktuationen könnten dadurch evtl. nicht eingezeichnet werden.
#wenn man das nicht will, setzt man "poltFlag" auch unter "else" auf "True".

            self.prepareLog()        
# self.prepareLog() kommt vor nextRound, weil es die deceiver-Zustände notiert
#damit in selber zeile wo "d" steht dieser auch kein Favorit ist

#Step9: das folgende führt zu Step9 in Induction.py. "self.world.nextRound
#wird aufgerunden, dh neue Runde wird durchsimuliert

            self.world.nextRound() 
            #if self.win.hiddenOI:
            #    pList = self.world.predictorList+[self.world.OI]
            #else:
#nun werden am Anschluss der neuen Runde die neuen Werte eingezeichnet
# sofern neuer Wert ein Pixel vom alten entfernt ist. In "Mittelwertberechnung"
#wird zusätzlich der neue Mittelwert eingetragen.

            pList = self.world.getPredictorList()
            if plotFlag:
                for predictor in pList:
                    if self.win.absoluteSuccess:
                        self.graph.addValue(str(predictor), n, \
                                            predictor.success)                        
                    else:
                        self.graph.addValue(str(predictor), n, \
                                            predictor.successRate)
#Option 6:
#                 self.graph.addValue("Event Frequency", n, \
#                                            self.world.relFrequency) 
#self.graph.addValue(str(predictor), n, predictor.successRate) trägt für Namen
# "str(predictor)" x-Wert n (=round) und y-Wert p--.successRate ein

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
        
        
#Damit ist Verlauf des Programs zu Ende. Alle weiteren Steps ab Step9 in Induction.py
#Rest sind Hilfsfunktionen für das Einzeichnen der Werte
    def changeScale(self, logScale):
        if logScale:
            self.graph.setStyle(self.graph.styleFlags|Graph.LOG_X, redraw=True)
        else:
            self.graph.setStyle(self.graph.styleFlags & ~Graph.LOG_X, redraw=True)
            
#Hiert unten wird Reihenfolge der Piixelpunkte von übereinanderliegenden Werten
# verschiedener predictors vertauscht, sodass in Graphik alle zu sehen
#sind
    def changeDrawMode(self, shuffleDraw):
        if shuffleDraw:
            self.graph.setStyle(self.graph.styleFlags|Graph.SHUFFLE_DRAW, redraw=True)
        else:
            self.graph.setStyle(self.graph.styleFlags & ~Graph.SHUFFLE_DRAW, redraw=True)
        
    def shortName(self, predictor):
        if predictor:
            return predictor.shortName(3)
        else: return " - "

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

    
    def QualityPlot(self):
        # draw markers
##        density = 20; delta = 0; step = max(1,density/len(self.graph.penOrder))
##        for name in self.graph.penOrder:
##            xvalues = [p[0] for p in self.graph.values[name]]
##            yvalues = [p[1] for p in self.graph.values[name]]
##            xmvals = xvalues[delta::density]
##            ymvals = yvalues[delta::density]
##            delta = (delta+step) % density
##            if name.find("mean") >= 0:
##                style = "k:"
##            elif name.find("OI") >= 0 or name.find("Object") >= 0:
##                style = "w:o"
##            elif name.find("MI") >= 0 or name.find("Meta") >= 0:
##                style = "w:d"
##            else:
##                style = "w:s"
##            pylab.plot(xmvals, ymvals, style)
            
        # draw lines
        for name in self.graph.penOrder:
            xvalues = [p[0] for p in self.graph.values[name]]
            yvalues = [p[1] for p in self.graph.values[name]]
            if name.find("Mean") >= 0:
    #wenn Name "Mean" enthält            
                #style = "k-"
                if name.find("non") >= 0:
                    style = "k-o"
                    xvalues = xvalues[5::10]
                    yvalues = yvalues[5::10]
#fängt bei 5.Wert an, nimmt jeden 10. Punkt           
                else:
                    style = "k-s"
                    xvalues = xvalues[::10]
                    yvalues = yvalues[::10]
            elif name.find("MI") >= 0 or name.find("Meta") >= 0:
                style = "k-"
            elif name.find("OI") >= 0 or name.find("Object") >= 0:
                style = "k--"
            else:
                style = "k:"
            pylab.plot(xvalues, yvalues, style)

        # Hier würde er die legende schreiben, die aber verdeckt.
        # pylab.legend(tuple(self.graph.penOrder))
        pylab.show()
    

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

    
