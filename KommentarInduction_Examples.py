#!/usr/bin/python
# -*- encoding: UTF-8 -*-

# Beispiele für induktive Prognosespiele

#Kommentare: #Step_i ist Schritt i im Programmablauf

import SimWindow, Induction
from PyPlotter import Gfx, Graph, Colors
#Importiert Module. Siehe Schreibung in SimWindow


def bright(c):
    brightness = c[0]**2 + c[1]**2 + c[2]**2
    return brightness > 0.4

redPens = [Gfx.Pen(c) for c in filter(bright,filter(Colors.RedFilter, Colors.colors))]
bluePens = [Gfx.Pen(c) for c in filter(bright,filter(Colors.BlueFilter, Colors.colors))]
greenPens = [Gfx.Pen(c) for c in filter(bright,filter(Colors.GreenFilter, Colors.colors))]
yellowPens = [Gfx.Pen(c) for c in filter(bright,filter(Colors.YellowFilter, Colors.colors))]
emptyPens = [Graph.DONT_DRAW_PEN]*10

exampleList = {}

#Die Beispiele folgen der Klasse "Sim(Parameter", nämlich:
# def Sim(self, title, predictorList, penList = [], rounds = 500,
# eventFunction = lambda : Induction.getRandomEvent(2.0/3.0)).
#eventFunktion ist per Default voreingestellt. Rounds auch.
#Das in "[ ... ]" nach "exampleList" ist die Bezeichnung des Menüpunktes.
#Danach kommt die Überschrift("title").
# predictorList wird neu bestimmt; ebenfalls Farben

#Generell kommen zuerst die Forecasters in Farbentönen blau, dann die MIs in
#Farbentönen rot; dann OI in grün
#bei den Schwarzweisstönen sind die Forecasters dicker und grau;
#die MIs und der OI dünn und schwärzer

#Die Buttons Overlap Graphs visible und logarithmic scale schalten direkt um
#die Buttons absoluteSuccess, LoggingOn, Hardrule und ShowMeanValues müssen
#neu simuliert werden.


exampleList["01(MI): MI + Forecasters"]  =  \
    ("Example 01(MI): MI + Forecasters",
     [Induction.DelayedForecaster(0.7, 40, "Forecaster 1 (success; delay)"),
      Induction.ForecasterFromBottom(0.90, "Forecaster 2 (success; recovers from zero)"),
      Induction.MetaInductivist("Meta-Inductivist"),
      Induction.ObjectInductivist("Object-Inductivist")],
     bluePens[:2] + redPens[:1] + greenPens,
     500,
     lambda : Induction.getRandomEvent(2.0/3.0))
#WorldDeception wirkt sich hier kaum aus; nur OI oszilliert dann; wenn er fav ist,
#sagt r falsch voraus.Wenn MI auf Forecasters setzt, passiert gar nichts.


exampleList["02(MI): MI + Amplitude-Oscillator + OI"] = \
    ("Example 02(MI): MI + Amplitude-Oscillator + OI",
     [Induction.AmplitudeOscillator(0.3, 0.85, "AmpOsc"),
      Induction.MetaInductivist("Meta-Inductivist"),
      Induction.ObjectInductivist("Object-Inductivist")],
     bluePens[:1] + redPens[:1] + greenPens,
     500,
     lambda : Induction.getRandomEvent(2.0/3.0))
#Worlddeception bewirkt hier, dass OI mit AmplitudeOscillator mitwandert; weder
# höher wird (denn dann fav), noch niedriger (dann nonfav).

exampleList["03(MI): MI + 1 Systematic Oscillator + OI"] = \
    ("Example 03(MI): MI + 1 Systematic Oscillator + OI",
     [Induction.SystOscillator("SystOscillator"),
     Induction.MetaInductivist("Meta-Inductivist"),
      Induction.ObjectInductivist("Object-Inductivist")],
     bluePens[:1] + redPens[:1] + greenPens, 500,
     lambda : Induction.getRandomEvent(2.0/3.0))
#WorldDeception senkt hier MI-Rate auf 0, weil dann sowohl OI wie SystOsc betrügt.
#SystOsc ist ja ein fast-systematischer Deceiver; der MI-verhalten vorausberechnet,
#und sich zurückfallen lät, sobald er MI-Fav ist.


# minimal period coupled oscillators
# OI stört hier
exampleList["04(MI): MI + 2 Systematic Oscillators"] = \
    ("Example 04(MI): MI + 2 Systematic Oscillators",
     [Induction.SystOscillator("SystOscillator 1"),
     Induction.SystOscillator("SystOscillator 2"),
     Induction.MetaInductivist("Meta-Inductivist"),
      #Induction.ObjectInductivist("OI")
      ],
     bluePens[:2] + redPens[:1] + greenPens,500,
     lambda : Induction.getRandomEvent(2.0/3.0))

# minimal period coupled oscillators
# OI stört hier
exampleList["05(eMI): epsilonMI + 2 Systematic Oscillators"] = \
    ("Example 05(eMI): epsilonMI + 2 Systematic Oscillators",
     [Induction.SystOscillator("SystOscillator 1"),
     Induction.SystOscillator("SystOscillator 2"),
     Induction.EpsilonMetaInductivist(name="epsilonMI"),
      #Induction.ObjectInductivist("OI")
      ],
     bluePens[:2] + redPens[:1] + greenPens, 500,
     lambda : Induction.getRandomEvent(2.0/3.0))
#worldDeception bewirkt hier, dass eMI immer von unten kommt.
#Denn zuerst macht er randomguess und wird von events betrogen.
#Analoges gilt für Beispiele 06 und 07


