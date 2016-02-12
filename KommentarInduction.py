# -*- encoding: UTF-8 -*-
# Induktionsalgorithmen


import random

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
                          of each strategies when it is being used
                          by any MI
        deceivers       - list of deceivers (updated after each round before the
                          analyse-methods are called)
        nondeceivers    - list of nondeceivers (updated after each round before the
                          analyse-methods are called)
        ultdeceivers    - list of three times out deceivers 
        nonultdeceivers - list of non three times out deceivers
        alldeceivers    - list of deceivers and ultdeceivers
        nonalldeceivers - list of non alldeceivers 
        favlist         - list of favorites of some MI (updated after each round before the
                          analyse-methods are called)
        worldDeceived   - A variable taking as its values the predictor that
                          is deceived by the world (the world can only deceive one
                           predictor at a time) or None, if there is no world
                          deception. 
        self.deceiveCount - ein dictionary das Anzahl der switches für jeden
                            non_MI von NichtbetrügerStatus auf BetrügerStatus einträgt.
        self.deceiveState - ein dictionary das den jeweils vorherigen betrügerStatus
                            - non_MI war deceiver oder nicht-deceiver einträgt"""
        
#Step 6: die Klasse Induction.World wird initialisiert, und unten sämtliche predictors
# des Examples, das von Klasse "sim" übergeben wird, werden bei dieser Klasse World
#registriert; siehe unten. Dabei werden die non_miList und die miList gebiltet; die
# nondeceivers werden voreingestellt. Mit "registeredBy" wird ausserdem die Klasse world
#zur Klasse self.world jedes Predictors gemacht 

#Das folgende erzeugt die Instanz "self" der Klasse "World"
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
#würde "register" abbrechen, wenn self.round > 0 ist,
# dient nur der Programmsicherheit

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
                
#Frage: wann muss bei "def -Funktion-" eigentlich zum Schluss ein Befehl
    # "return --- " stehen: wenn x = class.function() gesetzt wird, dann ja.
#wenn nur class.function() befohlen wird, dann nicht.

#Step9: "nextRound" wird von der Klasse "Sim" für alle n zwischen 1 und rounds (Rundenzahl)
#aufgerufen. Zunächst wird self.round um 1 erhöht; erste Runde = 0+1 = 1.
# Dann wird das self.event erzeugt; gehört auch noch zu Step9.
    def nextRound(self):
        """Generate a new event. Let the predictors make their
        predictions and evaluate their predictions, i.e. update
        the variables storing the absolute success rate as well
        as the relative success rate. Update the event frequency
        rates. Finally, call the predictors analyse method.
        """
        self.round += 1

# Grundsätzlich wird Event festgelegt,bevor predictors ihre Voraussagen machen,
#damit die Clairvoyants auf Events zugreifenb können; die können ja in Zukunft
#sehen. Für gewisse Zwecke ist dies dagegen hinderlich. ZB wenn die Events den OI
#betrügen, müssten die Events eigentlich von OI Vorhersage wissen.
#Diese Probleme werden dann speziell gelöst.

#wenn self.worldDeceived an ist, wird der angegebene MI genau dann von Events betrogen,
# wenn er entweder auf OI setzt oder randomguess macht.
# Per default wird der erste Mi betrogen.
#Falls der betrogene MI auf OI setzt, müssen die Events so sein, dass sie den
#OI betrügen, denn dessen Vorhersagen sind durch bisherige Events determiniert.
#Dh ich kann betrug des OI simulieren, wenn ich Example wähle, indem nur
#ein OI und ein MI vorkommt.

        if self.worldDeceived:
            if isinstance(self.worldDeceived.fav, ObjectInductivist):
                if self.relFrequency > 0.5:
                    self.event = 0
                elif self.relFrequency < 0.5:
                    self.event = 1
#trotz der folgenden Klausel wird OI auch in diesem Fall betrogen, siehe bei OI
                else:
                    self.event = getRandomEvent(0.5)
            elif self.worldDeceived.fav == None:
                self.event = getRandomEvent(0.5)
# oben: wenn der deceived MI keinen fav hat, geht event auf random event, und
# der MI sagt immer das Gegenteil davon voraus. Damit wird simuliert, dass
# dann eigentlich der MI randomguess mit 0.5 macht, und die Events immer das
#Gegenteil davon realisieren.
#Jetz erst kommt der Normalfall:
        else:
            self.event = self.getEvent()

            
# Step10: zuerst sagen non-mi's voraus, und ihre SUccess Records werden
#einfachheitshalber zugleich upgedated. Dann erstdie mi's, weil
# die mi's auf Vorhersagen der non-mi's zurückgreifen.
# Dabei wird davon ausgegangen, dass die Analyse-Funktion den Favoriten
# bzw. die Vorhersagestrategie speziell weighAvMI gibt es keinen Favoriten,
#daher wird hier durch analyse das AtraktivitätsDictionary erzeugt.
#Noch schwieriger bei TTB, der seinen Favoriten erst aufgrund der neuen Voraussagen der
#nonMis machen kann; weil er wissen muss, wer eine Vorauissage gemacht hat. Daher
#werden hier die alten SuccessWerte durch Analyse übergeben.

        for predictor in self.non_miList + self.miList:
#Hier wird die predict-Funktion mit Parametern des Predictors aufgerufen.
#Sie bezieht sich zumeist auf das Resultat der Analyse-Funktion der vorigen Runde.
#Danach werden die Success-Records upgedated.
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
        
#Step10: nun werden die ControlDictionaries aktualisiert. Siehe unten
        self.updateControlDictionaries()

#Nun folgt die Analyse-Funktion, die aufgerufen wird für jeden Predictor.
# Die non-MI-predictors haben bei analyse oft "pass" stehen.
# zuerst analyse für mi's, dann erst für non-mi's, weil non-mi's
# wissen müssen, ob sie fav's sind.
        for predictor in self.miList + self.non_miList:
            predictor.analyse()
#An dieser Stelle ist die Definition von "nextRound" erst zu Ende. Damit ist Step10
#der letzte Programmschritt pro Iteration.


#Im folgenden werden nur globale Parameter, zB globale DeceiveParameters festgelegt,
#die unabhängig sind von einem bestimmten MI. Wichtig für Globale Collective Strategien.
#Bei LocalDeceptiondetection, LocalAvoidance etc wird das für jeden MI speziell
#in einer Klasse gemacht. Die Global-versionen sind ab er wichtiger.
#self ist hier also immer noch "world"
            
    def updateControlDictionaries(self):
        self.favlist = [m.fav for m in self.miList]
        self.deceivers = []
        self.nondeceivers = []
        for p in self.non_miList:
            if p in self.favlist:
#favN ist das Dictionary, das für jeden Favoriten die Anzahl von Runden als er Favorit
#war bestimmt, als Eintrag zu seinem Namen
#absucc ein Dictionary, dass als Eintrag seinen absoluten Success solange er Favorit
#war, einträgt
                self.favN[p.name] += 1
                if p.prediction == self.event:
                    self.absucc[p.name] += 1
# deceivers ist die aktuelle Liste der Deceivers; und nondeceivers die der NonDeceivers.
# die deceived-Funktion mit Parameter des predictors wird weiter unten definiert
#ebenfalls die ultdeceived-Funktion
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


# Mit der deceptionRule werden unten die Prädikate deceived(p),
# future_deceiveddown, future_deceivedup (für Antideceivers) und
#ultdeceived definiert. Daher hat dieses Prädikat eine variable Rundenzahl,
# n - steht für Anzahl mit der gegebenen non_MI fav war, 
# absucc ist der absolute success des gegebenen non_MI während a fav war
# sucess ist der absolute success des gegebenen non_MI
# Achtung "absucc" ist hier lokale Variable, bedeutet was anderes als "absucc" oben:
#ebenfalls für "success" -- sehr unschön
#Division furch float(n) bewirkt, dass eine reelle zahl eruegt wird; absucc/n würde nur
#Integer erzeugen. Achtung: der ganze nenner ist in "float" einzuklammern.
#"deceptionRule" is wahr wenn geg. non_MI mit geg. Parametern Betrüger ist

    def _deceptionRule(self, round, n, absucc, success):
        if n <= 5:
            return False
        condSuccRate = absucc / float(n)
        if hardrule:
            if (round - n) <= 5:  return False
            invSuccRate = float(success - absucc) / float(round - n)
            return invSuccRate > condSuccRate + epsilonD
# hier oben wird eine Bedingung zurückgegeben, die wahr oder falsch sein kann
        else:
            succRate = success / float(round)
            return (succRate > condSuccRate + epsilonD or succRate < epsilonD)
# wozu wird die succRate hier neu bestimmt: weil sie auch bei future_Anwendung
# gebraucht wird. Die Or-Bedingung ist neu: sie verhindert, dass non-MIs automatisch
# nicht-deceivers werden, wenn ihre succRate < epsilonD ist; sie bleiben dann Betrüger.
        
# Globale FutureDeceived Funktion für systematic Deceivers bzw. AntiDeceivers
# bedeutet: wenn non-MI namens "a" nächstes Mal richtig vorhersagen würde,
# würde er ein globaler deceiver sein. Wird nur erzeugt wenn a NICHT fav ist
#absucc[a.name] ist der absucc-Wert von a während er fav war im Dictionary "absuccc"
#a.success ist sein absoluter success, der unter "predictor-Klassen" gebildet wird.
# Dort heisst absoluter success "predictor.success" und relativer success
# "predictor.successRate". a.success würde um 1 steigen. Aber da er nicht fav
#ist, steigt weder favN[a.name] noch absucc[a.name]
    def future_deceivedup(self, a):
        return self._deceptionRule(self.round+1,
                                   self.favN[a.name],
                                   self.absucc[a.name],
                                   a.success+1)
        

#future_deceiveddown wird nur gebildet, wenn a fav ist, und wenn a daher
#falsch voraussagen würde.
    def future_deceiveddown(self, a):
        return self._deceptionRule(self.round+1,
                                   self.favN[a.name]+1,
                                   self.absucc[a.name],
                                   a.success)

# die gewöhnliche deceived-Funktion, die generell von MIs mit globaler
#Deception-Detection benötigt wird.
    def deceived(self, a):
        return self._deceptionRule(self.round,
                                   self.favN[a.name],
                                   self.absucc[a.name],
                                   a.success)

#die ultimate-deceived-Funktioin, wird vom ultAvoidMI benötigt.
    def ultdeceived(self, a):
        if self.deceiveCount[a.name] >= 3:
            return True
        else:
            if self.deceived(a):
# der Betrügerstatus (ja/nein) der letzten Runde steht im Dictionary "deceiveState"
#als Eintrag von "a". War der falsch, dann wird im Dictionary "deceiveCount" der Wert
#von "a" um 1 erhöht -- der Wert der BetrügerStatus-Switches. Und, der Eintrag im
#Dictionary "deceiveState" wird aktualisiert; d.h. auf wahr gesetzt. Das passiert nur
#beim Switch von Nicht-Betrügen auf Betrügen.
#Falls oben deceiveCount[a.name] schon grösser-gleich 3 ist, dann ist "ultdeceived"
#wahr für "a" und bliebt immer wahr.
                if not self.deceiveState[a.name]:
                    self.deceiveCount[a.name] += 1
                self.deceiveState[a.name] = True
            else:
                self.deceiveState[a.name] = False
        return False     

#damit ist Definition von "updateControlDictionaries(self)" zu Ende.
########################################################################
#
#   Predictor classes
#
########################################################################


#Hier werden gemeinsame Eigenschaften unterschiedlicher Klassen von Voraussagespieler
#in jeweiligen Oberklassen zusammengefasst.

class Predictor(object):
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

# diesen Befehl benutzt die Print-Funktion der Klasseninstanz. Soe druckt statt des
#Namens den Namen plus SUffix aus, wenn self-suffix >=1, dh es gibt mehr als
#einen Voraussager der jeweiligen Klasse.
    def __str__(self):
        if self.suffix >= 1: return self.name+" "+str(self.suffix)
        else: return self.name
   
#Klasseninstanz wird hier mit teilweise variablen Werten name und "" angelegt;
#unten wird PredictorKlasse bei world registriert; dort werden dann Nahmen
#shortname bestimmt.
    def __init__(self, name):
        self.name = name
        self.short = ""
        self.suffix = 0
        self.world = None
        self.success = 0
        self.successRate = 0.0
        self.prediction = 0


#Dies bestimmt Kurznamen.
# Short name = max 3 Buchstaben, Grossbuchstaben oder Zahlen
#nur gebraucht in SimWindow
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

#Dies bestimmt Suffix
#bei Namenskonflikten wird Nummer als Suffixangehängt
#wenn in exampleList schon nummriert, dann wird das nicht benötigt
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
        

# die predict-Funktion darf nur in den Unterklassen aufgerufen werden, wo sie
#spezifiziert ist. Wäre in Examplelist ein unspezifischer Predictor, würde hier
#das Programm abbrechen. -- Denn: jeder Voraussager muss was voraussagen.
#die Analyse-Funktion unten wird übergangen; ebenfalls in Unterklassen aufgerufen.

    def predict(self):
        """Predict the next event."""
        raise NotImplementedError

    def analyse(self):
        """Possible analysis of results after the prediction cycle
        is finished.
        """
        pass
        

#diese Funktion wird schon hier definiert: gibt liste der links-nach-rechts-gereihten
#Besten der predictorList
# wenn diese Liste leer ist, wird Programm abgebrochen.
#Ohne "assert" würde dies im Fall leerer predictorList die leere Liste zurückgeben.
    
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


#das folgende wird nur für die InvertMIColl benötigt.
#Könnte also fast sinnvoller dort stehen, oder 
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
durchgeführt wird, darf dieser RandomGuess als Favorit nur verwendet werden, wenn
worldDeceived None ist, Wird fast nie verwendet"""

