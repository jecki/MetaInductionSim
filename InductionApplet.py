# -*- coding: cp1252 -*-
#!/usr/bin/jython
import copy, pawt, java # , re
from javax.swing import JApplet, JLabel, JList, JTextArea, JButton, JRadioButton, \
                        ButtonGroup, JTextPane, JPanel, JOptionPane, \
                        ListSelectionModel, DefaultListModel
from javax.swing.event import ListSelectionListener, ListSelectionEvent
from java.awt import Container, Canvas, BorderLayout, FlowLayout, GridLayout, \
                     Font, Color, Dimension
from java.util import regex
from PyPlotter import awtGfx, Graph, Gfx, Colors
import Induction


###############################################################################
#
# Flags: edit these to change the behaviour of the simulation
#
###############################################################################

SHOW_MI_MEAN     = False
SHOW_NON_MI_MEAN = False


###############################################################################
#
# utility functions and variables
#
###############################################################################

def bright(c):
    brightness = c[0]**2 + c[1]**2 + c[2]**2
    return brightness > 0.4

redPens = [Gfx.Pen(c) for c in filter(bright,filter(Colors.RedFilter, Colors.colors))]
bluePens = [Gfx.Pen(c) for c in filter(bright,filter(Colors.BlueFilter, Colors.colors))]
greenPens = [Gfx.Pen(c) for c in filter(bright,filter(Colors.GreenFilter, Colors.colors))]
yellowPens = [Gfx.Pen(c) for c in filter(bright,filter(Colors.YellowFilter, Colors.colors))]
emptyPens = [Graph.DONT_DRAW_PEN]*10

#def ProxyPenGenerator(penList=[]):
#    for pen in penList:
#        yield pen
#    if penList != []: print "Warning: pen list seems to be too short!"
#    for c in Colors.colors:
#        yield Gfx.Pen(c)

class RunAsThread(java.lang.Thread):
    def __init__(self, procedure):
        self.procedure = procedure
        java.lang.Thread.__init__(self)

    def run(self):
        self.procedure()

def re_sub(pattern, replacement, txt):
    """Replaces 'pattern' with 'replacement' in 'txt'."""
    # for some reason the java security managar does not accept module 're'
    # return re.sub("[ \\n]+", " ", txt)
    pattern = regex.Pattern.compile(pattern)
    matcher = pattern.matcher(txt)
    return matcher.replaceAll(replacement)


###############################################################################
#
# list of examples
#
###############################################################################

exampleList = {}
exampleList["A: MI Demonstration"]  =  \
    ("Example 01(MI): MI + Forecasters",
     [Induction.DelayedForecaster(0.7, 40, "Forecaster 1 (success; delay)"),
      Induction.ForecasterFromBottom(0.90, "Forecaster 2 (success; recovers from zero)"),
      Induction.MetaInductivist("Meta-Inductivist"),
      Induction.ObjectInductivist("Object-Inductivist")],
     bluePens[:2] + redPens[:1] + greenPens,
     500,
     lambda : Induction.getRandomEvent(2.0/3.0),
     """ "MI Demonstration" demonstrates how a meta-inductivist works:
     The meta-inductivist simply follows the predictor that had the highest
     success rate so far. This predictor is called its "favorite". If another
     predictor becomes better than the favorite, the meta-inductivists choses this
     predictor as its new favorite.
     """)
exampleList["B: Amp. Oscillators"] = \
    ("Example 02(MI): MI + Amplitude-Oscillator + OI",
     [Induction.AmplitudeOscillator(0.3, 0.85, "AmpOsc"),
      Induction.MetaInductivist("Meta-Inductivist"),
      Induction.ObjectInductivist("Object-Inductivist")],
     bluePens[:1] + redPens[:1] + greenPens,
     500,
     lambda : Induction.getRandomEvent(2.0/3.0),
     """Hier noch eine Beschreibung einfügen...
     """)
exampleList["C: Systematic Oscillator"] = \
    ("Example 03(MI): MI + 1 Systematic Oscillator + OI",
     [Induction.SystOscillator("SystOscillator"),
     Induction.MetaInductivist("Meta-Inductivist"),
      Induction.ObjectInductivist("Object-Inductivist")],
     bluePens[:1] + redPens[:1] + greenPens, 500,
     lambda : Induction.getRandomEvent(2.0/3.0),
     """An dieser Stelle sollten ein par nette Zeilen zur
     Erklärung für den Nutzer stehen...
     """)


###############################################################################
#
#  the graphical user interface (java applet)
#
###############################################################################

class GraphCanvas(Canvas):
    def __init__(self):
        self.applet = None
    def setApplet(self, applet):
        self.applet = applet
    def paint(self, g):
        if self.applet != None: self.applet.refresh();