#Deceiver
exampleList["06(eMI): epsilonMI + 1 Deceiver + OI"] = \
    ("Example 06(eMI): epsilonMI + 1 Deceiver + OI",
     [Induction.Spy("Deceiver 1"),
      Induction.EpsilonMetaInductivist(name="epsilonMI"),
      Induction.ObjectInductivist("OI")],
     bluePens[:1] + redPens[:1] + greenPens, 500,
     lambda : Induction.getRandomEvent(2.0/3.0))     
     
#Deceivers
# OI stört hier nicht (deceivers über OI)
exampleList["07(eMI): epsilonMI + 4 Deceivers"] = \
    ("Example 07(eMI): epsilonMI + 4 Deceivers",
    [Induction.Spy("Deceiver 1"),
     Induction.Spy("Deceiver 2"),
    Induction.Spy("Deceiver 3"),
    Induction.Spy("Deceiver 4"),
     Induction.EpsilonMetaInductivist(name="epsilonMI"),
     Induction.ObjectInductivist("OI")],
    bluePens[:4] + redPens[:1] + greenPens, 500,
     lambda : Induction.getRandomEvent(2.0/3.0))


# OI stört hier nicht (deceivers über OI)
exampleList["08(InvMI): 5 inverted eMIs + 5 InvMI-Deceivers"] = \
    ("Example 08(InvMI): 5 inverted eMIs + 5 InvMI-Deceivers",
     [Induction.InvMIDeceiver("Deceiver 1"),
      Induction.InvMIDeceiver("Deceiver 2"),
      Induction.InvMIDeceiver("Deceiver 3"),
      Induction.InvMIDeceiver("Deceiver 4"),
      Induction.InvMIDeceiver("Deceiver 5"),
      Induction.InvertMIColl(name="Meta-Inductivist"),
      Induction.InvertMIColl(name="Meta Inductivist"),
      Induction.InvertMIColl(name="Meta Inductivist"),
      Induction.InvertMIColl(name="Meta Inductivist"),
      Induction.InvertMIColl(name="Meta Inductivist"),
      Induction.ObjectInductivist("OI")
      ],
      bluePens[:5] + redPens[:5] + greenPens, 500,
     lambda : Induction.getRandomEvent(2.0/3.0))

#Deceivers
# OI stört hier nicht (deceivers liegen über OI)
exampleList["09(NeutMI,=): neutralizing MIs + equal number of deceivers"] = \
    ("Example 09(NeutMI,=): neutralizing MIs + equal number of deceivers",
     [Induction.Spy("Deceiver 1"),
      Induction.Spy("Deceiver 2"),
      Induction.Spy("Deceiver 3"),
      Induction.Spy("Deceiver 4"),
      Induction.Spy("Deceiver 5"),
      Induction.PunishMIColl(name = "MI"),
      Induction.PunishMIColl(name = "MI"),
      Induction.PunishMIColl(name = "MI"),
      Induction.PunishMIColl(name = "MI"),
      Induction.PunishMIColl(name = "MI"),
      #Induction.ObjectInductivist("OI")
      ],
      bluePens[:5] + redPens[:5] + greenPens[:1],500,
     lambda : Induction.getRandomEvent(2.0/3.0))


exampleList["10(NeutMI,>): neutralizing MIs + less deceivers"] = \
    ("Example 10(NeutMI,>): neutralizing MIs + less deceivers",
     [Induction.Spy("Deceiver 1"),
      Induction.Spy("Deceiver 2"),
      Induction.Spy("Deceiver 3"),
      Induction.Spy("Deceiver 4"),
      Induction.Spy("Deceiver 5"),
      Induction.PunishMIColl(name = "MI"),
      Induction.PunishMIColl(name = "MI"),
      Induction.PunishMIColl(name = "MI"),
      Induction.PunishMIColl(name = "MI"),
      Induction.PunishMIColl(name = "MI"),
      Induction.PunishMIColl(name = "MI"),
      #Induction.ObjectInductivist("OI"),
      ],
     bluePens[:5] + redPens[:6] + greenPens, 500,
     lambda : Induction.getRandomEvent(2.0/3.0))

exampleList["11(NeutMI,<): neutralizing MIs + more deceivers"] = \
    ("Example 11(NeutMI,<): neutralizing MIs + more deceivers",
     [Induction.Spy("Deceiver 1"),
      Induction.Spy("Deceiver 2"),      
      Induction.Spy("Deceiver 3"),
      Induction.Spy("Deceiver 4"),
      Induction.Spy("Deceiver 5"),
      Induction.Spy("Deceiver 6"),
      Induction.PunishMIColl(name = "MI 1"),
      Induction.PunishMIColl(name = "MI 2"),
      Induction.PunishMIColl(name = "MI 3"),
      Induction.PunishMIColl(name = "MI 4"),
      Induction.PunishMIColl(name = "MI 5"),
      #Induction.ObjectInductivist("OI"),
      ],
     bluePens[:6] + redPens[:5] + greenPens, 500,
     lambda : Induction.getRandomEvent(2.0/3.0))