class RandomGuess(Predictor):
    """Random Guess Strategy."""

    def __init__(self, name = "Random Guess"):
#nun wird entsprechende Oberklasse initialisiert. Geschieht in folgenden immer
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
# self.prediction wird voreingestellt, weil sie erst durch analyse-Funktion
# festgelegt wird; in erster Runde liefert die noch keinen Wert

    def predict(self):
        if self.world.worldDeceived and (self.world.round == 1\
        or self.world.relFrequency == 0.5):
            self.prediction = invertEvent(self.world.event)
#Erläuterung: wenn worldDeceived on, wurden Events so bestimmt, dass OI wenn er
# wie gewöhnlich voraussagt
#und fav des betrogenen MI ist, das Gegenteil voraussagt. In erster Runde ist OI immer
#der fav des world-betrogenen MI. Ausnahmen liegen nur vor,
#wenn entweder erste Runde vorliegt, also noch keine Eventfrequencies, oder wenn
#Eventfrequencies auf genau 0.5 liegt; dies tritt nur ein wenn OI der fav des
# world-betrogenen MI ist. In diesem Fall sind Events random(0.5). 
# self.prediction von OI wird in diesem Fall in erster Runde wird überschrieben.  
        return self.prediction

#die analyse-Funktion liefert die gewöhnluiche predict-Funktion des OI.
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
#oben: anstelle des"%" wird der Wert von "successAim" auf 2 Kommastellen gesetzt
        self.successAim = successAim
        
    def predict(self):
        if randomBool(self.successAim): #randomBool(x) liefert einen W.wert 1 mit W.keit x, sonst 0
            self.prediction = self.world.event
        else:
            self.prediction = invertEvent(self.world.event)
        return self.prediction


