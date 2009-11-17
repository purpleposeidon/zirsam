# -*- coding: utf-8 -*-

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

import time

def get_string(fd, allowed_time=.1):
  """Yank everything out of the buffer"""
  start = time.time()
  allowed_time = 0
  r = c = fd.read(1)
  while c:
    c = fd.read(1)
    r += c
  return r

def OLDget_string(fd, allowed_time=.1):
  """Take allowed_time seconds to read anything that is in the buffer"""
  dest = time.time()+allowed_time
  r = ''
  while dest-time.time() > 0 and select.select([fd], [], [], dest-time.time()):
    r += fd.read(1)
  return r

class terminal:
  def __del__(self):
    os.unlink(self.fifoname)
    if self.fd:
      os.close(self.fd)
  def write(self, *args):
    try:
      while args:
        a = args[0]
        os.write(self.fd, bytes(str(a), 'utf8'))
        args = args[1:]
    except OSError as err:
      if err.errno == 32 or err.strerror == "Broken pipe":
        self.create_terminal() #Try to re-make the terminal
        #Try to re-write everything... but don't try too hard
        for a in args:
          os.write(self.fd, bytes(str(a), 'utf8'))
      else:
        raise
    

  def flush(self):
    pass
    #os.fsync(self.fd)

  def create_terminal(self):
    """Runs the program to display our output"""
    DO_AND = True
    if "TERM" in os.environ:
      t = os.environ["TERM"]

      if t == 'screen':
        if not exists("screen"):
          raise SystemExit("TERM is screen, yet the program 'screen' could not be found")
        cmd = "screen -t {1} {0}"
        DO_AND = False
      elif "DISPLAY" in os.environ:
        cmd = "x-terminal-emulator -T {1} -e {0}"
        if "DESKTOP_SESSION" in os.environ:
          ds = os.environ["DESKTOP_SESSION"].lower()
          if 'kde' in ds:
            if exists("konsole"):
              cmd = "konsole --caption {1} --title {1} -e {0}"
          elif 'gnome' in ds:
            if exists("gnome-terminal"):
              cmd = "gnome-terminal -t {1} --execute {0}"
      else:
        if not exists("screen"):
          raise SystemExit("Can not continue. You will either need to run this program from a graphical environment, or install the program 'screen'.")
        else:
          raise SystemExit("Can not continue. You will either need to run this program from a graphical environment, or from 'screen'")
    else:
      raise SystemExit("This program requires the TERM environment variable to be defined.")
    #Another option would be try using "TERM" as the name of the shell to execute, but it would be unlikely to ever get there (And might be a little bit insecure)
    tail = "cat {0} > /dev/zero 2> /dev/zero".format(self.fifoname)
    if not exists("cat"):
      if exists("type"): #type is the windows equivalent...
        tail.replace("cat", "type", 1)
      else:
        raise SystemExit("What kind of a person doesn't have a cat? (Hint: command 'cat' not found)")
    if DO_AND:
      tail += " &"
    cmd = cmd.format(tail, repr(self.title))
    r = os.system(cmd)
    print("\r If this program hangs, press Ctrl-C", end='\r')
    #try:
    if 1:
      self.fd = os.open(self.fifoname, os.O_WRONLY)
    #except Exception as e:
      #raise SystemExit("Failed to execute {0}".format(cmd))

    self.write(ClearLine, '\r')
    self.write("\t{0}".format(self.title))
    print(ClearLine, end='\r')
    #print("\t{0}".format(self.title), file=o, end='')
    
  def __init__(self, title):
    """
    Creates another terminal that can be used. If the program is being called from within
    screen, it will use the command "screen" to create another screen in screen. Otherwise,
    it will try to guess the best graphical terminal to use. It returns a write-only file.

    It probably wouldn't be too difficult to be able to read input from the terminal too.
    TODO: Write cases for other graphical environments?
    TODO: Are there programs similiar to screen?
    TODO: Being able to read input would be nice
    """
    self.fifoname = tempfile.mktemp(prefix="amuse-")
    self.title = title
    self.fd = None
    os.mkfifo(self.fifoname)
    self.create_terminal()




in_screen = "TERM" in os.environ and os.environ["TERM"] == 'screen'
in_x = "DISPLAY" in os.environ and os.environ["DISPLAY"]
if not(in_screen or in_x):
  if exists("screen"):
    recommand = sys.argv[0]
    for c in sys.argv[1:]:
      recommand += ' ' + c
    os.system("screen python {0}".format(recommand))
  else:
    raise SystemExit("Can not continue. You must either run this program with $DISPLAY set, or you must have screen installed.")

class Character:
  #A thought: What about multi-cell items?
  def dup(self):
    """If you're going to be manipulating characters (or colors) on an individual basis, you'll need to duplicate them. Otherwise, all of them will change!"""
    return Character(self.symbol, self.ascii, self.color)
  def __init__(self, symbol, ascii=None, color=GRAY, name='(No name)', flavor='(No flavor)'):
    #XXX: What about animated stuff?
    self.symbol = symbol
    self.color = color
    self.name = name
    self.description = flavor
    if not ascii:
      if ord(symbol) < 255:
        self.ascii = symbol
      else:
        self.ascii = '?'
    else:
      self.ascii = ascii
  
  def __str__(self):
    return "%s%s" % (self.color, self.symbol)

empty_char = Character(' ', ascii=' ')

class ScreenBuffer:
  def __init__(self):
    self.buff = {}
  def __setitem__(self, add, val):
    self.buff[add] = val
  def __getitem__(self, pos):
    return self.buff.get(pos, empty_char)
  def diff_char(self, old, pos):
    c = self[pos]
    b = old[pos]
    return (c.symbol == b.symbol) and (c.color == b.color)
  def draw(self, fd, old, width, height, draw_count=0):
    #if draw_count: return
    fd.write(CursorHome)
    con = ''
    old_attr = None
    for y in range(0, width):
      l = ''
      for x in range(0, height):
        p = (x, y)
        c = self[p]
        if c.color == old_attr:
          l += c.symbol
        else:
          l += str(c)
          old_attr = c.color
        
      #fd.write(l+'\n\r')
      con += l + '\n\r'
    fd.write(con)

    return
    for y in range(0, width):
      #Build list of what needs to be redrawn
      needs_refresh = []
      for x in range(0, height):
        if self.diff_char(old, (x, y)):
          needs_refresh.append(( x, self[(x, y)] ))

      #Now, redraw.
      #Moving costs CSI+2 char, reprinting costs CSI+4 char if the attr has changed, only 1 char if the attr is the same as the one to the left.
      # TODO This could be made more efficient by checking if the distance to move is less than 3 and all of those symbols are the same
      oldattr = None
      while needs_refresh:
        x, c = needs_refresh.pop(0)
        if c.color == oldattr:
          fd.write(c.symbol)
        else:
          oldattr = c.color
          fd.write(str(oldattr)); fd.write(c.symbol)
        if len(needs_refresh) > 1:
          dx = (needs_refresh[1][0] - x) - 1
          if dx > 0:
            fd.write(CursorRight(dx))
      fd.write('\r\n')
    #import time
    #time.sleep(1)

#setup()