# Hier macht OI etwas aus
exampleList["12(NeutMI): neutralizing MIs + AntiPunishDeceivers (equal numer)"] = \
    ("Example 12(NeutMI): neutralizing MIs + AntiPunishDeceivers (equal numer)",
     [Induction.AntiPunishDeceiver("AntiPun 1"),
      Induction.AntiPunishDeceiver("AntiPun 2"),
      Induction.AntiPunishDeceiver("AntiPun 3"),
      Induction.AntiPunishDeceiver("AntiPun 4"),
      Induction.AntiPunishDeceiver("AntiPun 5"),
      Induction.PunishMIColl(name = "MI 1"),
      Induction.PunishMIColl(name = "MI 2"),
      Induction.PunishMIColl(name = "MI 3"),
      Induction.PunishMIColl(name = "MI 4"),
      Induction.PunishMIColl(name = "MI 5"),
      #Induction.ObjectInductivist("OI"),
      ],
     bluePens[:5] + redPens[:5] + greenPens, 500,
     lambda : Induction.getRandomEvent(2.0/3.0))
#Hinweise:  im Logging wird sowohl d-Status(deceived) wie u-Status (ultdeceived)
# ausgegeben. NAch kurzer Zeit sind alle A-P-deceivers im Status u; spielt hier aber
#keine Rolle; sie wechselnd mal im Status d und mal nicht. Sind sie nicht im Status d,
#setzen die MIs auf die besseren und sind daher besser.
#Die MIs mit höherer Numemr setzen häufiger auf APDeceivers im non-d Status. In dem Status
#deceiven sie aber immer in nächster Runde. Daher schneiden die APMIs mit höherer
#Nummer schlechter ab.
#Im Mean schneiden die MIs ebenfalls schlechter ab!! Dh das zeigt deutlich,m warum die
#tulimatePunishers benötigt werden.
#Die Hardrule verbessert Ergebnis kaum
#Dasselbe Ergebnis bei less und bei more APDeceivers; siehe Beispiele 13 und 14
#die APDeceivers bekommen auch u-Status, wenn u auf 10 gesetzt wird.


# Hier macht OI etwas aus
exampleList["13(NeutMI): neutralizing MIs + less AntiPunishDeceivers"] = \
    ("Example 13(NeutMI): neutralizing MIs + less AntiPunishDeceivers",
     [Induction.AntiPunishDeceiver("AntiPun 1"),
      Induction.AntiPunishDeceiver("AntiPun 2"),
      Induction.AntiPunishDeceiver("AntiPun 3"),
      Induction.AntiPunishDeceiver("AntiPun 4"),
      Induction.PunishMIColl(name = "MI 1"),
      Induction.PunishMIColl(name = "MI 2"),
      Induction.PunishMIColl(name = "MI 3"),
      Induction.PunishMIColl(name = "MI 4"),
      Induction.PunishMIColl(name = "MI 5"),
      Induction.PunishMIColl(name = "MI 6"),
      #Induction.ObjectInductivist("OI"),
      ],
     bluePens[:4] + redPens[:6] + greenPens, 500,
     lambda : Induction.getRandomEvent(2.0/3.0))

#Hier macht OI etwas aus
exampleList["14(NeutMI): neutralizing MIs + more AntiPunishDeceivers"] = \
    ("Example 14(NeutMI): neutralizing MIs + more AntiPunishDeceivers",
     [Induction.AntiPunishDeceiver("AntiPun 1"),
      Induction.AntiPunishDeceiver("AntiPun 2"),      
      Induction.AntiPunishDeceiver("AntiPun 3"),
      Induction.AntiPunishDeceiver("AntiPun 4"),
      Induction.AntiPunishDeceiver("AntiPun 5"),
      Induction.AntiPunishDeceiver("AntiPun 6"),
      Induction.PunishMIColl(name = "MI 1"),
      Induction.PunishMIColl(name = "MI 2"),
      Induction.PunishMIColl(name = "MI 3"),
      Induction.PunishMIColl(name = "MI 4")
    # ,Induction.ObjectInductivist("OI"),
      ],
     bluePens[:6] + redPens[:4] + greenPens, 500,
     lambda : Induction.getRandomEvent(2.0/3.0))


# Hier macht OI nichts aus
exampleList["15(UltneutMI): Ultneutralizing MIs + AntiUltPunDeceivers (equal numer)"] = \
    ("Example 15(UltneutMI): Ultneutralizing MIs + AntiUltPunDeceivers (equal numer)",
     [Induction.AntiUltPunDeceiver("AntiPun 1"),
      Induction.AntiUltPunDeceiver("AntiPun 2"),
      Induction.AntiUltPunDeceiver("AntiPun 3"),
      Induction.AntiUltPunDeceiver("AntiPun 4"),
      Induction.AntiUltPunDeceiver("AntiPun 5"),
      Induction.UltPunishMIColl(name = "MI 1"),
      Induction.UltPunishMIColl(name = "MI 2"),
      Induction.UltPunishMIColl(name = "MI 3"),
      Induction.UltPunishMIColl(name = "MI 4"),
      Induction.UltPunishMIColl(name = "MI 5"),
      #Induction.ObjectInductivist("OI"),
      ],
     bluePens[:5] + redPens[:5] + greenPens, 500,
     lambda : Induction.getRandomEvent(2.0/3.0))
#hier konvergieren MeanUltneutMIs und AUPDeceivers gegen Wert nahe 1, denn
#sie sind dauern auf u und sagen daher fast perfekt voraus