#Die Klasse ForecasterFromBottom sollte beser mit variabler Delay-Zahl definiert
#werden, analog wie "DelayedForecaster" abgeleitet von "Forecaster; aber
#nicht mit successRate  0 0.5 während Delay, sondern mit successRate = 0
class ForecasterFromBottom(Predictor):
    """A prediction strategy that is successfull at a predifined rate.
        after a 70 rounds; so its successRates comes "from bottom"
    Attributes:
        successAim      - the predifined success rate this
                          Forecaster shall reach
    """

    def __init__(self, successAim, name="Forecaster"):
        Predictor.__init__(self, name + " %.2f" % successAim)
        self.successAim = successAim
        
#Hinweis: der Wert ">70" kann hier variable verändert werden
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
            self.delay -= 1   #1 wird von self.delay abgezogen
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

#Das folgende ist nur die Oberklasse der Oszillatoren
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
    


#Oszilliert zwischen zwei Amplituden. Ist daher ein contingent deceiver.
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
        

#Oszillator mit ficierter Periode; die Amplituden schrumpfen daher.
#Ebenfalls kontingent Deceiver
class PeriodOscillator(Oscillator):
    """An oscillator with a fixed period but (necessarily)
    diminishing amplitude.

    Attributes:
        halfperiod          - half of the period length in rounds
        shift               - phase shift at the beginning in rounds
    """

    def __init__(self, halfperiod, shift, name = "Period Oscillator"):
        Oscillator.__init__(self, name)
        self.name = name + " " + str(halfperiod) + " " + str(shift)
        self.halfperiod = halfperiod
        self.shift = shift % (2*halfperiod)
