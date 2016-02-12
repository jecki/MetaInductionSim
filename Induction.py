# -*- encoding: UTF-8 -*-
# Induktionsalgorithmen


import random
from PyPlotter.Compatibility import *

########################################################################
#
#  Global Parameters   
#
########################################################################

ERROR_TOLERANCE = 1.0 / 1000000.0

first_from_left = lambda l:l[0]          
first_from_right = lambda l:l[-1] 
random_choice = random.choice     

choice = first_from_left
epsilon = 0.05
epsilonD = 0.04
hardrule = False


########################################################################
#
#  Random event series functions
#
########################################################################


def randomBool(p = 0.5):
    """Return True with a probability of p."""
    if random.random() < p: return True
    else: return False

def getRandomEvent(p = 0.5):
    """Generate a random event that is 1 with the probability p
    otherwise 0."""
    if random.random() < p: return 1
    else: return 0

def invertEvent(e):
    """Return the inverted event."""
    if e == 1: return 0
    else: return 1


########################################################################
#
#   World class   
#
########################################################################


class World(object):
    """The world class contains all global variables such as the
    lists of predictor strategies, the number of the current round
    etc.

    Attributes:
        round           - round number
        event           - the next event to take place
        absFrequency    - absolute frequency of the event 1
        relFrequency    - relative frequency of the event 1
        miList          - list of predictors that are meta inductivists
        non_miList      - list of predictors that are not meta
                          inductivists
        miMean          - average success rate of all MIs 
        non_miMean      - average success rate of all non MIs
        favN            - dictionary that records for each strategy the
                          number of rounds when it is being observed by
                          any MI
        absucc          - dictionary that counts the absolute success 
                          of each strategies when it is being observed
                          by any MI
        deceivers       - list of deceivers (updated after each round before the
                          analyse-methods are called)
        nondeceivers    - list of nondeceivers (updated after each round before the
                          analyse-methods are called)
        ultdeceivers    - list of three times out deceivers 
        nonultdeceivers - list of non three times out deceivers
        alldeceivers    - list of deceivers and ultdeceivers
        nonalldeceivers - list of non alldeceivers 
        favlist         - list of favorites (updated after each round before the
                          analyse-methods are called)
        worldDeceived   - A variable taking as its values the predictor that
                          is deceived by the world (the world can only deceive one
                           predictor at a time) or None, if there is no world
                          deception. """
    
    def __init__(self, eventFunction = lambda : getRandomEvent(2.0/3.0)):
        self.getEvent = eventFunction
        self.round = 0
        self.event = 0
        self.absFrequency = 0
        self.relFrequency = 0.0
        self.predictorList = []
        self.miList = []
        self.non_miList = []
        self.miMean = 0.0
        self.non_miMean = 0.0        
        self.deceivers = []
        self.nondeceivers = []
        self.ultdeceivers = []
        self.alldeceivers = []
        self.nonalldeceivers = []
        self.nonultdeceivers = []        
        self.favN = {}
        self.absucc = {}
        self.favlist = []
        self.deceiveCount = {}
        self.deceiveState = {}
        self.worldDeceived = None

        
    def register(self, predictor):
        """Add another predictor strategy. Make sure that meta
        inductivists will always be last in the predictor list.
        wird nur einmal durchlaufen, vor Simulation"""
        assert self.round == 0, "Simulation is already running: " + \
                                "Predictors can not be added any more!"

        if isinstance(predictor, MetaInductivist):
            self.miList.append(predictor)
        else:
            self.non_miList.append(predictor)
            self.favN[predictor.name] = 0
            self.absucc[predictor.name] = 0
            self.nonultdeceivers.append(predictor)
            self.deceiveCount[predictor.name] = 0
            self.deceiveState[predictor.name] = False
        
        predictor.registeredBy(self)
        #print str(predictor)

    def getPredictorList(self):
        """-> list of all registered predictors, MIs and non MIs"""
        return self.non_miList + self.miList
                
    def nextRound(self):
        """Generate a new event. Let the predictors make their
        predictions and evaluate theis predictions, i.e. update
        the variables storing the absolute success rate as well
        as the relative success rate. Update the event frequency
        rates. Finally, call the predictors analyse method.
        """
        self.round += 1

        if self.worldDeceived:
            if isinstance(self.worldDeceived.fav, ObjectInductivist):
                if self.relFrequency > 0.5:
                    self.event = 0
                elif self.relFrequency < 0.5:
                    self.event = 1
                else:
                    self.event = getRandomEvent(0.5)
            elif self.worldDeceived.fav == None:
                self.event = getRandomEvent(0.5)
            else: self.event = self.getEvent()
    # wenn worldDeceived und Runde 1, dann in jedem Fall getEandomEvent(0.5)
        else:
            self.event = self.getEvent()

            
# zuerst sagen non-mi's voraus, dann erstdie mi's, weil
# die mi's auf Vorhersagen der non-mi's zurückgreifen
        for predictor in self.non_miList + self.miList:
            e = predictor.predict()
            if e == self.event: predictor.success += 1
            predictor.successRate = predictor.success / float(self.round)
                       
        if self.event == 1:  self.absFrequency += 1
        self.relFrequency = self.absFrequency / float(self.round)

        if self.miList:
            self.miMean = sum([p.successRate for p in self.miList]) / \
                          len(self.miList)
        if self.non_miList:
            self.non_miMean = sum([p.successRate for p in self.non_miList]) / \
                              len(self.non_miList)
        
# zuerst analyse für mi's, dann erst für non-mi's, weil non-mi's
# wissen müssen, ob sie fav's sind.
        self.updateControlDictionaries()
        for predictor in self.miList + self.non_miList:
            predictor.analyse()


    def updateControlDictionaries(self):
        self.favlist = [m.fav for m in self.miList]
        self.deceivers = []
        self.nondeceivers = []
        for p in self.non_miList:
            if p in self.favlist:
                self.favN[p.name] += 1
                if p.prediction == self.event:
                    self.absucc[p.name] += 1
            if self.deceived(p):
                self.deceivers.append(p)
            else:
                self.nondeceivers.append(p)
        for p in self.nonultdeceivers:      
            if self.ultdeceived(p):
                self.ultdeceivers.append(p)
                self.nonultdeceivers.remove(p)
        self.alldeceivers = list(set(self.deceivers).union(set(self.ultdeceivers)))
        self.nonalldeceivers = [x for x in self.non_miList \
                                if not x in self.alldeceivers]