# weil mehr UltneutMIs da sind, macht OI etwas aus; denn die beiden freien UltNeutMI
# setzen sonst auf random. Generell liegt hier MI-mean darunter, weil
# die AntiUltPunDeceivers viel besser spielen als die freien UltNeutMI und trotzdem als
#ult-deceivers registriert wurden. Dies zeigt die Schwäche des
# neutralizing Ansatzes.
exampleList["16(UltneutMI): Ultneutralizing MIs + less AntiUltPunDeceivers"] = \
    ("Example 16(UltneutMI): Ultneutralizing MIs + less AntiUltPunDeceivers",
     [Induction.AntiUltPunDeceiver("AntiPun 1"),
      Induction.AntiUltPunDeceiver("AntiPun 2"),
      Induction.AntiUltPunDeceiver("AntiPun 3"),
      Induction.AntiUltPunDeceiver("AntiPun 4"),
      Induction.UltPunishMIColl(name = "MI 1"),
      Induction.UltPunishMIColl(name = "MI 2"),
      Induction.UltPunishMIColl(name = "MI 3"),
      Induction.UltPunishMIColl(name = "MI 4"),
      Induction.UltPunishMIColl(name = "MI 5"),
      Induction.UltPunishMIColl(name = "MI 6"),
      #Induction.ObjectInductivist("OI"),
      ],
     bluePens[:4] + redPens[:6] + greenPens, 500,
     lambda : Induction.getRandomEvent(2.0/3.0))

#Hier macht OI wieder nichts aus; Kovergenz nahe 1 tritt ein
exampleList["17(UltneutMI): Ultneutralizing MIs + more AntiUltPunDeceivers"] = \
    ("Example 17(UltneutMI): Ultneutralizing MIs + more AntiUltPunDeceivers",
     [Induction.AntiUltPunDeceiver("AntiPun 1"),
      Induction.AntiUltPunDeceiver("AntiPun 2"),      
      Induction.AntiUltPunDeceiver("AntiPun 3"),
      Induction.AntiUltPunDeceiver("AntiPun 4"),
      Induction.AntiUltPunDeceiver("AntiPun 5"),
      Induction.AntiUltPunDeceiver("AntiPun 6"),
      Induction.UltPunishMIColl(name = "MI 1"),
      Induction.UltPunishMIColl(name = "MI 2"),
      Induction.UltPunishMIColl(name = "MI 3"),
      Induction.UltPunishMIColl(name = "MI 4")
    # ,Induction.ObjectInductivist("OI"),
      ],
     bluePens[:6] + redPens[:4] + greenPens, 500,
     lambda : Induction.getRandomEvent(2.0/3.0))


#Die folgenden Beispiele testen den PunishMIColl (bzw.den neutMI).
#Die Frage ist, ob unerwünschte deceptionRecordings bzw. u-recordings auftreten.
#Man könnte das auch für den UltPunishMIColl probieren und sehen, ob es bei AmplitudeOscillator
#Verschlechterungen gibt. Das hängt vom Wert von u ab.

exampleList["18(neutMI) - neutralizing MI and AmplitudeOscillator"] = \
    ("Example 18(neutMI) - neutralizing MI and AmplitudeOscillator",
     [Induction.AmplitudeOscillator(0.3, 0.85, name = "AmpOsc"),
      Induction.PunishMIColl(name = "MI")],
     bluePens[:1] + redPens[:1] + greenPens,
     500,
     lambda : Induction.getRandomEvent(2.0/3.0))
#kein unerwünschtes deception recording. Liegt wohl daran, dass MI NUR auf ihn
#setzen kann

exampleList["19(neutMI) - 3 neutralizing MIs and CoupledOscillators + Forecaster"] = \
    ("Example 19(neutMI) - 3 neutralizing MIs and CoupledOscillators + Forecaster",
     [Induction.CoupledOscillator(0.3, 0.85,"CO 1"),
      Induction.CoupledOscillator(0.3, 0.85,"CO 2"),
      Induction.Forecaster(0.70, "Forecaster"),
      Induction.PunishMIColl(name = "MI"),
      Induction.PunishMIColl(name = "MI"),
      Induction.PunishMIColl(name = "MI")],
     bluePens[:3] + redPens[:3] + greenPens,
     500,
     lambda : Induction.getRandomEvent(2.0/3.0))
#Sogar der Forcaster wird hier zumeist, wegen seiner Schwankungen, als u (ultdeceiver)
#registriert. Zeigt hohe Schwäche des deception recording Ansatzes.
#Würde UltPunishMIColl stehen, würden dies eben punishen (ausprobiert).
#Die Schwankungen sind am Anfang einfach zu hoch. Deception recording sollte erst
#TEST: nachdem ich u auf 10 gesetzt habe, geht keiner von denen auf u-Status


exampleList["20(neutMI) - 2 neutralizing MIs + Deceiver + Forecaster"] = \
    ("Example 20(neutMI) - 2 neutralizing MIs + Deceiver + Forecaster",
     [Induction.Spy("D"),
      Induction.Forecaster(0.80, "F"),
      Induction.PunishMIColl(name = "MI"),
      Induction.PunishMIColl(name = "MI")],
     bluePens[:2] + redPens[:2] + greenPens,
     500,
     lambda : Induction.getRandomEvent(1.0/2.0))
#Auch hier kriegt für u=10 keiner den u-Status; für u=3 schon oft.
#der eine geht auf den Spy = SystDeceiver; der andere auf den Forecaster.

exampleList["21(neutMI) - 4 neutralizing MIs + 2 Deceivers + 2 Forecasters"] = \
    ("Example 21 - 4 neutralizing MIs + 2 Deceivers + 2 Forecasters",
     [Induction.Forecaster(0.7, "F 1"),
      Induction.OscDelayedForecaster(0.65, 0.75, 4, 0.9, "F 2"),
    #4 mal min-max, dann letzter Wert
      Induction.Spy("D 1"),
      Induction.Spy("D 2"),
      Induction.PunishMIColl("MI 1"),
      Induction.PunishMIColl("MI 2"),
      Induction.PunishMIColl("MI 3"),
      Induction.PunishMIColl("MI 4")],
      bluePens[:4] + redPens[:4] + greenPens,
      500,
      lambda : Induction.getRandomEvent(2.0/3.0))