# dies ist die module-Operation: gibt den Rest der Division shift / 2*halfperiod aus.
        if self.shift >= halfperiod:  self.phase = OSC_DOWN
        else: self.phase = OSC_UP
        
    def analyse(self):
        s = (self.world.round+self.shift) % (2*self.halfperiod) 
        if s >= self.halfperiod:  self.phase = OSC_DOWN
        else: self.phase = OSC_UP


#Zwei gegenläufig gekoppelte Oszillatoren mit fixer Amplitude; dh anwachsender
#Periode. Weil steigen bei SuccessRates > 0.5 langsamer dauert als sinken,
#müssen Wartephasen eingebaut werden.
# in ExampleLIst kein coupledOscillator. Wie müsste "combo" denn eingetragen
#werden: normal als Coupled Oscillator

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
#der Combo wird idendifiziert; die Phasen werden anfangs gegengerichtet; überschrieben
#diese Klausel setzt voraus, dass es genau zwei CoupledOscillators gibt
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
#WAITTOP = wahr bewikt, der Oscillator sagt mit Rate self.max richtig voraus
#bei WAITBOTTOM mit Rate self.min
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
        phaseLimit  - the number of half period changes until
            its behavior changes from an amplitude oscillator
            to a Forecaster
        phaseCounter - the actual number of half period chagnes
        oscState    - the state (up or down) of the current
            phase
            
    Note: the parameter maxPhase of the constructor __init__
    takes the number of full phases, while the object variables
    phaseLimit and phaseCounter use half phases!
    """
    def __init__(self, minv, maxv, maxPhases, successAim, 
                 name = "OscDelayedForecaster"):
        Forecaster.__init__(self, successAim, name)
        AmplitudeOscillator.__init__(self, minv, maxv, name)
        self.phaseLimit = maxPhases*2  
        self.phaseCounter = 0
        self.oscState = self.phase
#self.phase wird bei AmplitudeOscillator bestimmt.
        
    def predict(self):
        if self.phaseCounter < self.phaseLimit:
            return AmplitudeOscillator.predict(self)
        else: return Forecaster.predict(self)
        
    def analyse(self):
        if self.phaseCounter < self.phaseLimit: 
            AmplitudeOscillator.analyse(self)
        else: Forecaster.analyse(self)
#self.oscState merkt sich frühere self.phase
#beim Wechsel der self.phase wird phaseCounter um 1 erhöht
        if self.oscState != self.phase:
            self.phaseCounter += 1
            self.oscState = self.phase

        
                           
########################################################################
#
#   Meta-Inductivists
#
########################################################################

#Metainduktivisten hier sind solche im engen Sinne: d.h. die nur EINEN Favoriten
#haben. Die Klassen WeightAv und WeightAvMIColl sind Metainduktivisten im weiteren
#Sinne, die sich aber nicht von MetaInductivist-Klasse sondern direkt von
#Predictor-Klasse ableiten.

class MetaInductivist(Predictor):
    """Follow the most successful strategy so far.

    Attributes:
        fav         - the current favorite of the meta inductivist
    """
    def __init__(self, name = "Meta Inductivist"):
        Predictor.__init__(self, name)
        self.fav = None
#zuerst haben sie keinen Favoriten; denn ein OI muss nicht dabei sein.
        
    def registeredBy(self, world):
        Predictor.registeredBy(self, world)
        self.fav = None

    def predict(self):
        if self.fav:    #wenn MI einen Favoriten hat; das ist Normalfall
            self.prediction = self.fav.prediction
# hier war ein Fehler drin; die nachgetragene Klausel "and not" fehlt
# das folgende tritt nur ein, wenn MI keinen Favoriten hat. das ist in erster
#Runde der Fall, oder wenn alle non_MIs Betrüger sind.
#In erster Runde sucht sich MI den OI als Favorit, falls ein solcher da ist.
#wenn world.worldDeceived == self wird OI von Events betrogen, falls er Fav von MI ist.
#wenn nicht, hängt es von world.worldDeceived == self ab.
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

# self.world.non_miList = Liste aller Predictors, die keine MIs sind
# bestof(Liste) gibt Liste der besten Strategien zurück.
# choice wählt Element der Liste der Gleichguten links-nach-rechts aus
# man könnte choice Funktion im Eingang des Programms wechseln
# self-fav == None tritt nur in erster Runde ein -- ausser bei DeceptionDetection
# Hinweis:  Befehl funktioniert nur, wenn self.world.non_miList nichtleer ist.
# Das könnte man noch ändern. 
#Bislang: der spezielle deceiver-Fall wird separat abgehandelt;
#mit der speziellen Analyse-Funktion.
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

#die predict-Funktion wird von Oberklasse übernommen. non_miList ist wieder nichtleer.

    def analyse(self):
        candidate = choice(bestOf(self.world.non_miList))
        if self.fav == None or \
           candidate.successRate > self.fav.successRate + epsilon:
            self.fav = candidate


###################################################################
#### Die folgende Klasse wird nur für lokale Deception-Detection benötigt,
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
#verwendet nur der LocalAvoidMI


    def succ(self, a):
        """Return the relative success of 'a' while MI has put on 'a'."""
#das self.control Dictionary wird unter "analyse" aufgebaut; wird hier eingelesen
        n, absucc = self.control[a.name]
        if n == 0:  return 0.0
        else:  return float(absucc) / float(n)
        
    def nsucc(self, a):
        """Return the relative success of 'a' while MI has not put on 'a'."""
        n, absucc = self.control[a.name]
        if self.world.round == n:  return 0.0
        else:  return float(a.success - absucc) / float(self.world.round - n)
            
    def deceived(self, a):
        """return True if MI is at the given time deceived by 'a'.
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
#das "try" ist eine Vorsichtsmassnahme: falls verletzt, würde Programm abbrechen ??

            
# die folgenden zwei Funktionen sind lokale future-deceived Funktionen, relativ zu
#einem gegebenen non_Mi "a", und würden nur benötigt werden, wenn local AntiDeceivers
#eingeführt werden, die für alle oder nur bestimmte MIs vermeiden,dass sie als
#Deceivers erkannt werden
def future_deceiveddown(self, a):
        """return True if MI would be recognized as deceiver of by 'a', if
        a predicts wrongly in the next round and is favorite.
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
        """return True if MI would be recognized as a deceiver of 'a', if
        a predicts correctly in the next round and is not favorite.
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

