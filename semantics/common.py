#!/usr/bin/python3.0
# -*- coding: utf-8 -*-


"""
soooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo.................
An Abstraction consists of:
  Selbri
  Terms

A Selbri can be:
  A gismu
  A lujvo
  A tanru
  A fu'ivla
  A me {sumti}

Terms consist of:
  A term type
  A term value
A term type could be:
  LE SE SELBRI
  BAI (modal)
  me zoi xy.EXISTS.xy ("zasti"?)
A term value could be:
  An abstraction

Each abstraction will need a few different terms, no matter what its' selbri is!
  TRUTH (me zoi xy.TRUTH.xy)
    This is true.
    This is false.
  ACCORDING-TO (me zoi xy.ACCORDING-TO.xy)
  CONTEXT - Maybe not everything, but like... if you're holding separate conversations about cars, and someone asks, "which cars are blue" or something. Still... I think it'd be useful.
  ACL - the information of this abstraction is confidential to xACL
Also, there will need to be some non-zero amount of fake-selbri abstractions.
  me zoi xy.EXIST.xy: x1 exists
  


Suppose I turn on the server. These things will be loaded into the database on startup:
  {mi me zoi xy.EXIST.xy +TRUTH zo ja'a +ACCORDING-TO skami cevni}
This will be converted into...
{
  EXIST zo'e
  TRUTH zo ja'a
  ACORD la skami cevni (Or something like that...)
}
  

Now, suppose I type in:
> mi'e djeims .i mi nelci lo nu tavla lo mamta be la timos
{(EXIST)
  EXIST la djeims
  ACORD ri
  TRUTH zo ja'a
}
{(EXIST)
  EXIST la timos
  ACORD la djeims
}
{(mamta)
  mamta zo'e
  se-mamta la timos
  ACORD la djeims
}
{(tavla)
  se-tavla <lo mamta be la timos>
  TRUTH zo ja'a
  ACORD la djeims
}
{(nelci)
  nelci mi
  se-nelci <lo nu tavla lo mamta be la timos>
  TRUTH zo ja'a
  ACORD la djeims
}

oooooookay, I think I see how we can get NU stuff to work maybe...
Like SE <abstraction>, NU <abstraction>
"""



class Selbri:
  def __init__(self, selbri):
    self.selbri = selbri
    self.id = 0

class Abstraction:
  def __init__(self, selbri, places):
    self.selbri = selbri
    self.places = places


class Terbri:
  #A single terbri for some bridi
  def __init__(self, abstraction_id, place, value):
    self.abstraction_id = abstraction_id
    self.place_id = place
    self.value = value