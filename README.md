MetaInductionSim
================

A simulation of meta-induction based prediction strategies.
Meta-inductive prediction strategies are an approach that
has been proposed by Gerhard Schurz to answer the problem
of induction (also known as "Hume's problem" by philosophers).

Version: 0.5 

(c) 2007 by Eckhart Arnold & Gerhard Schurz, MIT Open Source License

Authors: Gehard Schurz (design of the simulation and meta-inductive
                        strategies)
         Eckhart Arnold (implementation in python and user interface)
web:    [https://www.phil-fak.uni-duesseldorf.de/philo/personal/thphil/schurz/](https://www.phil-fak.uni-duesseldorf.de/philo/personal/thphil/schurz/)
        [www.eckhartarnold.de](http://eckhartarnold.de)
email:  schurz@phil-fak.uni-duesseldorf.de
        eckhart_arnold@yahoo.de


What the simulation is about
----------------------------

In philosophy the problem of induction is understood as the problem to
justify the inference of future regularities or general laws (e.g. natural
laws)from observed past regularities (e.g. experimental evidence). The
18th century sceptic David Hume famously denied that induction could
be justified. Most subsequent philosophers found this hard to accept and
thinkers as important as Immanuel Kant and Karl Popper have proposed
solutions to the problem of induction. Today, however, experts agree that
none of these attempts has been successful. Therefore, the problem of induction is
still an area of active research. The meta-inductivist approach, proposed
by Gerhard Schurz, tries to answer the problem of induction not on the
object level (e.g. induction over recurring events in the world), but on the
meta level (e.g. rules for picking the best of various different inductive
strategies).

In order to develop his meta-induction approach, Gehard Schurz
designed computer simulations to study the characteristics of
meta-inductive strategies and to design new and types of
meta-inductive strategies. These simulations have been programmed by
me Python code in the years between 2003 and 2007. In order to
actually answer the problem of induction, it is of course necessary to
mathematically prove so-called "possibility theorems" about the
predictive power of meta-inductive strategies. This cannot be done by
a computer simulation alone. But computer simulations are great
heuristic tool in this context.

The meta-inductivist approach is discussed in-depth in the papers
listed below. For a short synopsis of simulation design, see sections
2 and 3 of the extended preprint of my paper, on:
http://eckhartarnold.de/papers/2009_Induktionsproblem/node2.html (I
had to take these passages out for publication, because the referees
considered a synposis of Schurz own presentation as unnecessary. While
I agree with that, the passages might still be helpful for the
beginner.)

 - Schurz, Gerhard. 2003. Der Metainduktivist. Ein spieltheoretischer
   Zugang zum Induktionsproblem. In Proceedings der GAP.5, Bielefeld
   22.-26.9.2003, ed. Roland Bluhm and Christian Nimtz. Gesellschaft
   für analytische Philosophie Paderborn: mentis Verlag
   pp. 243-257. URL: www.gap5.de/proceedings/pdf/243-257_schurz.pdf

 - Schurz, Gerhard. 2008. “The Meta-inductivist's Winning Strategy in the
   Prediction Game: A New Approach to Hume's Problem.” Philosophy of
   Science 75:278-305.

 - Eckhart Arnold: Can the Best-Alternative-Justification solve Hume's
   Problem? (On the Limits of a Promising Approach), in: Philosophy of
   Science 2010, 584-593, DOI: 10.1086/656010, URL (extended preprint):
   http://eckhartarnold.de/papers/2009_Induktionsproblem/Induktionsproblem.html

For an introduction to the problem of induction itself, I highly
recommend the respective chapter in Bertrand Russell's "The problems
of philosophy". Also, Nelson Goodman's "New Riddle of Induction" is
very important in this context. A more recent treatment is found in
Colin Howson's "Hume's problem".

Installing MetaInductionSim
---------------------------

Before you can run the simulation you need to install the following software
on your computer:

- **python2** which can by found on [www.python.org](www.python.org) . Beware,
  though, you need to use the old version, i.e. python2. I did not have time
  to port the programm to python 3, althouh I believe that this can easily
  be done.

- **wxPython** for the user interface, which can be downloaded from
   [www.wxpython.org](www.wxpython.org)

- there is also a jython user interface, but it only contains very few
  examples. Jython is the java virtual machine version of python, see
  [www.jython.org](www.jython.org). 

Finally, you need to clone the git repository of MetaInductionSim.


Running MetaInductionSim
------------------------

MetaInductionSim can be run, by starting either the wxPython or
jython/SWING user interface. In order to start the wxPython user
interface (recoommended) use the following command on the command
line:

    python2 Induction_Examples.py

You can pick different meta-induction scenarios from the menu then.

For the jython/SWING user interface, run:

    jython InductionApplet.py


Understanding MetaInductionSim
------------------------------

If you would like to analyze the simulation and the meta-inductive
strategies by reading the source code, I suggest leaving the user
interface code aside (it's pretty messy, anyway) but concentrating on
the simulation code in the file

    Induction.py

It is reasonably well documented with python docstrings to be understandable, I hope.


Extending MetaInductionSim
--------------------------

Back then when I wrote the simulation, I had to programm my own
library for graph plotting:
[PyPlotter](http://www.eckhartarnold.de/apppages/pyplotter.html)
. Because during the last ten years python has become increasinly
popular in the scientific community, there are much better plotting
libraries out there, nowdays.  Most probably a combination of
jupyter-Notebooks [jupyter.org](http://jupyter.org/) and the
matplot-Library [matplotlib.org](http://matplotlib.org/) would be the
best choice for anyone who would like to continue experimenting with
MetaInductionSim.