#Ebenfalls hier wird F1 schnell als u registriert.
#F1 und F2 verlieren ihren d-Status, behalten aber ihren u-Status.
#UltPunishMIColl hätte hier nicht den Effekt, dass die beiden freien MIs
#zum Schluss auf den besten setzen. Sie würden dann auch bestrafen.
#Habe ich ausprobiert.
#Nachdem ich u auf 10 setzte, krigt auch hier keiner einen u-Status.


#Bei den Antideceiver-Tests ist es egal, ob PunishMIColl oder UltPunishMIColl vorliegt,
#weil sie ja nie deceiven.
#Im folgenden wird OI sogar gebraucht; sonst funktioniert AntiDeceiver nicht,
# denn weil MI von vornherein auf ihn setzt ist die non-cond. Vorbedingung
#nie erfüllt und keine deceiver Meldung erfolgt.
#Hinweis: der AvoidMI hat genau dasselbe Problem
exampleList["22(neutMI) - neutralizing MI + AntiDeceiver + OI"] = \
    ("Example 22(neutMI) - neutralizing MI + AntiDeceiver + OI",
     [Induction.AntiDeceiver("AD"),
      Induction.PunishMIColl("MI"),
     Induction.ObjectInductivist("Object-Inductivist")
      ],
     bluePens[:1] + redPens[:1]+ greenPens,
     500,
     lambda : Induction.getRandomEvent(1.0/2.0))
#Das Logging zeigt, dass AntiDeceivers tatsächlich nie als d registriert werden.

exampleList["22(neutMI) - neutralizing MI + AntiDeceiver"] = \
    ("Example 22(neutMI) - neutralizing MI + AntiDeceiver",
     [Induction.AntiDeceiver("AD"),
      Induction.PunishMIColl("MI")],
     bluePens[:1] + redPens[:1]+ greenPens,
     500,
     lambda : Induction.getRandomEvent(1.0/2.0))

exampleList["23(neutMI) - neutralizing MI + 2 AntiDeceivers"] = \
    ("Example 23(neutMI) - neutralizing MI + 2 AntiDeceivers",
     [Induction.AntiDeceiver("AD 1"),
      Induction.AntiDeceiver("AD 2"),
      Induction.PunishMIColl("MI")],
     bluePens[:2]+ redPens[:1]+ greenPens,
     500,
     lambda : Induction.getRandomEvent(1.0/2.0))

exampleList["24(neutMI) - neutralizing MI + 4 AntiDeceivers"] = \
    ("Example 24(neutMI) - neutralizing MI + 4 AntiDeceivers",
     [Induction.AntiDeceiver("AD 1"),
      Induction.AntiDeceiver("AD 2"),
      Induction.AntiDeceiver("AD 3"),
      Induction.AntiDeceiver("AD 4"),
      Induction.PunishMIColl("MI")],
     bluePens[:4]+redPens[:1]+greenPens,
     500,
     lambda : Induction.getRandomEvent(1.0/2.0))


########################################################################
#
#   Avoidance MI
#
########################################################################

#OI macht was aus, weil aMI nun auf random setzt
exampleList["25(laMI) - local Avoidance-MI + 3 Deceivers"] = \
    ("Example 25(laMI) - local Avoidance-MI + 3 Deceivers",
     [Induction.Spy("D 1"),
      Induction.Spy("D 2"),
      Induction.Spy("D 3"),
      Induction.LocAvoidMI(name = "MI"),
      Induction.ObjectInductivist("OI"),
      ],
     bluePens[:3]+ redPens[:1] + greenPens,
     500,
     lambda : Induction.getRandomEvent(2.0/3.0))
#Unterschied zu AvoidanceMI macht hier nichts aus
#Achtung: Im Logging wird nur globale deceive Funktion ausgespuckt.

exampleList["25(aMI) - Avoidance-MI + 3 Deceivers"] = \
    ("Example 25(aMI) - Avoidance-MI + 3 Deceivers",
     [Induction.Spy("D 1"),
      Induction.Spy("D 2"),
      Induction.Spy("D 3"),
      Induction.AvoidMI(name = "MI"),
      Induction.ObjectInductivist("OI"),
      ],
     bluePens[:3]+ redPens[:1] + greenPens,
     500,
     lambda : Induction.getRandomEvent(2.0/3.0))


exampleList["26(aMI) - AvoidanceMI + AmplitudeOscillator + Forecaster"] = \
    ("Example 26(aMI) - AvoidanceMI + AmplitudeOscillator + Forecaster",
     [Induction.AmplitudeOscillator(0.3, 0.85, "AmpOsc"),
      Induction.Forecaster(0.5, "F"),
      Induction.AvoidMI(name = "MI")],
     bluePens[:2] + redPens[:1] + greenPens,
     500,
     lambda : Induction.getRandomEvent(2.0/3.0))
#Hier wird Forecaster dummerweise oft ald deceiver registriert
#weil MI nur so selten auf ihn setzt. Zeigt neue Schwäche des Ansatzes.
#Hier müsste deception recording Anfangsphase länger sein.
#Ausprobiert: setze Anfangsphasen auf 10: Problem verschwindet, aber auch
#nicht immer. 


