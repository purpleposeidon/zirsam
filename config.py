# -*- coding: utf-8 -*-



class CharSet:
  def __init__(self, *args):
    self.a, self.e, self.i, self.o, self.u, \
    self.A, self.E, self.I, self.O, self.U, \
    self.con, self.y, self.h, self.comma, self.period, self.whitespace, self.eof = args
    
    self.low_vowel = self.a+self.e+self.i+self.o+self.u
    self.accent_vowel = self.A+self.E+self.I+self.O+self.U
    self.low_vowel = self.a+self.e+self.i+self.o+self.u
_whitespace = ' \t\n\r'
_low_vowel = 'aeiou'

#NOTE: Sane people don't use macrons
_A = "AáÁàÀ" #āĀ
_E = "EéÉèÈ" #ēĒ
_I = "IíÍìÌ" #īĪ
_O = "OóÓòÒ" #ōŌ
_U = "UúÚùÙ" #ūŪ
_accent_vowel = _A+_E+_I+_O+_U
_con = 'bcdfgjklmnprstvxz'
_y = 'yY'
_h = "'h\"H"
_comma = ','
_period = "."
_eof = ['', '\0', '\x0c', '\x06'] #Empty string, null character, ^L, ^F
strict_chars = CharSet('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U', _con, 'y', "'", ',', '.', _whitespace, '')
liberal_chars = CharSet('a', 'e', 'i', 'o', 'u', _A, _E, _I, _O, _U, _con+_con.upper(), 'yY', "'\"hH", ',', '.', _whitespace+'\\/', _eof)


###############_ipacon = "b  ʃʂ d fɸ g ʒʐ k lɭ mɱ nɳɲŋ p rɾɹʀ s t vβ x z".split(' ')

###############ipa_chars = CharSet("aɑ", "eɛ", "i", "oɔ", "u", '', '', '', '', '', _ipacon, 'ə', 'hθ', ',', 'ʔ', _whitespace, _eof)
###############_cyrcon = "б  ш  д ф  г ж  к л  м  н    п р    с т в  х з".split(' ')

###############cyrllic_chars = CharSet('а', 'е', 'и', 'о', 'у')

"""
IPA:
         b  ʃʂ d fɸ g ʒʐ k lɭ mɱ nɳɲŋ p rɾɹʀ s t vβ x z aɑ eɛ i oɔ u ə hθ ʔ ,
Latin:
         b  c  d f  g j  k l  m  n    p r    s t v  x z a  e  i o  u y '  . ,
cyrillic:
         б  ш  д ф  г ж  к л  м  н    п р    с т в  х з а  е  и о  у ъ '  . ,

How It (will) Work<s>:
  A character has been requested. The caller will be returned a list of Characters.
    while 1:
      Read 1 character. Check it out in the encoding table.
        Is one of those accent characters?
          Set acccent mode
        else:
          break
    Look up the character in the encoding table.
    For each character we find:
      Check if the character modifies the accent state, like above.
      Otherwise, create the Character object, add it to the list
      Handle the accent state
    Return the list of characters.
XXX - Sort out this MESS
"""

class GlyphTable(dict):
  latin_lower = "b c d f g h j k l m n p r s t v x z a e i o u y ' . ,".split(' ')
  latin_upper = 'B C D F G H J K L M N P R S T V X Z A E I O U Y " . ,'.split(' ')
  def __init__(self, name, foreign_lower, foreign_upper, accentmark=None, unaccentmark=None, accenton=None, accentoff=None, extra={}):
    """
    name is the name of the alphabet
    foreign_lower is a string of lower case characters, seperated by spaces. They do not imply accent. If multiple foreign letters map to a single latin letter, do not seperate them with a space
    foreign_upper is in a similiar format, except that these letters imply accent. You may specify None, but you'll want to define some kind of accent marking.
    accentmark is a string of characters that mean, "The next character is accented"
    unaccentmark is similiar
    accenton is a string of characters that mean, "Everything following is accented"
    accentoff is a string of characters that mean, "Everything following is unaccented"
    accenton/accentoff characters are not matched. For example, if you have "<^" as accenton and ">v" as accentoff, "<ava" will be translated to "Aa"
    extra is a dictionary in form {latin_character:list_of_foreign_characters}. For example, you could map chinese numeral characters to equivalent latin ones. (The latin_character key doesn't have to be a single character)
    """
    dict.__init__(self)
    self.name = name
    
    self.accentmark = accentmark #This means the next character is accented
    self.unaccentmark = unaccentmark
    self.accenton = accenton #This means everything following is accented
    self.accentoff = accentoff #This means everything following is not accented
    
    if type(foreign_lower) == str:
      foreign_lower = foreign_lower.split()
    if type(foreign_upper) == str:
      foreign_upper = foreign_upper.split()
    
    
    for latin, foreign in zip(GlyphTable.latin_lower, foreign_lower):
      for c in foreign:
        self[c] = latin
    if foreign_upper:
      for latin, foreign in zip(GlyphTable.latin_upper, foreign_upper):
        for c in foreign:
          self[c] = latin
    
    for latin in extra:
      for foreign in extra[latin]:
        self[foreign] = latin