#diese Klasse leitet sich von zwei Oberklassen ab
class LocAvoidMI(EpsilonMetaInductivist, DeceptionDetectionMixin):
    def __init__(self, name="LocAvoidMI"):
        DeceptionDetectionMixin.__init__(self)        
        EpsilonMetaInductivist.__init__(self, name)

    def registeredBy(self, world):
        EpsilonMetaInductivist.registeredBy(self, world)
# bei der EpsMetaInd-OberKlasse wird die Welt registriert. Hier steht das nur zur Sicherheit,
#weiles zwei Oberklassen gibt; das wird ohnedies bei EpsMetaInd gemacht.

#in folgender Def wird im Effekt in Runde 1 durch "_registered"        
#das disctionary auf 0,0 gesetzt und vorausgesagt was epsilonMI voraussagt
    def predict(self):
        if self.world.round == 1:
            DeceptionDetectionMixin._registered(self)
        return EpsilonMetaInductivist.predict(self)  
# Hinweis zur predict-Funktion: für Runden > 1 wird sie von EpsilonMI geholt,
#und der holt sie sich vom normalen MI.
# Der Fav kann diesmal auch den Wert "None" erhalten; wird in "analyse"
#zugewiesen.

    def analyse(self):
        DeceptionDetectionMixin._analyse(self)