# Globale Deception detection, in class world
# absucc ist der abs.succ. von a während a fav war
# sucess ist der abs.succ. von a

    def _deceptionRule(self, round, n, absucc, success):
        if n <= 5:
            return False
        condSuccRate = absucc / float(n)
        if hardrule:
            if (round - n) <= 5:  return False
            invSuccRate = float(success - absucc) / float(round - n)
            return invSuccRate > condSuccRate + epsilonD
        else:
            succRate = success / float(round)
            return (succRate > condSuccRate + epsilonD or succRate < epsilonD)
# wozu wird die succRate hier neu bestimmt: weil sie auch bei future_Anwendung
# gebraucht wird. Die Or-Bedingung ist neu!
        
# Globale FutureDeceived Funktion
# bedeutet: wenn non-MI nächstes Mal richtig vorhersagen würde,
# würde er ein globaler deceiver sein. Wird nur erzeugt wenn a fav ist
    def future_deceivedup(self, a):
        return self._deceptionRule(self.round+1,
                                   self.favN[a.name],
                                   self.absucc[a.name],
                                   a.success+1)
        

    def future_deceiveddown(self, a):
        return self._deceptionRule(self.round+1,
                                   self.favN[a.name]+1,
                                   self.absucc[a.name],
                                   a.success)

    def deceived(self, a):
        return self._deceptionRule(self.round,
                                   self.favN[a.name],
                                   self.absucc[a.name],
                                   a.success)

    def ultdeceived(self, a):
        if self.deceiveCount[a.name] >= 3:
            return True
        else:
            if self.deceived(a):
                if not self.deceiveState[a.name]:
                    self.deceiveCount[a.name] += 1
                self.deceiveState[a.name] = True
            else:
                self.deceiveState[a.name] = False
        return False     


########################################################################
#
#   Predictor classes
#
########################################################################

# aus Kompatibilitiätsgründen (jython) werden hier "old style"-Klassen
# verwendet, die nicht von "object" abgeleitet sind. Andernfalls sollte
# man ab Python 2.2 besser "new style"-Klassen verwenden, d.h.
# "class Predictor(object):" schreiben. Auf die Funktion des Programms
# hat das aber keinen Einfluss! 

class Predictor:
    """Template for a prediction strategy.

    Attributes:
        name            - predictor's name
        short           - predictor's short name
        suffix          - a suffix number to the predictor's name in
                          order to tell different predictors apart 
        world           - a reference to the world object this predictor
                          belongs to
        success         - absolute number of correct predictions
        successRate     - average rate of correct predictions so far
        prediction      - prediction made in the current round
                          (only after method predict has been called)
    """

    def __str__(self):
        if self.suffix >= 1: return self.name+" "+str(self.suffix)
        else: return self.name
   
    def __init__(self, name):
        self.name = name
        self.short = ""
        self.suffix = 0
        self.world = None
        self.success = 0
        self.successRate = 0.0
        self.prediction = 0

    def shortName(self, length = 3):
        """Returns an abbreviated name of 'length' characters"""
        if len(self.short) == length: return self.short
        s = str(self)
        if len(s) < length:
            self.short = s + " "*(length-len(s))
            return self.short
        r = []; alphaNum = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        for ch in s:
            if ch in alphaNum:
                r.append(ch)
            elif ch in ", ":  alphaNum = alphaNum + "0123456789"
            elif ch == ".":
                del r[-1]
                alphaNum = alphaNum[:26]
        r = r[:length]
        if len(r) < length: r.extend([" "]*(length-len(r)))
        if self.suffix >= 1: r[-1] = str(self.suffix)[-1]
        self.short = "".join(r)
        return self.short

    def _determineSuffix(self):
        l = [p for p in self.world.getPredictorList() \
             if p.name == self.name and p != self]
        if l:
            if l[-1].suffix == 0: l[-1].suffix = 1
            self.suffix = l[-1].suffix + 1
            self.short = "";  l[-1].short = ""
            
    def registeredBy(self, world):
        """Associates predictor with a world-object."""
        self.world = world
        self._determineSuffix()
        self.short = ""
        self.short = self.shortName(3)
        
    def predict(self):
        """Predict the next event."""
        raise NotImplementedError

    def analyse(self):
        """Possible analysis of results after the prediction cycle
        is finished.
        """
        pass
        

def bestOf(predictorList):
    """Return the most succesful predictor(s) of the list. The
    return value is a list of one or more predictors. The latter
    is the case if there are several equally good best predictors
    in the list.
    """
    assert predictorList != [], "Predictor list is empty!"
    bestList = []
    bestRate = -1.0
    for p in predictorList:
        if p.successRate > bestRate:
            bestList = [p]
            bestRate = p.successRate
        elif p.successRate == bestRate:
            bestList.append(p)
    return bestList


def worstOf(predictorList):
    """Return the least succesful predictor(s) of the list. The
    return value is a list of one or more predictors. The latter
    is the case if there are several equally bad worst predictors
    in the list.
    """
    assert predictorList != [], "Predictor list is empty!"
    worstList = []
    worstRate = 2.0
    for p in predictorList:
        if p.successRate < worstRate:
            worstList = [p]
            worstRate = p.successRate
        elif p.successRate == worstRate:
            worstList.append(p)
    return worstList            


########################################################################
#
#   Random Guess
#
########################################################################


""" Hinweis: da RandomGuess als fallback-Strategie für jeden MI separat
durchgeführt wird, dard dieser RandomGuess nur verwendet werden, wenn
worldDeceived None ist"""

class RandomGuess(Predictor):
    """Random Guess Strategy."""

    def __init__(self, name = "Random Guess"):
        Predictor.__init__(self, name)

    def predict(self):
        self.prediction = getRandomEvent(0.5)
        return self.prediction


