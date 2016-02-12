#!/usr/bin/python
# -*- encoding: UTF-8 -*-

# Beispiele für induktive Prognosespiele

import SimWindow, Induction
from PyPlotter import Gfx, Graph, Colors


def bright(c):
    brightness = c[0]**2 + c[1]**2 + c[2]**2
    return brightness > 0.4

redPens = [Gfx.Pen(c) for c in filter(bright,filter(Colors.RedFilter, Colors.colors))]
bluePens = [Gfx.Pen(c) for c in filter(bright,filter(Colors.BlueFilter, Colors.colors))]
greenPens = [Gfx.Pen(c) for c in filter(bright,filter(Colors.GreenFilter, Colors.colors))]
yellowPens = [Gfx.Pen(c) for c in filter(bright,filter(Colors.YellowFilter, Colors.colors))]
emptyPens = [Graph.DONT_DRAW_PEN]*10

exampleList = {}

exampleList["01(MI): MI + Forecasters"]  =  \
    ("Example 01(MI): MI + Forecasters",
     [Induction.DelayedForecaster(0.7, 40, "Forecaster 1 (success; delay)"),
      Induction.ForecasterFromBottom(0.90, "Forecaster 2 (success; recovers from zero)"),
      Induction.MetaInductivist("Meta-Inductivist"),
      Induction.ObjectInductivist("Object-Inductivist")],
     bluePens[:2] + redPens[:1] + greenPens,
     500,
     lambda : Induction.getRandomEvent(2.0/3.0))

exampleList["02(MI): MI + Amplitude-Oscillator + OI"] = \
    ("Example 02(MI): MI + Amplitude-Oscillator + OI",
     [Induction.AmplitudeOscillator(0.3, 0.85, "AmpOsc"),
      Induction.MetaInductivist("Meta-Inductivist"),
      Induction.ObjectInductivist("Object-Inductivist")],
     bluePens[:1] + redPens[:1] + greenPens,
     500,
     lambda : Induction.getRandomEvent(2.0/3.0))

exampleList["03(MI): MI + 1 Systematic Oscillator + OI"] = \
    ("Example 03(MI): MI + 1 Systematic Oscillator + OI",
     [Induction.SystOscillator("SystOscillator"),
     Induction.MetaInductivist("Meta-Inductivist"),
      Induction.ObjectInductivist("Object-Inductivist")],
     bluePens[:1] + redPens[:1] + greenPens, 500,
     lambda : Induction.getRandomEvent(2.0/3.0))

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

# weil mehr UltneutMis da sind, macht OI etwas aus; denn MIs
# setzen sonst auf random. generell liegt hier MI-mean darunter, weil
# die AntiUltPunDeceivers viel besser spielen und trotzdem als
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

#Hier macht OI wieder nichts aus
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


exampleList["18(neutMI) - neutralizing MI and AmplitudeOscillator"] = \
    ("Example 18(neutMI) - neutralizing MI and AmplitudeOscillator",
     [Induction.AmplitudeOscillator(0.3, 0.85, name = "AmpOsc"),
      Induction.PunishMIColl(name = "MI")],
     bluePens[:1] + redPens[:1] + greenPens,
     500,
     lambda : Induction.getRandomEvent(2.0/3.0))

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

exampleList["20(neutMI) - 2 neutralizing MIs + Deceiver + Forecaster"] = \
    ("Example 20(neutMI) - 2 neutralizing MIs + Deceiver + Forecaster",
     [Induction.Spy("D"),
      Induction.Forecaster(0.80, "F"),
      Induction.PunishMIColl(name = "MI"),
      Induction.PunishMIColl(name = "MI")],
     bluePens[:2] + redPens[:2] + greenPens,
     500,
     lambda : Induction.getRandomEvent(1.0/2.0))

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


#hier wird OI sogar gebraucht; sonst funktioniert AntiDeceiver nicht,
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

#Hier kann sich UNterschied locAvoidMI zu AvoidMI auswirken; wegen eMI
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

exampleList["27(aMI) - Avoidance-MI + CoupledOscillators, Forecaster"] = \
    ("Example 27(aMI) - Avoidance-MI + CoupledOscillators, Forecaster",
     [Induction.CoupledOscillator(0.3, 0.85,"CO 1"),
      Induction.CoupledOscillator(0.3, 0.85,"CO 2"),
      Induction.Forecaster(0.70, "F"),
      Induction.AvoidMI(name = "MI")],
     bluePens[:3] + redPens[:1] + greenPens,
     500,
     lambda : Induction.getRandomEvent(2.0/3.0))

# Problem: bringt oft Zufalls-Detektion von F2 als deceiver

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

# Hier verhält sich UltAvoidMI anders als AvoidMI
exampleList["26(uaMI) - UltAvoidanceMI + AmplitudeOscillator + Forecaster"] = \
    ("Example 26(uaMI) - UltAvoidanceMI + AmplitudeOscillator + Forecaster",
     [Induction.AmplitudeOscillator(0.3, 0.85, "AmpOsc"),
      Induction.Forecaster(0.5, "F"),
      Induction.UltAvoidMI(name = "MI")],
     bluePens[:2] + redPens[:1] + greenPens,
     500,
     lambda : Induction.getRandomEvent(2.0/3.0))

exampleList["27(uaMI) - UltAvoidance-MI + CoupledOscillators, Forecaster"] = \
    ("Example 27(uaMI) - UltAvoidance-MI + CoupledOscillators, Forecaster",
     [Induction.CoupledOscillator(0.3, 0.85,"CO 1"),
      Induction.CoupledOscillator(0.3, 0.85,"CO 2"),
      Induction.Forecaster(0.70, "F"),
      Induction.UltAvoidMI(name = "MI")],
     bluePens[:3] + redPens[:1] + greenPens,
     500,
     lambda : Induction.getRandomEvent(2.0/3.0))

# Problem: bringt oft Zufalls-Detektion von F2 als deceiver

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





sim = SimWindow.Simulation(exampleList)
sim.run()

##for mi in sim.world.miList:
##    for a in sim.world.non_miList:
##        if sim.world.putList[a.name][mi.name] > 0:
##            print mi.name, a.name, sim.world.succ(a, mi)
##for a in sim.world.non_miList:
##    print a.name, a.successRate
    