#das Dictionary wurde eingelesen
        if (self.world.round % 100) < 5:
#gibt alle 100 Runden neue Chance 5 mal, indem er wieder auf besten setzt.
#der kann so seine konditionalen Success hochtreiben und wieder zum non-deceiver werden.
#Achtung bringt nichts für die meisten non-MIs denn der aMI
#geht ja nur auf den besten non_MI
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


# weitere Hinweise zum obigen:
# deception Recording erst nach n=5 Runden...
# SoftDecRec:  | Succ(Ai,n) - Succ(Ai,n | MIj puts on Ai) |> epsilonD
# gibt dem Ai immer wieder eine Chance, weil die Anzahl von Runden wo MIj auf Ai setzt,
# verschwindend gering wird im Vgl. zu den Runden, wo das nicht der Fall ist,
# und daher im Quotient untergeht
# HardDecRec:|Succ(Ai,n| nicht MIj puts on Ai) - Succ(Ai,n | MIj puts on Ai)|> epsilonD


#Jetzt folgt der globale AvoidMI
class AvoidMI(EpsilonMetaInductivist):
    def __init__(self, name="AvoidMI"):     
        EpsilonMetaInductivist.__init__(self, name)

    def registeredBy(self, world):
        EpsilonMetaInductivist.registeredBy(self, world)

    def analyse(self):
#spielt wie PunishMIColl wenn nicht neutralizing
#ausser gibt immer wieder neue Chance. Das habe ich hier aber auf eliminiert,
#indem ich Wert "<0" gesetzt habe
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
            else: True    #hier wird self.fav einfach beibehalten                  
        else:
            self.fav = None  #gibt es keine nondeceivers, wird self.fav auf None gesetzt.


class UltAvoidMI(EpsilonMetaInductivist):
    def __init__(self, name="AvoidMI"):     
        EpsilonMetaInductivist.__init__(self, name)

    def registeredBy(self, world):
        EpsilonMetaInductivist.registeredBy(self, world)

    def analyse(self):
#wieder wurde "neue Chance" auf "<0" gesetztM d.h. eliminiert
        if (self.world.round % 100) < 0:
            candidate = choice(bestOf(self.world.non_miList))
            if self.fav == None \
               or candidate.successRate > self.fav.successRate + epsilon:
                self.fav = candidate
            return
        