########################################################################
#
#   Object Inductivist
#
########################################################################

    
class ObjectInductivist(Predictor):
    """Object inductivist strategy."""

    def __init__(self, name = "Object Inductivist"):
        Predictor.__init__(self, name)
        self.prediction = getRandomEvent()

    def predict(self):
        if self.world.worldDeceived and (self.world.round == 1\
        or self.world.relFrequency == 0.5):
            self.prediction = invertEvent(self.world.event)
    # in diesem Fall wird überschrieben. self.world.relFrequency ist noch
    # auf alten Wert eingestellt. Wenn OI aufgerufen wird, ist er jedenfalls Spieler,
    # und ist daher in erster Runde MI-Favorit
        return self.prediction

    def analyse(self):
        if self.world.relFrequency > 0.5:  self.prediction = 1
        elif self.world.relFrequency < 0.5:  self.prediction = 0
        else: self.prediction = getRandomEvent(0.5)
        


########################################################################
#
#   Forecaster
#
########################################################################

        
class Forecaster(Predictor):
    """A prediction strategy that is successfull at a predifined rate.

    Attributes:
        successAim      - the predifined success rate this
                          Forecaster shall reach
    """

    def __init__(self, successAim, name="Forecaster"):
        Predictor.__init__(self, name + " %.2f" % successAim)
        self.successAim = successAim
        
    def predict(self):
        if randomBool(self.successAim): #randomBool(x) liefert einen W.wert 1 mit W.keit x, sonst 0
            self.prediction = self.world.event
        else:
            self.prediction = invertEvent(self.world.event)
        return self.prediction


class ForecasterFromBottom(Predictor):
    """A prediction strategy that is successfull at a predifined rate.

    Attributes:
        successAim      - the predifined success rate this
                          Forecaster shall reach
    """

    def __init__(self, successAim, name="Forecaster"):
        Predictor.__init__(self, name + " %.2f" % successAim)
        self.successAim = successAim
        
    def predict(self):
        if randomBool(self.successAim) and self.world.round > 70:
    #randomBool(x) liefert einen W.wert 1 mit W.keit x, sonst 0
            self.prediction = self.world.event
        else:
            self.prediction = invertEvent(self.world.event)
        return self.prediction
        

class DelayedForecaster(Forecaster):
    """A prediction strategy that is successfull at a predifined rate
    only after a certain while;  random success before that while.

    Attributes:
        successAim      - the predifined success rate this
                          Forecaster shall reach
        delay           - number of rounds until sucess increases
    """

    def __init__(self, successAim, delay, name="Forecaster"):
        Predictor.__init__(self, name + " %.2f; %i" % (successAim,delay))
        self.successAim = successAim
        self.delay = delay
        
    def predict(self):
        if self.delay > 0:
            self.delay -= 1
            self.prediction = getRandomEvent(0.5)
        else:
            self.prediction = Forecaster.predict(self)   
        return self.prediction


########################################################################
#
#   Oscillator
#
########################################################################

OSC_UP          = "up"
OSC_DOWN        = "down"
OSC_WAITTOP     = "waitTop"
OSC_WAITBOTTOM  = "waitBottom"

class Oscillator(Predictor):
    """Abstract base class for all oscillator classess.

        Attributes:
            phase       - tells whether this oscillator is presently
                          going up or down; can take the value of one
                          of the above defined constants
    """

    def __init__(self, name):
        Predictor.__init__(self, name)
        self.phase = OSC_UP

    def predict(self):        
        if self.phase == OSC_UP: self.prediction = self.world.event
        else: self.prediction = invertEvent(self.world.event)
        return self.prediction

    def analyse(self):
        raise NotImplementedError
    


class AmplitudeOscillator(Oscillator):
    """Success oscillates between predefined rates.

    Attributes:
        min         - minimal success rate value
        max         - maximal success rate value
    """

    def __init__(self, minv, maxv, name = "Amplitude Oscillator"):
        """Succes rate oscillates between min and max."""
        Oscillator.__init__(self, name + " %.2f, %.2f" % (minv, maxv))
        if minv > maxv:
            x = maxv;  maxv = minv;  minv = x
        self.min = minv
        self.max = maxv

    def analyse(self):
        if self.successRate > self.max: self.phase = OSC_DOWN
        elif self.successRate < self.min: self.phase = OSC_UP
        

class PeriodOscillator(Oscillator):
    """An oscillator with a fixed period but (necessarily)
    diminishing amplitude.

    Attributes:
        halfperiod          - half the period length in rounds
        shift               - phase shift in rounds
    """

    def __init__(self, halfperiod, shift, name = "Period Oscillator"):
        Oscillator.__init__(self, name)
        self.name = name + " " + str(halfperiod) + " " + str(shift)
        self.halfperiod = halfperiod
        self.shift = shift % (2*halfperiod)
        if self.shift >= halfperiod:  self.phase = OSC_DOWN
        else: self.phase = OSC_UP
        
    def analyse(self):
        s = (self.world.round+self.shift) % (2*self.halfperiod) 
        if s >= self.halfperiod:  self.phase = OSC_DOWN
        else: self.phase = OSC_UP


class CoupledOscillator(AmplitudeOscillator):
    """Oscillator that is connected to another oscillator of the
    same kind, but opposite phase.

    Attributes:
        combo       - the other oscillator that this one is
                      combined with
    """

    def __init__(self, min, max, name = "Coupled Oscillator"):
        AmplitudeOscillator.__init__(self, min, max, name)
        self.combo = None

    def registeredBy(self, world):
        AmplitudeOscillator.registeredBy(self, world)
        for predictor in self.world.non_miList:
            if isinstance(predictor, CoupledOscillator) and \
               predictor != self:
                self.combo = predictor   
                self.combo.combo = self
                if self.phase == self.combo.phase: 
                    if self.phase == OSC_UP: self.phase = OSC_DOWN
                    else: self.phase = OSC_UP
                break

    def predict(self):
        if self.phase == OSC_UP:
            self.prediction = self.world.event
        elif self.phase == OSC_DOWN:
            self.prediction = invertEvent(self.world.event)
        elif self.phase == OSC_WAITTOP:
            if randomBool(self.max): self.prediction=self.world.event
            else: self.prediction = invertEvent(self.world.event)
        else:   # self.phase == "waitBottom"
            if randomBool(self.min): self.prediction=self.world.event
            else: self.prediction = invertEvent(self.world.event)            
        return self.prediction

    def analyse(self):
        if self.phase == OSC_UP and self.successRate > self.max:
            self.phase = OSC_WAITTOP
        elif self.phase == OSC_DOWN and self.successRate < self.min:
            self.phase = OSC_WAITBOTTOM
        if self.phase == OSC_WAITTOP:
            if self.combo.phase != OSC_DOWN: self.phase = OSC_DOWN   #else do nothing
        elif self.phase == OSC_WAITBOTTOM:
            if self.combo.phase != OSC_UP: self.phase = OSC_UP
                               
                               
                       