# Im folgenden verhält sich UltAvoidMI gelegentlich anders als AvoidMI, nämlich wenn
#der Forecaster sogar u-Status erhält. Das kann schon durch kleine Schwankungen
#passieren, sofern der MI auf Forecaster nur wenige male gesetzt hat, wo dessen
#SuccessRate niedriger war.
exampleList["26(uaMI) - UltAvoidanceMI + AmplitudeOscillator + Forecaster"] = \
    ("Example 26(uaMI) - UltAvoidanceMI + AmplitudeOscillator + Forecaster",
     [Induction.AmplitudeOscillator(0.3, 0.85, "AmpOsc"),
      Induction.Forecaster(0.5, "F"),
      Induction.UltAvoidMI(name = "MI")],
     bluePens[:2] + redPens[:1] + greenPens,
     500,
     lambda : Induction.getRandomEvent(2.0/3.0))


exampleList["27(aMI) - Avoidance-MI + CoupledOscillators, Forecaster"] = \
    ("Example 27(aMI) - Avoidance-MI + CoupledOscillators, Forecaster",
     [Induction.CoupledOscillator(0.3, 0.85,"CO 1"),
      Induction.CoupledOscillator(0.3, 0.85,"CO 2"),
      Induction.Forecaster(0.70, "F"),
      Induction.AvoidMI(name = "MI")],
     bluePens[:3] + redPens[:1] + greenPens,
     500,
     lambda : Induction.getRandomEvent(2.0/3.0))
# Problem: bringt oft Zufalls-Detektion von F2 als deceiver. Aber mit
#erhöhter Anfangsphase 10 nicht so oft.

exampleList["27(uaMI) - UltAvoidance-MI + CoupledOscillators, Forecaster"] = \
    ("Example 27(uaMI) - UltAvoidance-MI + CoupledOscillators, Forecaster",
     [Induction.CoupledOscillator(0.3, 0.85,"CO 1"),
      Induction.CoupledOscillator(0.3, 0.85,"CO 2"),
      Induction.Forecaster(0.70, "F"),
      Induction.UltAvoidMI(name = "MI")],
     bluePens[:3] + redPens[:1] + greenPens,
     500,
     lambda : Induction.getRandomEvent(2.0/3.0))
# Selbes Problem wie oben. u-Status nicht beobachtet.


exampleList["28(laMI) - local Avoidance-MI + 2 Deceivers + 2 Forecasters"] = \
    ("Example 28(laMI) - local Avoidance-MI + 2 Deceivers + 2 Forecasters",
     [Induction.Forecaster(0.7, "F 1"),
      Induction.DelayedForecaster(0.9, 200, "F 2"),
    #4 mal min-max, dann letzter Wert
      Induction.Spy("D 1"),
      Induction.Spy("D 2"),
      Induction.LocAvoidMI(name = "MI")],
      greenPens[:2] + bluePens[:2] + redPens[:12] + greenPens,
      500,
      lambda : Induction.getRandomEvent(2.0/3.0))
#Wieder tritt oft unerwünschte deception recording beim Forcaster1 auf.
#Ein Unterschied des localAvoidanceMI zum AvoidanzMI tritt nicht auf.
#auch kaum zum UltAvoidanceMI.

exampleList["28(aMI) - Avoidance-MI + 2 Deceivers + 2 Forecasters"] = \
    ("Example 28(aMI) - Avoidance-MI + 2 Deceivers + 2 Forecasters",
     [Induction.Forecaster(0.7, "F 1"),
      Induction.DelayedForecaster(0.9, 200, "F 2"),
    #4 mal min-max, dann letzter Wert
      Induction.Spy("D 1"),
      Induction.Spy("D 2"),
      Induction.AvoidMI(name = "MI")],
      greenPens[:2] + bluePens[:2] + redPens[:12] + greenPens,
      500,
      lambda : Induction.getRandomEvent(2.0/3.0))

exampleList["28(uaMI) - UltAvoidance-MI + 2 Deceivers + 2 Forecasters"] = \
    ("Example 28(uaMI) - UltAvoidance-MI + 2 Deceivers + 2 Forecasters",
     [Induction.Forecaster(0.7, "F 1"),
      Induction.DelayedForecaster(0.9, 200, "F 2"),
    #4 mal min-max, dann letzter Wert
      Induction.Spy("D 1"),
      Induction.Spy("D 2"),
      Induction.UltAvoidMI(name = "MI")],
      greenPens[:2] + bluePens[:2] + redPens[:12] + greenPens,
      500,
      lambda : Induction.getRandomEvent(2.0/3.0))


#Im folgenden kann sich Unterschied locAvoidMI zu AvoidMI auswirken;
# wegen eMI. Der setzt auf einen Deceiver; der sagt falsch voraus.
# Ist nicht klar, ob das Unterschied bewirkt. Jedenfalls muss der localAvoidMI
#auf beide deceivers hinreichend oft gesetzt haben, damit er beide als deceived
#erkennt, während der globale AvoidMI schon vom Setzen des eMI profitiert.
#Dh der localAvoidMI könnte etwas länger brauchen.
#Achtung: Im Logging wird nur globale deceive Funktion ausgespuckt.
exampleList["29(laMI) - local Avoidance-MI + eMI + 2 Deceivers + 2 Forecasters"] = \
    ("Example 28(laMI) - local Avoidance-MI + eMI + 2 Deceivers + 2 Forecasters",
     [Induction.Forecaster(0.7, "F 1"),
      Induction.DelayedForecaster(0.9, 200, "F 2"),
    #4 mal min-max, dann letzter Wert
      Induction.Spy("D 1"),
      Induction.Spy("D 2"),
      Induction.EpsilonMetaInductivist(name = "eMI"),
      Induction.LocAvoidMI(name = "aMI")],
      greenPens[:2] + bluePens[:2] + redPens[:12] + greenPens,
      500,
      lambda : Induction.getRandomEvent(2.0/3.0))