#alldeceivers sind aktuelle deceivers sowie jene ultimate deceivers, die
# aktuell keine deceivers sind      
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
    together as a coordinated group.

    Attributes:
        order       - the order number of the meta inductivist, e.g.
                      if this MI is MI3 then order will be 3
        cmiList     - a list of the other collective meta inductivists
                      (of the same class) in the world with a lower order
    """
    
#Hinweis: die cmiList wird nur für die Inverted MIColls benötigt.
# die self.order hätte bei WeightAvMIColl abgerufen werden können,
#wird aber durch durch Funktion "index" neu berechnet.
#PunishMIColl benötigt auch die self.order

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
Hinweise: ein MI setzt invertiert auf einen Fav, wenn er den Favoriten Fav eines
MI invertiert benutzt, der selbst sehr schlecht voraussagt.
nach wie vor haben die InvertMIs nur non_MIs as Favoriten, aber evtl. invertiert
Die Ornung der InvertMIs und cmiList ist nötig, denn sonst könnten Zirkel
entstehen: MI1 setzt invertiert auf MI2.fav, und MI" invertiert auf MI1.fav; dann
#wäre der fav von beiden unbestimmt.
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
#der erste InvertMI spielt wie ein gewöhnlicher epsilonMI
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


class PunishMIColl(CollectiveMI):
#"Punish" sollte eigentlich "Neutralization" heissen. Benutzt globale Parameter
    """A collective defense which uses global deception dection to
    protect itself. The MIs "punish" the decivers, or better neutralize
    them, by putting on the deceivers in a 1:1 manner as long as they deceiver.
    The MIs not needed for neutralization/punishment act like ordinary eMIs.
    """    
    def __init__(self, name="Punish"):  
        CollectiveMI.__init__(self, name)

    def registeredBy(self, world):
        CollectiveMI.registeredBy(self, world)

    def analyse(self):
#die folgende if-Klausel kann man weglassen; die deception recording setzt ohnedies
#erst nach einigen Runden ein.
        if self.world.round < 10:
            candidate = choice(bestOf(self.world.non_miList))
            if not self.fav or \
               candidate.successRate > self.fav.successRate + epsilon:
                self.fav = candidate
            return

#PunishMIColl benötigt auch self.order
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
#wieder könnte man diese if-Klausel weglassen
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
### und sie leiten sich direkt von Predictor ab; nicht von MetaInductivist
##################################################################

class WeightAv(Predictor):
#In dieser Klase wird idealprediction berechnet. Würden reelle Zahlen vorausgesagt
#werden, so würde diese Funktion genügen.  Den eigenen Stellenidex bräcjte man nicht.  
 
    def __init__(self, name="WeightAv"):
        Predictor.__init__(self, name)
        self.idealabsucc = 0.0
        self.idealsuccessRate = 0.0
        self.attDict = {}
        self.idealprediction = 0.5

    def registeredBy(self, world):
        Predictor.registeredBy(self, world)
# Hinweis: registeredBy ist hier überflüssig! Wird ohnedies in
# Oberklasse getan. world wird als self.world eingetragen. Nur wenn registeredBy
#Funktion zusätzlich spezielle Dinge macht, ist das nötig.

    
# createAttDict ist eine Funktion (ohne Parameter), zu unterscheiden vom
# Wert der Funktion attDict
# die analyse-Funktion steht bei deiser Klasse; die WeightAvMIColl hat nur eine
#predict Funktion, keine analyse Funktion.
#die Funktion createAttDict wird jeweils beim ersten WeightAvMIColl pro Runde
#einmal aufgerufen.

    def createAttDict(self):
        self.attDict = {}
# abs gibt den Absolutbetrag.
        self.idealabsucc += (1 - abs(self.world.event - self.idealprediction ))
        self.idealsuccessRate = (self.idealabsucc/self.world.round)
        for p in self.world.non_miList:
#List.index(p) gibt den Stellenindex des Elements p der Liste List, beginnend mit 0.
            order = self.world.non_miList.index(p)
            value = p.successRate - self.idealsuccessRate           
            self.attDict[order] = value
        return self.attDict

    def idealpred(self):
#für WeightAvMIColls mit order>1 wird self.idealprediction nicht neu berechnet,
#nur beim ersten WeightAvMIColl mit Index 0.        
        if self.world.miList.index(self) > 0:
            self.idealprediction = self.world.miList[0].idealprediction
            return self.idealprediction
        if self.world.round <= 1:
            idealprediction = 0.5
        else:
            Denum = 0.0
            Nom = 0.0
            for p in self.world.non_miList:
                order = self.world.non_miList.index(p)
                if self.attDict[order] > 0:
                    Nom = Nom + self.attDict[order]
                    if p.prediction == 1:
                        Denum = Denum + self.attDict[order]
#der Nominator Nom = Summe der Attraktivitätswerte aller non_MIs, welche
# einen Attraktivitätswert > 0 haben. Der Denumerator summiert nur jede darunter                        
#auf welche 1 vorausgesagt haben.
#Falls der Numerator/Nenner ist, wird pr default wieder 0.5 vorausgesagtg
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
# berechnet wieder attDict nur einmal, beim ersten WeightAvMIColl


class WeightAvMIColl(WeightAv, CollectiveMI):
 
#Von zwei Oberklassen abgeleitet, daher müssen beide initialisiert werden.
    def __init__(self, name="WeightAvMIColl"):
        WeightAv.__init__(self, name)
        CollectiveMI.__init__(self, name)

    def registeredBy(self, world):
        WeightAv.registeredBy(self, world)
        CollectiveMI.registeredBy(self, world)

    def predict(self):
        idealprediction = self.idealpred()
        miNumber = len(self.world.miList)
        miPosNumber = round(miNumber * idealprediction)
#obiges rundet auf nächste Integerzahl auf oder ab.
        order = self.world.miList.index(self)
#der folgende auskommentierte Befehl dient zur Abfrage der idealpredictions
#        if order == 0: print idealprediction
        if (order + 1) <= (miNumber - miPosNumber):
            self.prediction = 0
        else:
            self.prediction = 1
        return self.prediction
#Im Effekt enstpricht Verhältnis der 1-VoraussagerMIs zu allen MIs dem vVerhältnis
#von PosNumber zu miNumber.

                     
########################################################################
#
#   Deceivers
# Damit sind systematische Deceivers gemeint
########################################################################

AG_SUCCEED  = "succeed"
AG_FAIL     = "fail"


class Deceiver(Predictor):
    """Abstract base class for all deceivers. Deceivers are predictors that
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
    