class OscDelayedForecaster(Forecaster, AmplitudeOscillator):
    """Forecaster that acts like an Amplitude Oscillator
    in the beginning (for a given number of phases), before
    it acts like a Forecaster.
    
    Attributes:
        phaseLimit  - the number of half phase changes until
            its behavior changes from an amplitude oscillator
            to a Forecaster
        phaseCounter - the actual number of half phase chagnes
        oscState    - the state (up or down) of the current
            phase
            
    Note: the parameter maxPhase of the constructor __init__
    take the number of full phases, while the object variables
    phaseLimit and phaseCounter use half phases!
    """
    def __init__(self, minv, maxv, maxPhases, successAim, 
                 name = "OscDelayedForecaster"):
        Forecaster.__init__(self, successAim, name)
        AmplitudeOscillator.__init__(self, minv, maxv, name)
        self.phaseLimit = maxPhases*2  
        self.phaseCounter = 0
        self.oscState = self.phase
        
    def predict(self):
        if self.phaseCounter < self.phaseLimit:
            return AmplitudeOscillator.predict(self)
        else: return Forecaster.predict(self)
        
    def analyse(self):
        if self.phaseCounter < self.phaseLimit: 
            AmplitudeOscillator.analyse(self)
        else: Forecaster.analyse(self)
        if self.oscState != self.phase:
            self.phaseCounter += 1
            self.oscState = self.phase

        
                           
########################################################################
#
#   Meta-Inductivists
#
########################################################################


class MetaInductivist(Predictor):
    """Follow the most successful strategy so far.

    Attributes:
        fav         - the current favorite of the meta inductivist
    """
    def __init__(self, name = "Meta Inductivist"):
        Predictor.__init__(self, name)
        self.fav = None

    def registeredBy(self, world):
        Predictor.registeredBy(self, world)
        self.fav = None

    def predict(self):
        if self.fav:
            self.prediction = self.fav.prediction
        elif self.world.round == 1 and not(self.world.worldDeceived == self):
            for p in self.world.non_miList:
                if isinstance(p, ObjectInductivist):
                    self.prediction = p.prediction
                    break
            else:
                self.prediction = getRandomEvent()
        else:
            if self.world.worldDeceived == self:
                self.prediction = invertEvent(self.world.event)
            else:
                self.prediction = getRandomEvent() 

        return self.prediction

# self.world.non_miList = Liste aller predictors, die keine MIs sind
# bestof(Liste) gibt Liste der besten Strategien zurück.
# (Liste) wählt Element der Liste der Gleichguten aus
# einzuführen: alphchoice, randchoice
    def analyse(self):
        best = choice(bestOf(self.world.non_miList))
        if self.fav == None or \
           best.successRate > self.fav.successRate:  self.fav = best



class EpsilonMetaInductivist(MetaInductivist):
    """Meta inductivist that picks a new strategy only
    if it is more than a little bit better than its old favorite.
    """

    def __init__(self, name="Epsilon Meta Inductivist"):
        MetaInductivist.__init__(self, name)
  # "%.3f" gibt Format der Zahl nach dem % an. .3Fliesskomma   

    def analyse(self):
        candidate = choice(bestOf(self.world.non_miList))
        if self.fav == None or \
           candidate.successRate > self.fav.successRate + epsilon:
            self.fav = candidate


###################################################################
#### Diese Klasse wird nur für lokale Deception-Detection benötigt,
#### bei local Avoidance MI
####################################################################


class DeceptionDetectionMixin(MetaInductivist):
    """A Mixin class that implements the local "deceived"-function.
    
    Attributes:
        control -  a dictionary of [a,b] indexed by the 
            Non-MI Strategies (possibly deceivers) that records the number
            of times this MI has put each one of them (a) as well as the
            number of successes this MI had when putting on a certain 
            strategy (b).
    """
    def __init__(self):
        self.control = {}

    def _registered(self):
        for p in self.world.non_miList:
            self.control[p.name] = [0, 0]    

# Lokale deception detection; für jeden MI einzeln; diese Klasse abgeleitet von MI
#verwendet nur der bisherige avoidanceMI
# höchstens relevant für die Zukunft

    def succ(self, a):
        """Return the relative success of 'a' while MI has put on 'a'."""
        n, absucc = self.control[a.name]
        if n == 0:  return 0.0
        else:  return float(absucc) / float(n)
        
    def nsucc(self, a):
        """Return the relative success of 'a' while MI has not put on 'a'."""
        n, absucc = self.control[a.name]
        if self.world.round == n:  return 0.0
        else:  return float(a.success - absucc) / float(self.world.round - n)
            
    def deceived(self, a):
        """return True if MI seems to have been deceived by 'a'.
        """
        try:
            n = self.control[a.name][0]
            if hardrule:
                return self.nsucc(a) > self.succ(a) + epsilonD and \
                       (n > 5) and ((self.world.round - n) > 5)            
            else:
                return (n > 5) and ( (a.successRate > self.succ(a) + epsilonD) or \
                        (a.successRate < epsilonD))
        except KeyError:
            raise AssertionError, str(a) + " is not a non-MI!"
            
    def future_deceiveddown(self, a):
        """return True if MI seems to have been deceived by 'a', if
        a cheats in the next round.
        """
        nfav, succfav = self.control[a.name]          
        #f_n = n+1;
        # f_worldround = self.world.round+1
        f_successRate = float(a.success) / float(self.world.round+1)
        f_successRatefav = float(succfav) / float(nfav+1)
        if hardrule:
            return self.nsucc(a) > (f_successRatefav + epsilonD) and \
                   (nfav+1 > 5) and ((self.world.round - nfav) > 5)            
        else:
            return nfav+1 > 5 and (f_successRate > f_successRatefav + epsilonD \
            or f_successRate < epsilonD) 

    def future_deceivedup(self, a):
        """return True if MI seems to have been deceived by 'a', if
        a cheats in the next round.
        """        
        nfav, succfav = self.control[a.name]
        #f_n = n+1;
        # f_worldround = self.world.round+1
        f_successRate = float(a.success +1) / float(self.world.round+1)
        if hardrule:
            return (nfav+1 > 5) and ((self.world.round - nfav) > 5) and \
                   float(a.success+1-succfav)/(self.world.round+1 - nfav) > \
                   (float(succfav)/nfav) + epsilonD
        else:
            return nfav > 5 and (f_successRate > (float(succfav)/nfav) + epsilonD \
            or f_successRate < epsilonD)
        
    def _analyse(self):
        if self.fav in self.world.non_miList:
            self.control[self.fav.name][0] += 1
            if self.fav.prediction == self.world.event:
                self.control[self.fav.name][1] += 1