exampleList["29(aMI) - Avoidance-MI + eMI + 2 Deceivers + 2 Forecasters"] = \
    ("Example 28(aMI) - Avoidance-MI + eMI + 2 Deceivers + 2 Forecasters",
     [Induction.Forecaster(0.7, "F 1"),
      Induction.DelayedForecaster(0.9, 200, "F 2"),
      Induction.Spy("D 1"),
      Induction.Spy("D 2"),
      Induction.EpsilonMetaInductivist(name = "eMI"),
      Induction.AvoidMI(name = "aMI")],
      greenPens[:2] + bluePens[:2] + redPens[:12] + greenPens,
      500,
      lambda : Induction.getRandomEvent(2.0/3.0))


exampleList["29(uaMI) - UltAvoidance-MI + eMI + 2 Deceivers + 2 Forecasters"] = \
    ("Example 28(uaMI) - UltAvoidance-MI + eMI + 2 Deceivers + 2 Forecasters",
     [Induction.Forecaster(0.7, "F 1"),
      Induction.DelayedForecaster(0.9, 200, "F 2"),
      Induction.Spy("D 1"),
      Induction.Spy("D 2"),
      Induction.EpsilonMetaInductivist(name = "eMI"),
      Induction.UltAvoidMI(name = "aMI")],
      greenPens[:2] + bluePens[:2] + redPens[:12] + greenPens,
      500,
      lambda : Induction.getRandomEvent(2.0/3.0))