latin_alphabet = GlyphTable("latin", GlyphTable.latin_lower, GlyphTable.latin_upper)
leet_alphabet = GlyphTable("leet", GlyphTable.latin_lower, GlyphTable.latin_upper, extra={'1':'pa', '2':'re', '3':'ci', '4':'vo', '5':'mu', '6':'xa', '7':'ze', '8':'bi', '9':'so', '0':'no'})
cryllic_alphabet = GlyphTable("cryllic", "б ш д ф г ж к л м н  п р  с т в х з а е и о у ъ ' . ,".split(),  'Б Ш Д Ф Г Ж К Л М Н  П Р  С Т В Х З А Е И О У Ъ " . ,'.split())
ipa_alphabet = GlyphTable("ipa", "b ʃʂ d fɸ g ʒʐ k lɭ mɱ nɳɲŋ p rɾɹʀ s t vβ x z aɑ eɛ i oɔ u ə hθ ʔ ,".split(), None, accentmark='^')



def format_arg(w):
  return '--'+w.strip().replace(' ', '-')


class Configuration:
  __help = {'help':"Shows the help", 'strict':"Count warnings as errors", 'ascii only':"Permit only capitals to be used in accents", 'quiet':"*Don't print warnings", 'debug':"Parse noisily", 'print tokens':"prints out a token when it is made", 'token error':"Raise an error on the first token", 'no dotside':"Don't require a pause following cmene-markers"}
  
  def __check_options(self, argv):
    argv = list(argv) #Use a copy
    def arg(what):
      #XXX A thought: Make this function do all the work with __setattr__ and such
      if what not in Configuration.__help:
        raise Exception("No help given for argument {0}".format(what))
      what = format_arg(what)
      while what in argv:
        argv.pop(argv.index(what))
        return True
      
    if arg('help'):
      print("Text to parse is read from standard input. Output is sent to stdout, errors are sent to stderr. Options marked with * may not be fully implemented")
      for cmd in Configuration.__help:
        print("{0}: {1}".format(format_arg(cmd), Configuration.__help[cmd]))
      raise SystemExit
    if arg('strict'):
      self.strict = True
      self.ascii_only = True
    if arg('ascii only'):
      self.ascii_only = True
    if arg("quiet"):
      self.quiet = True
    if arg("debug"):
      self.debug = True
      self.print_tokens = True
    if arg("print tokens"): #Print tokens as they are parsed
      self.print_tokens = True
    if arg("token error"): #Error on first token
      self.token_error = True
    if arg("no dotside"):
      self.dotside = False
    

    if argv:
      if self.debug:
        print("\n\nCurrent settings:")
        print(str(self))
      print("Could not handle these arguments:")
      for a in argv:
        print('\t', a)
      
      raise SystemExit
      
  def __str__(self):
    r = ''
    for i in dir(self):
      if i[0] != '_':
        r += "\t{0}: {1}\n".format(i, self.__getattribute__(i))
    return r
  
  def __init__(self, args):
    """
    Configuration options to permeate the entire parser
    """
    self.strict = False
    self.quiet = False
    self.print_tokens = False
    self.dotside = True
    self.ascii_only = False
    self.token_error = False
    self.debug = False
    
    self.__check_options(args)
    if self.ascii_only:
      self.charset = strict_chars
    else:
      self.charset = liberal_chars