##    def predict(self):
##        if self.world.randomGuessFlag:
##            if deceivedOI:
##                self.prediction = invertEvent(self.world.event)
##            else:
##                self.prediction = getRandomEvent(p = 0.5)
##        else:
##            self.prediction = self.fav.prediction
##        return self.prediction


#####################################
###   Avoidance MIs  ###
#####################################

class LocAvoidMI(EpsilonMetaInductivist, DeceptionDetectionMixin):
    def __init__(self, name="LocAvoidMI"):
        DeceptionDetectionMixin.__init__(self)        
        EpsilonMetaInductivist.__init__(self, name)

    def registeredBy(self, world):
        EpsilonMetaInductivist.registeredBy(self, world)
        # DeceptionDetectionMixin._registered(self)

    def predict(self):
        if self.world.round == 1:
            DeceptionDetectionMixin._registered(self)
        return EpsilonMetaInductivist.predict(self)  

    def analyse(self):
        DeceptionDetectionMixin._analyse(self)

        if (self.world.round % 100) < 5:
            #gibt alle 100 Runden neue Chance 5 mal
            #Achtung bringt nichts für alle denn der aMI
            #geht ja nur auf den besten
            candidate = choice(bestOf(self.world.non_miList))
            if self.fav == None \
               or candidate.successRate > self.fav.successRate + epsilon:
                self.fav = candidate
            return
        
        agList = self.world.non_miList[:]
        while agList != []:
            F = choice(bestOf(agList))
            if self.deceived(F): agList.remove(F)
            else:  break
        if agList != []:         
            if self.fav not in agList or \
            (F.successRate > self.fav.successRate + epsilon):
                self.fav = F
        else: self.fav = None


# Änderungen:
# deception Recording erst nach n=5 Runden...
# SoftDecRec:  | Succ(Ai,n) - Succ(Ai,n | MIj puts on Ai) |> epsilon
# gibt dem Ai immer wieder eine Chance, weil die Anzahl von Runden von MIj auf Ai setzt,
# verschwindend gering wird im Vgl. zu den Runden, wo das nicht der Fall ist, und daher im
# Quotient untergeht
# HardDecRec:  | Succ(Ai,n | nicht MIj puts on Ai) - Succ(Ai,n | MIj puts on Ai)|> epsilon


class AvoidMI(EpsilonMetaInductivist):
    def __init__(self, name="AvoidMI"):     
        EpsilonMetaInductivist.__init__(self, name)

    def registeredBy(self, world):
        EpsilonMetaInductivist.registeredBy(self, world)

    def analyse(self):
            #spielt wie PunishMIColl wenn nicht neutralizing
            #ausser gibt imemr wieder neue Chance
        if (self.world.round % 100) < 0:
            candidate = choice(bestOf(self.world.non_miList))
            if self.fav == None \
               or candidate.successRate > self.fav.successRate + epsilon:
                self.fav = candidate
            return
        
        if self.world.nondeceivers != []:
            bestAg = choice(bestOf(self.world.nondeceivers))
            if self.fav not in self.world.nondeceivers:
                self.fav = bestAg
            elif bestAg.successRate > (self.fav.successRate + epsilon):
                    self.fav = bestAg
            else: True                    
        else:
            self.fav = None


class UltAvoidMI(EpsilonMetaInductivist):
    def __init__(self, name="AvoidMI"):     
        EpsilonMetaInductivist.__init__(self, name)

    def registeredBy(self, world):
        EpsilonMetaInductivist.registeredBy(self, world)

    def analyse(self):
            #spielt wie PunishMIColl wenn nicht neutralizing
            #ausser gibt imemr wieder neue Chance
        if (self.world.round % 100) < 0:
            candidate = choice(bestOf(self.world.non_miList))
            if self.fav == None \
               or candidate.successRate > self.fav.successRate + epsilon:
                self.fav = candidate
            return
        
        if self.world.nonalldeceivers != []:
            bestAg = choice(bestOf(self.world.nonalldeceivers))
            if self.fav not in self.world.nonalldeceivers:
                self.fav = bestAg
            elif bestAg.successRate > (self.fav.successRate + epsilon):
                    self.fav = bestAg
            else: True                    
        else:
            self.fav = None

###################################################################
### class MIcoll
## Die Überklasse der kollektiv organisierten MIs Nummerieren sich.
#####################################################################

class CollectiveMI(EpsilonMetaInductivist):
    """Abstract base class for collective meta inductivist strategies.
    Collective meta inductivists are prediction strategies that work
    together as a corrdinated group.

    Attributes:
        order       - the order number of the meta inductivist, e.g.
                      if this MI is MI3 then order will be 3
        cmiList     - a list of the other collective meta inductivists
                      (of the same class) in the world with a lower order
    """
    
    def __init__(self, name = "Collective Meta Inductivist"):
        EpsilonMetaInductivist.__init__(self, name)
        self.order = 1
        self.cmiList = [] 

    def registeredBy(self, world):
        for p in world.miList:
            if isinstance(p, self.__class__) and p != self:
                self.order += 1
                self.cmiList.append(p)
        # self.name = self.name + " " + str(self.order)
        EpsilonMetaInductivist.registeredBy(self, world)

    def analyse(self):
        raise NotImplementedError