exampleList["30(WeiAvMIColl): 10 WeightAvMIColls + 10 AmpOscillators"] = \
    ("Example 30(WeiAvMIColl): 10 WeightAvMIColls + 10 AmpOscillators",
     [Induction.AmplitudeOscillator(0.3, 0.85, "AmpOsc1"),
      Induction.AmplitudeOscillator(0.35, 0.8, "AmpOsc2"),
      Induction.AmplitudeOscillator(0.4, 0.75, "AmpOsc3"),
      Induction.AmplitudeOscillator(0.45, 0.7, "AmpOsc4"),
      Induction.AmplitudeOscillator(0.5, 0.65, "AmpOsc5"),
      Induction.AmplitudeOscillator(0.55, 0.6, "AmpOsc6"),
      Induction.AmplitudeOscillator(0.62, 0.63, "AmpOsc7"),
      Induction.AmplitudeOscillator(0.2, 0.9, "AmpOsc8"),
      Induction.AmplitudeOscillator(0.15, 0.95, "AmpOsc9"),
      Induction.AmplitudeOscillator(0.1, 0.95, "AmpOsc10"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      #Induction.ObjectInductivist("OI")
      ],
      bluePens[:10] + redPens[:10] + greenPens, 500,
     lambda : Induction.getRandomEvent(2.0/3.0))
#Eindrucksvolles Bild; die AmpOscillators schwanken; der MI ganz oben; viel
#höher als der non_MImean.

exampleList["31(WeiAvMIColl): 10 WeightAvMIColls + 10 AvDeceivers"] = \
    ("Example 31(WeiAvMIColl): 10 WeightAvMIColls + 10 AvDeceivers",
     [Induction.AvDeceiver ("D1"),
      Induction.AvDeceiver ("D2"),
      Induction.AvDeceiver ("D3"),
      Induction.AvDeceiver ("D4"),
      Induction.AvDeceiver ("D5"),
      Induction.AvDeceiver ("D6"),
      Induction.AvDeceiver ("D7"),
      Induction.AvDeceiver ("D8"),
      Induction.AvDeceiver ("D9"),
      Induction.AvDeceiver ("D10"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      #Induction.ObjectInductivist("OI")
      ],
      bluePens[:10] + redPens[:10] + greenPens, 500,
     lambda : Induction.getRandomEvent(2.0/3.0))
#Obwohl sie Avdeceivers sind, geht ihr Erfolg ganz nach oben.
#Logging zeigt: die AvDeceivers fangen bei 1 in Success an, sinken dann
#ganz nach unten, unter 0.5, und damit ist ihre Attraktivität
#negativ. MIs sagen randomguess voraus. Der Erfolg der AvDeceivers steigt dann
#aber wieder an, auf leicht positiven Wert.

#A kind of worst case
exampleList["32(WeiAvMIColl): 10 WeightAvMIColls + 10 different AvDeceivers"] = \
    ("Example 32(WeiAvMIColl): 10 WeightAvMIColls + 10 different AvDeceivers",
     [Induction.AvDeceiver ("D1"),
      Induction.AvDeceiver ("D2"),
      Induction.AvDeceiver ("D3"),
      Induction.AvDeceiver0 ("D4"),
      Induction.AvDeceiver0 ("D5"),
      Induction.AvDeceiver1 ("D6"),
      Induction.AvDeceiver1 ("D7"),
      Induction.AvDeceiver1 ("D8"),
      Induction.AvDeceiver2 ("D9"),
      Induction.AvDeceiver2 ("D10"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      #Induction.ObjectInductivist("OI")
      ],
      bluePens[:10] + redPens[:10] + greenPens, 500,
     lambda : Induction.getRandomEvent(2.0/3.0))
#Selbst hier, die 0AvDeceivers gehen letztlich in ihrem Erfolg nahe 1.
#Weil der idealSucesss liegt immer darüber!! Denn während
#AvDeceiver unter 0.5 prognostizierten, prognostizierten AvWeightMIs 0.5.
#Weil die 0AvDeceivers nicht ins Gewicht fallen, bleibt das
#so. Daher gehten Erfolgswerte hinauf. Ein nicht-0-AvDeceiver genügt; s. unten
#


#Anders im Fall, wo nur 0AvDeceivers da sind, Da gehen beide Erfolgsraten
#gegen Null.
#Aber: sobald nur ein AvDeceiver1 dabei ist, oder über Null, genügt der,
#damit Erfolge langfristig gegen 1 streben!! Habe ich ausprobiert.
#Denn dessen Attraktivität liegt dann zwischen 0 und 0.1, alle sagen voraus
#was er voraussagt, und die Av0deceivers sagen knapp unter Attraktivität 0
#richtig voraus und werden nie in idealprediction berücksichtig.
exampleList["32(WeiAvMIColl): 10 WeightAvMIColls + 10 Av0Deceivers"] = \
    ("Example 32(WeiAvMIColl): 10 WeightAvMIColls + 10 Av0Deceivers",
     [Induction.AvDeceiver0 ("D1"),
      Induction.AvDeceiver0 ("D2"),
      Induction.AvDeceiver0 ("D3"),
      Induction.AvDeceiver0 ("D4"),
      Induction.AvDeceiver0 ("D5"),
      Induction.AvDeceiver0 ("D6"),
      Induction.AvDeceiver0 ("D7"),
      Induction.AvDeceiver0 ("D8"),
      Induction.AvDeceiver0 ("D9"),
      Induction.AvDeceiver0 ("D10"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      #Induction.ObjectInductivist("OI")
      ],
      bluePens[:10] + redPens[:10] + greenPens, 500,
     lambda : Induction.getRandomEvent(2.0/3.0))


exampleList["33(WeiAvMIColl): 10 WeightAvMIColls + 5 diff. AvDeceivers + 5 AmpOsc"] = \
    ("Example 33(WeiAvMIColl): 10 WeightAvMIColls + 5 diff AvDeceivers + 5 AmpOsc",
     [Induction.AvDeceiver ("D1"),
      Induction.AvDeceiver ("D2"),
      Induction.AvDeceiver0 ("D3"),
      Induction.AvDeceiver1 ("D4"),
      Induction.AvDeceiver2 ("D5"),
      Induction.AmplitudeOscillator(0.3, 0.85, "AmpOsc1"),
      Induction.AmplitudeOscillator(0.4, 0.75, "AmpOsc2"),
      Induction.AmplitudeOscillator(0.5, 0.8, "AmpOsc3"),
      Induction.AmplitudeOscillator(0.4, 0.9, "AmpOsc4"),
      Induction.AmplitudeOscillator(0.8, 0.95, "AmpOsc5"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      #Induction.ObjectInductivist("OI")
      ],
      bluePens[:10] + redPens[:10] + greenPens, 500,
     lambda : Induction.getRandomEvent(2.0/3.0))
#Hier gegen Erfolgsraten wieder gegen 1; nur die AmpOscillators liegen drunter


exampleList["34(WeiAvMIColl): 10 WeightAvMIColls + 4 diff. AvDeceivers"] = \
    ("Example 34(WeiAvMIColl): 10 WeightAvMIColls + 4 diff AvDeceivers",
     [Induction.AvDeceiver0Lim9 ("D1"),
      Induction.AvDeceiver1Lim8 ("D2"),
      Induction.AvDeceiver0Lim8 ("D3"),
      Induction.AvDeceiver1Lim9 ("D4"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      #Induction.ObjectInductivist("OI")
      ],
      bluePens[:4] + redPens[:10] + greenPens, 500,
     lambda : Induction.getRandomEvent(2.0/3.0))
#Hier gehen die Erfolgsraten der AvDeceivers gegen ihren Limes
#Wohlgemerkt: die AvODeceivers sagen knapp unter Null voraus.
#Solange nur ein AvDeceiver da ist, dessen Atraktivtät knapp über null ist
#sagen die MIs daher dasselbe voraus wie der, also 1.


exampleList["35(WeiAvMIColl): 10 WeightAvMIColls + 2 diff. AvDeceivers + 2 AmpOsc"] = \
    ("Example 35(WeiAvMIColl): 10 WeightAvMIColls + 2 diff AvDeceivers + 2 AmpOsc",
     [Induction.AvDeceiver0Lim9 ("D1"),
      Induction.AvDeceiver1Lim8 ("D2"),
      Induction.AmplitudeOscillator(0.7, 0.85, "AmpOsc1"),
      Induction.AmplitudeOscillator(0.8, 0.95, "AmpOsc2"),   
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      Induction.WeightAvMIColl(name="MI"),
      #Induction.ObjectInductivist("OI")
      ],
      bluePens[:4] + redPens[:10] + greenPens, 500,
     lambda : Induction.getRandomEvent(2.0/3.0))



#Step1: holt aus dem Modul = file "SimWindow" die Klasseninstanz Simulation,
# mit dem Parameter exampleList, der eingegeben wird.
sim = SimWindow.Simulation(exampleList)
# "Simulation" baut auch entsprechenden Parameter der Klasse "SimWindow" auf.


# Nachdem die Klasseninstanz erzeugt wurde, wird dort der Befehl "run" erzeugt
sim.run()
#Wartet bis Fenster wieder geschlossen wird. Wenn User Menuepunkt auswählt, wird was getan

##Debugging-Code:
##for mi in sim.world.miList:
##    for a in sim.world.non_miList:
##        if sim.world.putList[a.name][mi.name] > 0:
##            print mi.name, a.name, sim.world.succ(a, mi)
##for a in sim.world.non_miList:
##    print a.name, a.successRate
    

