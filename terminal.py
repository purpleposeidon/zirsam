# -*- coding: utf-8 -*-

#A fragment of my anti- curses.i'enai.ionairu'e cook-book
#No, not BNF-terminals, or elidable terminators

ESC = chr(27)
CSI = ESC+'['

class AsciiCode:
  """
  An ascii code is used to control the terminal. It can be created either like:
    AsciiCode(arg [, default=''])
  or
    AsciiCode(sequence='' [, default=''])
  By default, "arg" is prepended with "<Esc>[". If you pass sequence instead, it is prepended only with "<Esc>".
  If there is a '@' character, it is replaced with the value 'default' if the AsciiCode is passed to directly to print. However, if you call the asciicode object, it will expect an argument, and the '@' will be replaced with the given argument.
  """
  def __init__(self, *arg, sequence="", default=''):
    self.default = default
    if arg:
      self.sequence = CSI+arg[0]
    else:
      self.sequence = ESC+sequence
  def __str__(self):
    return self.sequence.replace("@", self.default)
  def __call__(self, *args):
    i = str(self.sequence)
    args = list(args)
    while '@' in i and args:
      i = i.replace('@', str(args.pop(0)), 1)
    if '@' in i or args:
      raise Exception("Argument count mismatch")
    return i


ClearLine = AsciiCode("2K")
ClearLineRight = AsciiCode("K")
ClearLineLeft = AsciiCode("1K")
ClearScreen = AsciiCode("2J")
TerminalReset = AsciiCode(sequence="c")
TerminalTitle = AsciiCode("2;@\007")
CursorHome = AsciiCode("H")
CursorUp = AsciiCode("@A") #Attempts to move cursor offscreen have no uffect
CursorDown = AsciiCode("@B")
CursorRight = AsciiCode("@C")
CursorLeft = AsciiCode("@D")
CursorSet = AsciiCode("@;@f") #Line, Col
CursorHide = AsciiCode("?25l")
CursorShow = AsciiCode("?25h")
CursorSave = AsciiCode("s")
CursorRestore = AsciiCode("u")

class Color:
  def __init__(self, fg=None, bg=None, attr=None):
    self.fg = fg
    if isinstance(bg, Color):
      #Can't set special foregrounds to background, sadly
      bg = bg.fg
    self.bg = bg
    self.attr = attr
  def __str__(self):
    #XXX I'm pretty sure that somehow you can do CSI attribute; attribute; attribute m
    r = ''
    if self.fg:
      r = CSI+str(self.fg.val)+'m'
    if self.bg:
      r += CSI+str(self.bg.derived+10)+'m'
    if self.attr:
      r += CSI+str(self.attr.val)+'m'
    return r
  def __repr__(self):
    print(str(self), end='')
    return repr(str(self))

class AttrNum:
  def __init__(self, val, derived=False):
    self.val = val
    if derived:
      self.derived = derived
    else:
      self.derived = self.val
  def __str__(self):
    return CSI+str(self.val)+'m'
  def __repr__(self):
    print(str(self), end='')
    return repr(str(self))
  def __or__(self, other):
    return AttrNum(self.val | other.val)
    #return AttrNum(self.val | other.val, derived=self.val)

#Styles
NORMAL = AttrNum(0)
BRIGHT = AttrNum(1)
UNDERLINE = AttrNum(4)
BLINK = AttrNum(5)
REVERSE = AttrNum(7)
BOLD = BRIGHT

#Base colors
BLACK = AttrNum(30)
RED = AttrNum(31)
GREEN = AttrNum(32)
BROWN = AttrNum(33) #"yellow"
BLUE = AttrNum(34)
PURPLE = AttrNum(35) #"magenta"
CYAN = AttrNum(36)
GRAY = AttrNum(37) #"white"

#Advanced colors (These can't be used in the background)
DARK_GRAY = Color(BLACK, attr=BRIGHT)
WHITE = Color(GRAY, attr=BRIGHT)
ORANGE = Color(RED, attr=BRIGHT)
LIGHT_GREEN = Color(GREEN, attr=BRIGHT)
LIGHT_BLUE = Color(BLUE, attr=BRIGHT)
YELLOW = Color(BROWN, attr=BRIGHT)
LIGHT_CYAN = Color(CYAN, attr=BRIGHT)
PINK = Color(PURPLE, attr=BRIGHT)






import io
import os
import sys
import atexit
import tempfile

import termios, fcntl, select, struct



def termsize():
  """ Returns the (height, width) of the terminal. Stolen from somewhere."""
  try:
    return int(os.environ["LINES"]), int(os.environ["COLUMNS"])
  except KeyError:
    height, width = struct.unpack(
      "hhhh", fcntl.ioctl(0, termios.TIOCGWINSZ ,"\000"*8))[0:2]
    if not height: return 25, 80
    return height, width 


my_fifos = []
def exists(what):
  #Use 'which' to check that a program exists
  return not bool(os.system("which {0} > /dev/zero".format(what)))


#Handle input stuff...
fd = None
oldterm = None
newattr = None
oldflags = None

#stolen termios voodoo code is stolen magic voodoo

@atexit.register
def cleanup():
  """Return terminal to sanity, remove plumbing"""
  if fd is None:
    return #It wasn't set up to begin with!
  termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm) #Stolen
  fcntl.fcntl(fd, fcntl.F_SETFL, oldflags) #Stolen
  



def term_setup():
  """Puts the terminal the way we want it. This code is also stolen."""
  global fd, oldterm, newattr, oldflags
  fd = sys.stdin.fileno()
  
  oldterm = termios.tcgetattr(fd)
  newattr = oldterm[:]
  newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
  termios.tcsetattr(fd, termios.TCSANOW, newattr)
  
  oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
  fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

def read_char(fd):
  #Somewhat stolen
  r, w, e = select.select([fd], [], [])
  if r:
    return sys.stdin.read(1)
  return ''

def quick_char(fd):
  r, w, e = select.select([fd], [], [], .01)
  if r:
    return sys.stdin.read(1)
  return ''

def peek_char(stdin, c=0):
  return stdin.buffer.peek(c)