###################################################################
####### Die invertierten MIColls, die negativ auf andere MIs setzen können
#####################################################################
    
class InvertMIColl(CollectiveMI):
    """This meta inductivist uses other meta inductivists with small success as a
    negatively correlated source for his own predictions.

    Attributes:
        invert      - boolean flag that indicates whether this meta
                      inductivist puts negatively or positively
                      on its favorite
    """

    def __init__(self, name = "InvertMIColl"):
        CollectiveMI.__init__(self, name)
        self.invert = False

    def predict(self):
        if self.fav:
            if self.invert:
                self.prediction = invertEvent(self.fav.prediction)
            else:  self.prediction = self.fav.prediction
        else:  # nur in erster Runde kein fav
            if self.world.worldDeceived == self:
                self.prediction = invertEvent(self.world.event)
            else:
                self.prediction = getRandomEvent(0.5)
        return self.prediction
    
    def analyse(self):
        if self.order == 1:
            EpsilonMetaInductivist.analyse(self)
        else:
            best_nonMI = choice(bestOf(self.world.non_miList))
            worstMI = choice(worstOf(self.cmiList))
            if best_nonMI.successRate >= 1.0 - worstMI.successRate + epsilon:
                self.fav = best_nonMI
                self.invert = False
            else:
                #self.fav = worstMI
                self.fav = worstMI.fav
                # self.invert = not worstMI.invert
                self.invert = True
               
###############################################################
######  Die neutralisierenden MIColls - statt "neutralisierend" steht noch
####### "punish" -- mit deception detection.
###################################################################


class PunishMIColl(CollectiveMI):#, DeceptionDetectionMixin):
    """A collective defense which uses global deception dection to
    protect itself. The MIs "punish" the decivers, or better neutralize
    them, by putting on the deceivers in a 1:1 manner as long as they deceiver.
    The MIs not needed for neutralization/punishment act like ordinary eMIs.
    """    
    def __init__(self, name="Punish"):
#        DeceptionDetectionMixin.__init__(self)        
        CollectiveMI.__init__(self, name)

    def registeredBy(self, world):
        CollectiveMI.registeredBy(self, world)
#        DeceptionDetectionMixin._registered(self)
        # MetaInductivist.registeredBy(self, world)

    def analyse(self):
        if self.world.round < 10:
            candidate = choice(bestOf(self.world.non_miList))
            if not self.fav or \
               candidate.successRate > self.fav.successRate + epsilon:
                self.fav = candidate
            return

        if self.order <= len(self.world.deceivers):
            self.fav = self.world.deceivers[self.order-1]
            #Elementindizierung beginnt mit Null

        else:
            if self.world.nondeceivers != []:
                bestAg = choice(bestOf(self.world.nondeceivers))
                if self.fav not in self.world.nondeceivers:
                    self.fav = bestAg
                elif bestAg.successRate > (self.fav.successRate + epsilon):
                    self.fav = bestAg
                else: True
            else:
                self.fav = None
    

class UltPunishMIColl(PunishMIColl):
    """Like PunishMIColl, but if a deceiver has changed his deception status by
    at least three times, he will be recorded as a deceiver forever (he is then
    a so-called ultimate deceiver).
    """

    def __init__(self, name = "UltPunishMIColl"):
        PunishMIColl.__init__(self, name)

    def analyse(self):
        if self.world.round < 10:
            candidate = choice(bestOf(self.world.non_miList))
            if not self.fav \
               or candidate.successRate > self.fav.successRate + epsilon:
                self.fav = candidate
            return

        if self.order <= len(self.world.alldeceivers):
            self.fav = self.world.alldeceivers[self.order-1]
            #Elementindizierung beginnt mit Null

        else:
            if self.world.nonalldeceivers != []:
                bestAg = choice(bestOf(self.world.nonalldeceivers))
                if self.fav not in self.world.nonalldeceivers:
                    self.fav = bestAg
                elif bestAg.successRate > (self.fav.successRate + epsilon):
                    self.fav = bestAg
                else: True                    
            else:
                self.fav = None
        

#################################################################
### Collective Weighted Average Meta-Inductivist.
### Die MIs dieser Sorte haben keinen Favoriten mehr.
### Daher muss auch spezielle predict-Funktion definiert werden.
##################################################################

class WeightAv(Predictor):
 
    def __init__(self, name="WeightAv"):
        Predictor.__init__(self, name)
        self.idealabsucc = 0.0
        self.idealsuccessRate = 0.0
        self.attDict = {}
        self.idealprediction = 0.5

    def registeredBy(self, world):
        Predictor.registeredBy(self, world)
        # MetaInductivist.registeredBy(self, world)

#    def order(self, p):
#        return self.world.non_miList.index(p)
    
# createAttDict ist eine Funktion (ohne Parameter), zu unterscheiden vom
# Wert der Funktion attDict

    def createAttDict(self):
        self.attDict = {}
        self.idealabsucc += (1 - abs(self.world.event - self.idealprediction ))
        self.idealsuccessRate = (self.idealabsucc/self.world.round)
        for p in self.world.non_miList:
            order = self.world.non_miList.index(p)
            value = p.successRate - self.idealsuccessRate           
#            self.attDict['p.name'] = value
            self.attDict[order] = value
        return self.attDict

    def idealpred(self):
        if self.world.miList.index(self) > 0:
            self.idealprediction = self.world.miList[0].idealprediction
            return self.idealprediction
#für WeightAvMIColl order>1 nicht neu berechnet
        if self.world.round <= 1:
            idealprediction = 0.5
        else:
            Denum = 0.0
            Nom = 0.0
            for p in self.world.non_miList:
#                order = self.order(p)
                order = self.world.non_miList.index(p)
                if self.attDict[order] > 0:
#                   Nom = Nom + self.attDict[p.name]
                    Nom = Nom + self.attDict[order]
                    if p.prediction == 1:
                        Denum = Denum + self.attDict[order]