class InductionApplet(JApplet):
    def init(self):
        global exampleList
        self.thinFont = Font("Dialog", 0, 10)

        self.pane = self.getContentPane()
        self.examples = exampleList.keys()
        self.examples.sort()
        self.exampleSelector = JList(self.examples, valueChanged=self.valueChanged)
        self.exampleSelector.setSelectionMode(ListSelectionModel.SINGLE_SELECTION)
        self.exampleSelector.setLayoutOrientation(JList.VERTICAL)
        self.exampleSelector.setPreferredSize(Dimension(150,500))
        self.exampleSelector.setBackground(Color(0.95, 0.95, 0.98))
        self.exampleSelector.setFont(self.thinFont)

        self.centerPanel = JPanel(BorderLayout())
        self.canvas = GraphCanvas()
        self.canvas.setApplet(self)
        self.buttonRow = JPanel(FlowLayout())
        self.backButton = JButton("<", actionPerformed = self.backAction)
        self.backButton.setFont(self.thinFont)
        self.continueButton = JButton("continue >",
                                      actionPerformed=self.continueAction)
        self.continueButton.setFont(self.thinFont)
        self.scaleGroup = ButtonGroup()
        self.linearButton = JRadioButton("linear scale",
                                         actionPerformed=self.linearAction)
        self.linearButton.setSelected(True)
        self.linearButton.setFont(self.thinFont)
        self.logarithmicButton = JRadioButton("logarithmic scale",
                                      actionPerformed=self.logarithmicAction)
        self.logarithmicButton.setFont(self.thinFont)
        self.aboutButton = JButton("About...",
                                   actionPerformed=self.aboutAction)
        self.aboutButton.setFont(self.thinFont)
        self.scaleGroup.add(self.linearButton)
        self.scaleGroup.add(self.logarithmicButton)
        self.buttonRow.add(self.backButton)
        self.buttonRow.add(self.continueButton)
        self.buttonRow.add(JLabel(" "*5))
        self.buttonRow.add(self.linearButton)
        self.buttonRow.add(self.logarithmicButton)
        self.buttonRow.add(JLabel(" "*20));
        self.buttonRow.add(self.aboutButton)
        self.centerPanel.add(self.canvas, BorderLayout.CENTER)
        self.centerPanel.add(self.buttonRow, BorderLayout.PAGE_END)

        self.helpText = JTextPane()
        self.helpText.setBackground(Color(1.0, 1.0, 0.5))
        self.helpText.setPreferredSize(Dimension(800,80))
        self.helpText.setText(re_sub("[ \\n]+", " ", """
        Please select one of the examples in the list on the left!
        """))
        self.pane.add(self.exampleSelector, BorderLayout.LINE_START)
        self.pane.add(self.centerPanel, BorderLayout.CENTER)
        self.pane.add(self.helpText, BorderLayout.PAGE_END)
        self.graph = None
        self.simulation = None
        self.touched = ""
        self.selected = ""
        self.gfxDriver = None

    def start(self):
        self.gfxDriver = awtGfx.Driver(self.canvas)
        #self.gfxDriver.setAntialias(True)
        if self.gfxDriver.getSize()[0] < 200:  # konqueror java bug work around
            self.gfxDriver.w = 650
            self.gfxDriver.h = 380
        self.graph = Graph.Cartesian(self.gfxDriver, 1, 0.0, 1000, 1.0,
                                     title="Results",
                                     xaxis="Rounds", yaxis="Success Rate")

    def stop(self):
        pass

    def destroy(self):
        pass

    def refresh(self):
        if self.graph != None: self.graph.redraw()

    def valueChanged(self, e):
        global exampleList
        newSelection = self.examples[self.exampleSelector.getSelectedIndex()]
        if newSelection != self.touched:
            self.touched = newSelection
            text = re_sub("[ \\n]+", " ", exampleList[self.touched][-1])
            self.helpText.setText(text)
        if not e.getValueIsAdjusting() and newSelection != self.selected:
            self.selected = newSelection
            smallFontPen = copy.copy(Gfx.BLACK_PEN)
            smallFontPen.fontSize = Gfx.SMALL
            ex = exampleList[self.selected]
            myStyleFlags = self.graph.styleFlags
            if self.simulation != None:  self.simulation.stop()
            self.gfxDriver.resizedGfx() # konqueror 3.5.5 java bug workaround
            self.graph = Graph.Cartesian(self.gfxDriver, 1, 0.0, ex[3], 1.0,
                                         title=ex[0],
                                         xaxis="Rounds", yaxis="Success Rate",
                                         styleFlags = myStyleFlags,
                                         axisPen = smallFontPen,
                                         captionPen = smallFontPen)
            self.zoomFrame = [(1, 0.0, ex[3], 1.0)]
            self.simulation = Simulation(self.graph, ex[1], ex[2], ex[3], ex[4])
            RunAsThread(self.simulation.simulation).start()

    def determineCurrentZoomFrame(self):
        i = 0
        for zf in self.zoomFrame:
            if self.graph.x2 <= zf[2]: break
            i += 1
        return i

    def backAction(self, e):
        if self.simulation == None:  return
        wasRunning = self.simulation.isRunning
        self.simulation.stop()
        if wasRunning or len(self.zoomFrame) <= 1:  return
        zi = self.determineCurrentZoomFrame()
        if zi > 0 and zi < len(self.zoomFrame):
            x1, y1, x2, y2 = self.zoomFrame[zi-1]
            self.graph.adjustRange(x1, y1, x2, y2)

    def continueAction(self, e):
        if self.simulation == None:  return
        wasRunning = self.simulation.isRunning
        self.simulation.stop()
        zi = self.determineCurrentZoomFrame()
        if zi == len(self.zoomFrame)-1:
            if wasRunning or self.simulation.world.round == self.zoomFrame[zi][2]:
                if self.graph.styleFlags & Graph.LOG_X == 0:
                    self.simulation.rounds *= 2
                else:
                    self.simulation.rounds *= 10
                self.zoomFrame.append((1, 0.0, self.simulation.rounds, 1.0))
                self.graph.adjustRange(1, 0.0, self.simulation.rounds, 1.0)
            RunAsThread(self.simulation.simulation).start()
        else:
            x1, y1, x2, y2 = self.zoomFrame[zi+1]
            self.graph.adjustRange(x1, y1, x2, y2)

    def linearAction(self, e):
        if self.graph != None and (self.graph.styleFlags & Graph.LOG_X) != 0:
            if self.simulation != None:  self.simulation.stop()
            self.graph.setStyle(self.graph.styleFlags & ~Graph.LOG_X, redraw=True)
            if self.simulation != None:
                RunAsThread(self.simulation.simulation).start()

    def logarithmicAction(self, e):
        if self.graph != None and (self.graph.styleFlags & Graph.LOG_X) == 0:
            if self.simulation != None:  self.simulation.stop()
            self.graph.setStyle(self.graph.styleFlags | Graph.LOG_X, redraw=True)
            if self.simulation != None:
                RunAsThread(self.simulation.simulation).start()

    def aboutAction(self, e):
        aboutText = """Induction Applet v. 0.1

        (c) 2007 University of Düsseldorf

        Authors: Gerhard Schurz, Eckhart Arnold
        """
        aboutText = re_sub(" +", " ", aboutText)
        JOptionPane.showMessageDialog(self.getContentPane(), aboutText)