#Die folgende Klasse wird in ExampleList benutzt wo MI betrogen wird, der
#epsilonMI sich dagegen erholt. Wird benötigt, denn würde man dort
#den systematic deceiver verwenden, würde der auch den epsilonMI betrügen.
#Der SystOscillator greift nicht auf die fav's der MIs direkt zu, sondern
#berechnet sie sich selbst; gemäss der Regel der MI.    
    
class SystOscillator(Deceiver):  
    """This forecaster is not a proper systematic deceiver, but acts similar to a deceiver.
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
# man braucht diese predict-Funktion hier nicht: würde sich automatisch von Oberklasse
#Deceiver holen!

#self.miFav ist jeweils der beste non_MI; der Favorit der MIs.
#Anfangs auf None gesetzt.  

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

#p ist die Anzahl der InvertMIColls die positiv auf self setzen; n die ANzahl der
#InvertMIColls die invertiert auf ihn setzen. Der self betrügt so viele wie nöglich,
#dh abhängig von p>n oder nicht.
    def analyse(self):
        p = 0; n = 0
        for mi in self.world.miList:
            if isinstance(mi, InvertMIColl):
                if mi.fav == self:
                    if mi.invert:  n += 1
                    else:  p += 1
        if p > n:  self.state = AG_FAIL
        else:  self.state = AG_SUCCEED

        
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
# have ich ausgekomentiert:        for mi in self.world.miList:, sowie break
        if self in self.world.favlist and \
            not self in self.world.deceivers:
            self.state = AG_FAIL
        else:
            self.state = AG_SUCCEED

"""Hinweis: dies führt dazu, dass Anti-Punisher schnell deception
status wechselt, bald als ultdeceiver eingestuft wird und dann
nur mehr richtig voraussagt. Passiert auch denn, wenn es mehr Anti-Punishers als
neutMIs gibt, weil jeweils ein anderer als Favorit dient und deceiver
wird"""


class AntiUltPunDeceiver(Deceiver):     
    """Berücktichtig den ultDeceiver Status. Sobald ultimate deceiver,
    wird er dennoch ge-punished. Es wird wieder globale Variante benutzt.
    Führt wieder dazu, dass Anti-Punisher schnell deception
    status wechselt, bald als ultdeceiver eingestuft wird und dann
    nur mehr richtig voraussagt.
Das heisst: diese Variante entkommt dem ultimateAvoidance, bzw ultimate Punisher
nicht! """
    
    def __init__(self, name = "AntiPunishDeceiver"):
        Deceiver.__init__(self, name)


    def analyse(self):
        if self in self.world.favlist and \
            not self in self.world.alldeceivers:
            self.state = AG_FAIL
        else:
            self.state = AG_SUCCEED


class AntiDeceiver(Deceiver):     
    """A potential deceiver that avoids being recognized as a deceiver after
    some rounds by calculating his future status w.r.t. MI.
    Der Algorithmus ist auch bei mehreren MIs sinnvoll,
    weil globale deception-Parameter, bezogen auf beliebige MIs, benutzt
    werden.
    Es handelt sich um keinen eigentlichen deceiver; dennoch muss er von der
    deceiver-class abgeleitet werden
Diese Klasse ist wichtiger, um den AvoidanceMI und den PunishMI zu testen
    """
    
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


###########################################################################
###     Diese Deceivers betrügen die WeightedAvMIColls
### mit verschiedenen Parametern. Etwas unschön; sie sollten besser
### variable Parameter als Werte in Klammer haben
###########################################################################

            
class AvDeceiver(Deceiver, WeightAv):

#Die Idee: wenn die eigene Attraktivität einen gewissen Wert übersteigt,
#sagen die AvDeceivers das Falsche voraus. 

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

#Nun wird mit "Lim"-Angabe zusätzlich verhindert, dass die successRate dieses Deceivers
#einen gewissen Wert übersteigt

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

    