#                        Denum = Denum + self.attDict[p.name]
            if Nom == 0:
                idealprediction = 0.5
            else:
                idealprediction = (Denum/Nom)
        self.idealprediction = idealprediction
        return self.idealprediction

    def analyse(self):
        if self.world.miList.index(self) == 0:
            self.createAttDict()
        else:
            self.attDict = self.world.miList[0].attDict
# berechnet attDict nur einmal, beim ersten WeightAvMIColl


class WeightAvMIColl(WeightAv, CollectiveMI):
 
    def __init__(self, name="WeightAvMIColl"):
        WeightAv.__init__(self, name)
        CollectiveMI.__init__(self, name)

    def registeredBy(self, world):
        WeightAv.registeredBy(self, world)
        CollectiveMI.registeredBy(self, world)
        # MetaInductivist.registeredBy(self, world)

    def predict(self):
        idealprediction = self.idealpred()
        miNumber = len(self.world.miList)
        miPosNumber = round(miNumber * idealprediction)
        order = self.world.miList.index(self)
#        if order == 0: print idealprediction
        if (order + 1) <= (miNumber - miPosNumber):
            self.prediction = 0
        else:
            self.prediction = 1
        return self.prediction
 
        
             
########################################################################
#
#   Deceivers
#
########################################################################

AG_SUCCEED  = "succeed"
AG_FAIL     = "fail"


class Deceiver(Predictor):
    """Abstract base class for all deceivers. Deceiverss are predictors that
    try to lead meta inductivists into failure by predicting
    badly when they are favorites.

    Attributes:
        state       - indicates whether this deceiver will make succeeding
                      or failing predictions; can take the value of one
                      of the above defined constants: AG_XX
    """

    def __init__(self, name = "Deceiver"):
        Predictor.__init__(self, name)
        self.state = AG_SUCCEED

    def predict(self):
        if self.state == AG_SUCCEED: self.prediction = self.world.event
        else: self.prediction = invertEvent(self.world.event)
        return self.prediction

    def analyse(self):
        raise NotImplementedError
    


class SystOscillator(Deceiver):  
    """This forecaster is not a proper deceiver, but acts similar to a deceiver.
    It tries to get ahead of all other strategies and then
    conciously falls back in order to lead a meta-inductivist astray.
        It oscillates systematically independent of which other
        on-MI-players are present."""

    def __init__(self, name="Systematic Oscillator"):
        Deceiver.__init__(self, name)
        self.miFav = None

    def registeredBy(self, world):
        Deceiver.registeredBy(self, world)
        self.miFav = None

    def predict(self):
        return Deceiver.predict(self)

    def analyse(self):
        best = choice(bestOf(self.world.non_miList))
        if not self.miFav or \
           best.successRate > self.miFav.successRate: self.miFav = best
        if self.miFav == self: self.state = AG_FAIL
        else: self.state = AG_SUCCEED 



class Spy(Deceiver):   #Belassen bei 'Spy'. Ist der gewöhnlichste Deceiver
    """The spy checks the favorites of all meta inductivists.
    If it is a favorite of at least one of them it keeps failing,
    otherwise the spy will play perfect."""

    def __init__(self, name = "Spy"):
        Deceiver.__init__(self, name)

    def analyse(self):
        for mi in self.world.miList:
            if mi.fav == self:
                self.state = AG_FAIL
                break
        else:
            self.state = AG_SUCCEED
        
    
class InvMIDeceiver(Deceiver):    
    """A type of deceiver that issues a collective conspiracy against
    a defense of InvertedMIColls."""

    def __init__(self, name = "InvMIDeceiver"):
        Deceiver.__init__(self, name)

    def analyse(self):
        p = 0; n = 0
        for mi in self.world.miList:
            if isinstance(mi, InvertMIColl):
                if mi.fav == self:
                    if mi.invert:  n += 1
                    else:  p += 1
        if p > n:  self.state = AG_FAIL
        else:  self.state = AG_SUCCEED

# Diese Deceivers betrügen die WeightedAvMIColls
class AvDeceiver(Deceiver, WeightAv):

    def __init__(self, name = "AvDeceiver"):
        Deceiver.__init__(self, name)
        WeightAv.__init__(self, name)

    def analyse(self):
        order = self.world.non_miList.index(self)
        self.attDict = self.world.miList[0].attDict
        if self.attDict[order] > 0.05:
            self.state = AG_FAIL
        else: self.state = AG_SUCCEED

class AvDeceiver0(Deceiver, WeightAv):

    def __init__(self, name = "AvDeceiver"):
        Deceiver.__init__(self, name)
        WeightAv.__init__(self, name)

    def analyse(self):
        order = self.world.non_miList.index(self)
        self.attDict = self.world.miList[0].attDict
        if self.attDict[order] > 0:
            self.state = AG_FAIL
        else: self.state = AG_SUCCEED

class AvDeceiver1(Deceiver, WeightAv):

    def __init__(self, name = "AvDeceiver"):
        Deceiver.__init__(self, name)
        WeightAv.__init__(self, name)

    def analyse(self):
        order = self.world.non_miList.index(self)
        self.attDict = self.world.miList[0].attDict
        if self.attDict[order] > 0.1:
            self.state = AG_FAIL
        else: self.state = AG_SUCCEED

class AvDeceiver2(Deceiver, WeightAv):

    def __init__(self, name = "AvDeceiver"):
        Deceiver.__init__(self, name)
        WeightAv.__init__(self, name)

    def analyse(self):
        order = self.world.non_miList.index(self)
        self.attDict = self.world.miList[0].attDict
        if self.attDict[order] > 0.15:
            self.state = AG_FAIL
        else: self.state = AG_SUCCEED

class AvDeceiver0Lim9(Deceiver, WeightAv):

    def __init__(self, name = "AvDeceiver"):
        Deceiver.__init__(self, name)
        WeightAv.__init__(self, name)

    def analyse(self):
        order = self.world.non_miList.index(self)
        self.attDict = self.world.miList[0].attDict
        if self.attDict[order] > 0 or self.successRate > 0.9:
            self.state = AG_FAIL
        else: self.state = AG_SUCCEED