###############################################################################
#
# the simulation
#
###############################################################################

class Simulation:
    def __init__(self, graph, predictorList, penList = [], rounds = 500,
            eventFunction = lambda : Induction.getRandomEvent(2.0/3.0)):
        self.graph = graph
        self.rounds = rounds
        self.predictorList = copy.deepcopy(predictorList)
        self.world = Induction.World(eventFunction)
        for predictor in self.predictorList:
            self.world.register(predictor)
        penBox = copy.copy(penList)
        for predictor in self.predictorList:
            pen = penBox[0]; del penBox[0]
            pen.lineWidth = Gfx.MEDIUM
            self.graph.addPen(str(predictor), pen, updateCaption = False)
        if SHOW_MI_MEAN:
            pen = Gfx.Pen((0.0, 0.0, 0.0), lineWidth=Gfx.THICK,
                          linePattern=Gfx.CONTINUOUS)
            self.graph.addPen("miMean", pen, updateCaption = False)
        if SHOW_NON_MI_MEAN:
            pen = Gfx.Pen((0.3, 0.0, 0.6), lineWidth=Gfx.THICK,
                          linePattern=Gfx.CONTINUOUS)
            self.graph.addPen("non_miMean", pen, updateCaption = False)
        self.graph.redrawCaption()
        self.interrupt = False
        self.isRunning = False
        self.last_xPixel = -1

    def simulation(self):
        self.isRunning = True
        if self.world.round >= 1:
            self.last_xPixel = self.graph._scaleX(self.world.round)
        else: self.last_xPixel = -1
        while not self.interrupt and self.world.round < self.rounds:
            self.nextRound()
        self.isRunning = False
        self.interrupt = False

    def nextRound(self):
        self.world.nextRound()
        xPixel = self.graph._scaleX(self.world.round)
        if xPixel > self.last_xPixel:
            self.last_xPixel = xPixel
            predictorList = self.world.getPredictorList()
            for predictor in predictorList:
                self.graph.addValue(str(predictor), self.world.round,
                                    predictor.successRate)
            if SHOW_MI_MEAN:
                self.graph.addValue("miMean", self.world.round,
                                    self.world.miMean)
            if SHOW_NON_MI_MEAN:
                self.graph.addValue("non_miMean", self.world.round,
                                    self.non_miMean)
            # if self.world.round % ((b-a) / 10) == 0:  self.win.refresh()

    def stop(self):
        self.interrupt = True
        while self.interrupt and self.isRunning:
            pass
        self.interrupt = False

###############################################################################
#
# for testing purposes this jython file can also be run as standalone
# program outside a web-page
#
###############################################################################

if __name__ == "__main__":
    applet = InductionApplet()
    pawt.test(applet, size=(800,500))
    applet.start()
    #applet.refresh()