class AvDeceiver0Lim8(Deceiver, WeightAv):

    def __init__(self, name = "AvDeceiver"):
        Deceiver.__init__(self, name)
        WeightAv.__init__(self, name)

    def analyse(self):
        order = self.world.non_miList.index(self)
        self.attDict = self.world.miList[0].attDict
        if self.attDict[order] > 0 or self.successRate > 0.8:
            self.state = AG_FAIL
        else: self.state = AG_SUCCEED

class AvDeceiver1Lim8(Deceiver, WeightAv):

    def __init__(self, name = "AvDeceiver"):
        Deceiver.__init__(self, name)
        WeightAv.__init__(self, name)

    def analyse(self):
        order = self.world.non_miList.index(self)
        self.attDict = self.world.miList[0].attDict
        if self.attDict[order] > 0.1 or self.successRate > 0.8:
            self.state = AG_FAIL
        else: self.state = AG_SUCCEED

class AvDeceiver1Lim9(Deceiver, WeightAv):

    def __init__(self, name = "AvDeceiver"):
        Deceiver.__init__(self, name)
        WeightAv.__init__(self, name)

    def analyse(self):
        order = self.world.non_miList.index(self)
        self.attDict = self.world.miList[0].attDict
        if self.attDict[order] > 0.1 or self.successRate > 0.9:
            self.state = AG_FAIL
        else: self.state = AG_SUCCEED   
        
        
class AntiPunishDeceiver(Deceiver):     
    """A deceiver that tries to escape the punishing by reducing 
    deception rate as soon as recorded as deceiver.
    Berücksichtigt nicht den ultDeceiver-Status; ist bezogen auf
    den neutralizing/punishing MI"""
    
    def __init__(self, name = "AntiPunishDeceiver"):
        Deceiver.__init__(self, name)

# (lokale Variante)
#    def analyse(self):
#        for mi in self.world.miList:
#            if (mi.fav == self) and not mi.deceived(self):
#                self.state = AG_FAIL
#                break
#        else:
#            self.state = AG_SUCCEED

    def analyse(self):
        for mi in self.world.miList:
            if self in self.world.favlist and \
               not self in self.world.deceivers:
                self.state = AG_FAIL
                break
        else:
            self.state = AG_SUCCEED

"""Hinweis: führt dazu, dass Anti-Punisher schnell deception
status wechselt, bald als ultdeceiver eingestuft wird und dann
nur mehr richtig voraussagt. Passiert auch denn, wenn es mehr Anti-Punishers als
neutMIs gibt, weil jeweils ein anderer als Favorit dient und deceiver
wird"""


class AntiUltPunDeceiver(Deceiver):     
    """Berücktichtig den ultDeceiver Status. Sobald ultimate deceiver,
    wird er dennoch ge-punished. Es wird wieder globale Variante benutzt.
    "Führt dazu, dass Anti-Punisher schnell deception
    status wechselt, bald als ultdeceiver eingestuft wird und dann
    nur mehr richtig voraussagt. Passiert auch denn, wenn es mehr Anti-Punishers als
    neutMIs gibt, weil jeweils ein anderer als Favorit dient und deceiver
    wird"""
    
    def __init__(self, name = "AntiPunishDeceiver"):
        Deceiver.__init__(self, name)


    def analyse(self):
        for mi in self.world.miList:
            if self in self.world.favlist and \
               not self in self.world.alldeceivers:
                self.state = AG_FAIL
                break
        else:
            self.state = AG_SUCCEED


class AntiDeceiver(Deceiver):     
    """A potential deceiver that avoids being recognized as a deceiver after
    some rounds by calculating his future status w.r.t. MI.
    Der Algorithmus ist auch bei mehreren MIs sinnvoll,
    weil globale deception-Parameter, bezogen auf beliebige MIs, benutzt
    werden.
    Es handelt sich um keinen eigentlichen deceiver; dennoch muss er von der
    deceiver-class abgeleitet werden"""
    
    def __init__(self, name = "AntiDeceiver"):
        Deceiver.__init__(self, name)
        
    def analyse(self):
        if (self.world.round <= 10):
            self.state = AG_SUCCEED
            return

        future_favlist = [m.fav for m in self.world.miList]  
        if self in future_favlist:
            if not self.world.future_deceiveddown(self):
                self.state = AG_FAIL
#                print "favnodown"
                return
            else:
                self.state = AG_SUCCEED
#                print "favdown"
                return
        else:
            if not self.world.future_deceivedup(self):
                self.state = AG_SUCCEED
#                print "nofavnoup"
                return
            else:
                self.state = AG_FAIL
#                print "nofavup"
                return


########################################################################
#
#   Tests
#
########################################################################

def Simulation(title, predictorList, rounds = 500, visibleRange=(-1,-1),
               winTitle = "Indcution Simulation",
               eventFunction = lambda : getRandomEvent(2.0/3.0)):  

    win = wxGfx.Window(size=(800,600), title=winTitle)
    graph = Graph.Cartesian(win, 0, 0.0, rounds, 1.0,
                            title, "Round", "Relative Success")
    world = World(eventFunction)
    penBox = Graph.PenGenerator()
    for predictor in predictorList:
        world.register(predictor)
        pen = penBox.next()
        pen.thickness = win.MEDIUM
        graph.addPen(str(predictor), pen)

    for n in range(1,rounds+1):
        world.nextRound()
        for predictor in world.getPredictorList():
            graph.addValue(str(predictor), n, predictor.successRate)
        if n % (rounds / 10) == 0:  win.refresh()

    if visibleRange[1] >= 0:
        graph.adjustRange(visibleRange[0], 0.0, visibleRange[1], 1.0)
       
    win.waitUntilClosed()

    
               

def TestSuite():
    Simulation("Test 7",
               [
                Spy("A"),
                Spy("A"),
                Spy("A"),
                Spy("A"),
                Spy("A"),
                UltPunishMIColl(name = "MI"),
                PunishMIColl(name = "MI"),
                PunishMIColl(name = "MI"),
                PunishMIColl(name = "MI"),
                PunishMIColl(name = "MI"),
                PunishMIColl(name = "MI"),                
                ])


if __name__ == "__main__":
    import Gfx, wxGfx, Graph
    from wxPython.wx import *
    TestSuite()

    
