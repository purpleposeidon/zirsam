# -*- coding: utf-8 -*-

"""
Cmavo data.
To determine the selma'o of a cmavo, look of that cmavo's value in the SELMAHO dictionary
that is defined by this module.
"""

SELMAHO = {}


class selmaho:
  #Base class for selmaho objects
  def __repr__(self):
    return self.__name__
  def __init__(self, name, forms):
    """
    Define a new selma'o.
    "name" is the selma'o name (like KOhA)
    "forms" is a list of each member of the selma'o
    """
    for form in forms:
      SELMAHO[form] = self
    #SELMAHO_DICT[__name__] = forms
    self.__name__ = name
    self.forms = forms

  def __contains__(self, token):
    #Returns True if token is a member of the given selma'o
    #I might not use this?
    return token.value in self.forms
    #return any(token.value == _ for _ in self.forms)

class UnknownSelmaho:
  def __repr__(self):
    return "UNKNOWN"
  def __init__(self):
    SELMAHO['UNKNOWN'] = self
    self.__name__ = 'UNKNOWN'
    self.forms = []

  def __contains__(self, token):
    return token not in SELMAHO
"""
What is this?
      '''
      What I want.
      is_selmaho(token, SELMAhO)
      document_root(iter, config)
      '''
For the first item, I can use token.class. "document_root"? Uhm. Whatever, just delete this at some point
"""

unknown = UnknownSelmaho()

#I count 123 selma'o
#Everything below is more data than code
#Generated using data from cmavo.txt - if you want to regen, take note: spaces/periods in front of cmavo, some selmaho are really weird, like UIa, or UI3. Also, there are combined forms like UI*, don't use those.
BE = selmaho('BE', ['be'])
UIb = selmaho('UIb', ["ji'a", "ku'i", "mi'u", "po'o", "si'a"])
SEhU = selmaho('SEhU', ["se'u"])
BO = selmaho('BO', ['bo'])
BOI = selmaho('BOI', ['boi'])
LIhU = selmaho('LIhU', ["li'u"])
BY = selmaho('BY', ['by', 'cy', 'dy', 'fy', "ga'e", "ge'o", 'gy', "je'o", "jo'o", 'jy', 'ky', "lo'a", 'ly', 'my', "na'a", 'ny', 'py', "ru'o", 'ry', "se'e", 'sy', "to'a", 'ty', 'vy', 'xy', "y'y", 'zy'])
LUhU = selmaho('LUhU', ["lu'u"])
DAhO = selmaho('DAhO', ["da'o"])
NUhU = selmaho('NUhU', ["nu'u"])
GIhA = selmaho('GIhA', ["gi'a", "gi'e", "gi'i", "gi'o", "gi'u"])
NUhI = selmaho('NUhI', ["nu'i"])
VIhA = selmaho('VIhA', ["vi'a", "vi'e", "vi'i", "vi'u"])
BAhE = selmaho('BAhE', ["ba'e", "za'e"])
JOI = selmaho('JOI', ['ce', "ce'o", "fa'u", "jo'e", "jo'u", 'joi', "ju'e", "ku'a", "pi'u"])
NUhA = selmaho('NUhA', ["nu'a"])
VEI = selmaho('VEI', ['vei'])
ZEhA = selmaho('ZEhA', ["ze'a", "ze'e", "ze'i", "ze'u"])
MOhI = selmaho('MOhI', ["mo'i"])
NAI = selmaho('NAI', ['nai'])
ZAhO = selmaho('ZAhO', ["ba'o", "ca'o", "co'a", "co'i", "co'u", "de'a", "di'a", "mo'u", "pu'o", "za'o"])
GA = selmaho('GA', ['ga', 'ge', "ge'i", 'go', 'gu'])
JAI = selmaho('JAI', ['jai'])
TAhE = selmaho('TAhE', ["di'i", "na'o", "ru'i", "ta'e"])
GI = selmaho('GI', ['gi'])
VAU = selmaho('VAU', ['vau'])
KE = selmaho('KE', ['ke'])
BU = selmaho('BU', ['bu'])
BEhO = selmaho('BEhO', ["be'o"])
MAI = selmaho('MAI', ['mai', "mo'o"])
LAU = selmaho('LAU', ["ce'a", 'lau', 'tau', 'zai'])
LOhU = selmaho('LOhU', ["lo'u"])
BEI = selmaho('BEI', ['bei'])
VUhO = selmaho('VUhO', ["vu'o"])
KEhE = selmaho('KEhE', ["ke'e"])
VUhU = selmaho('VUhU', ["cu'a", "de'o", "fa'i", "fe'a", "fe'i", "fu'u", "ge'a", "ju'u", "ne'o", "pa'i", "pi'a", "ri'o", "sa'i", "sa'o", "si'i", "su'i", "te'a", "va'a", "vu'u"])
ROI = selmaho('ROI', ["re'u", 'roi'])
PU = selmaho('PU', ['ba', 'ca', 'pu'])
CEI = selmaho('CEI', ['cei'])
JA = selmaho('JA', ['ja', 'je', "je'i", 'jo', 'ju'])
PA = selmaho('PA', ['bi', "ce'i", 'ci', "ci'i", "da'a", 'dau', "du'e", 'fei', "fi'u", 'gai', 'jau', "ji'i", "ka'o", "ki'o", "ma'u", "me'i", "mo'a", 'mu', "ni'u", 'no', "no'o", 'pa', 'pai', 'pi', "pi'e", "ra'e", 'rau', 're', 'rei', 'ro', 'so', "so'a", "so'e", "so'i", "so'o", "so'u", "su'e", "su'o", "te'o", "tu'o", 'vai', 'vo', 'xa', 'xo', "za'u", 'ze'])
FAhA = selmaho('FAhA', ["be'a", "bu'u", "ca'u", "du'a", "fa'a", "ga'u", "ne'a", "ne'i", "ne'u", "ni'a", "pa'o", "re'o", "ri'u", "ru'u", "te'e", "ti'a", "to'o", "vu'a", "ze'o", "zo'a", "zo'i", "zu'a"])
FAhO = selmaho('FAhO', ["fa'o"])
ZO = selmaho('ZO', ['zo'])
ZI = selmaho('ZI', ['za', 'zi', 'zu'])
ZOI = selmaho('ZOI', ["la'o", 'zoi'])
LAhE = selmaho('LAhE', ["la'e", "lu'a", "lu'e", "lu'i", "lu'o", "tu'a", "vu'i"])
KUhO = selmaho('KUhO', ["ku'o"])
KUhE = selmaho('KUhE', ["ku'e"])
ME = selmaho('ME', ['me'])
CEhE = selmaho('CEhE', ["ce'e"])
TUhU = selmaho('TUhU', ["tu'u"])
NAhU = selmaho('NAhU', ["na'u"])
LEhU = selmaho('LEhU', ["le'u"])
MOI = selmaho('MOI', ["cu'o", 'mei', 'moi', "si'e", "va'e"])
UI = selmaho('UI', ["a'a", "a'e", "a'i", "a'o", "a'u", 'ai', 'au', "ba'a", "ba'u", "be'u", "bu'o", "ca'e", "da'i", 'dai', "do'a", "e'a", "e'e", "e'i", "e'o", "e'u", 'ei', "fu'i", "ga'i", "ge'e", "i'a", "i'e", "i'i", "i'o", "i'u", 'ia', 'ie', 'ii', 'io', 'iu', "ja'o", "je'u", "ju'a", "ju'o", "ka'u", "ke'u", "ki'a", "la'a", "le'o", "li'a", "mu'a", "o'a", "o'e", "o'i", "o'o", "o'u", 'oi', "pa'e", "pe'i", "ra'u", "re'e", "ri'e", "ro'a", "ro'e", "ro'i", "ro'o", "ro'u", "ru'a", "sa'e", "sa'u", "se'a", "se'i", "se'o", "su'a", "ta'o", "ti'e", "to'u", "u'a", "u'e", "u'i", "u'o", "u'u", 'ua', 'ue', 'ui', 'uo', 'uu', "va'i", "vu'e", 'xu', "za'a", "zo'o", "zu'u", "bi'u", "jo'a", 'kau', "li'o", "na'i", 'pau', "sa'a", "ta'u", "pe'a"])
ZIhE = selmaho('ZIhE', ["zi'e"])
TUhE = selmaho('TUhE', ["tu'e"])
NAhE = selmaho('NAhE', ["je'a", "na'e", "no'e", "to'e"])
DOI = selmaho('DOI', ['doi'])
FA = selmaho('FA', ['fa', 'fai', 'fe', 'fi', "fi'a", 'fo', 'fu'])
COI = selmaho('COI', ["be'e", "co'o", 'coi', "fe'o", "fi'i", "je'e", "ju'i", "ke'o", "ki'e", "mi'e", "mu'o", "nu'e", "pe'u", "re'i", "ta'a", "vi'o"])
TEI = selmaho('TEI', ['tei'])
KOhA = selmaho('KOhA', ["ce'u", 'da', "da'e", "da'u", 'de', "de'e", "de'u", 'dei', 'di', "di'e", "di'u", 'do', "do'i", "do'o", "fo'a", "fo'e", "fo'i", "fo'o", "fo'u", "ke'a", 'ko', "ko'a", "ko'e", "ko'i", "ko'o", "ko'u", 'ma', "ma'a", 'mi', "mi'a", "mi'o", 'ra', 'ri', 'ru', 'ta', 'ti', 'tu', "vo'a", "vo'e", "vo'i", "vo'o", "vo'u", "zi'o", "zo'e", "zu'i"])
PEhE = selmaho('PEhE', ["pe'e"])
MOhE = selmaho('MOhE', ["mo'e"])
NA = selmaho('NA', ["ja'a", 'na'])
RAhO = selmaho('RAhO', ["ra'o"])
PEhO = selmaho('PEhO', ["pe'o"])
FOI = selmaho('FOI', ['foi'])
FUhA = selmaho('FUhA', ["fu'a"])
CUhE = selmaho('CUhE', ["cu'e", 'nau'])
FUhE = selmaho('FUhE', ["fu'e"])
MEhU = selmaho('MEhU', ["me'u"])
FUhO = selmaho('FUhO', ["fu'o"])
NU = selmaho('NU', ["du'u", 'jei', 'ka', "li'i", "mu'e", 'ni', 'nu', "pu'u", "si'o", "su'u", "za'i", "zu'o"])
SEI = selmaho('SEI', ['sei', "ti'o"])
NIhE = selmaho('NIhE', ["ni'e"])
XI = selmaho('XI', ['xi'])
CO = selmaho('CO', ['co'])
NIhO = selmaho('NIhO', ["ni'o", "no'i"])
CAhA = selmaho('CAhA', ["ca'a", "ka'e", "nu'o", "pu'i"])
JOhI = selmaho('JOhI', ["jo'i"])
CU = selmaho('CU', ['cu'])
NOI = selmaho('NOI', ['noi', 'poi', 'voi'])
KEI = selmaho('KEI', ['kei'])
KI = selmaho('KI', ['ki'])
ZEI = selmaho('ZEI', ['zei'])
SU = selmaho('SU', ['su'])
LOhO = selmaho('LOhO', ["lo'o"])
SI = selmaho('SI', ['si'])
KU = selmaho('KU', ['ku'])
GOhA = selmaho('GOhA', ["bu'a", "bu'e", "bu'i", "co'e", 'du', "go'a", "go'e", "go'i", "go'o", "go'u", 'mo', 'nei', "no'a"])
SA = selmaho('SA', ['sa'])
SE = selmaho('SE', ['se', 'te', 've', 'xe'])
BIhI = selmaho('BIhI', ["bi'i", "bi'o", "mi'i"])
BIhE = selmaho('BIhE', ["bi'e"])
CAI = selmaho('CAI', ['cai', "cu'i", 'pei', "ru'e", 'sai'])
TOI = selmaho('TOI', ['toi'])
TEhU = selmaho('TEhU', ["te'u"])
GEhU = selmaho('GEhU', ["ge'u"])
BAI = selmaho('BAI', ["ba'i", 'bai', 'bau', "be'i", "ca'i", 'cau', "ci'e", "ci'o", "ci'u", "cu'u", "de'i", "di'o", "do'e", "du'i", "du'o", "fa'e", 'fau', "fi'e", "ga'a", 'gau', "ja'e", "ja'i", "ji'e", "ji'o", "ji'u", "ka'a", "ka'i", 'kai', "ki'i", "ki'u", 'koi', "ku'u", "la'u", "le'a", "li'e", "ma'e", "ma'i", 'mau', "me'a", "me'e", "mu'i", "mu'u", "ni'i", "pa'a", "pa'u", "pi'o", "po'i", "pu'a", "pu'e", "ra'a", "ra'i", 'rai', "ri'a", "ri'i", 'sau', "si'u", "ta'i", 'tai', "ti'i", "ti'u", "tu'i", "va'o", "va'u", 'zau', "zu'e"])
LE = selmaho('LE', ['le', "le'e", "le'i", 'lei', 'lo', "lo'e", "lo'i", 'loi'])
LA = selmaho('LA', ['la', "la'i", 'lai'])
SOI = selmaho('SOI', ['soi'])
VEhA = selmaho('VEhA', ["ve'a", "ve'e", "ve'i", "ve'u"])
LI = selmaho('LI', ['li', "me'o"])
TO = selmaho('TO', ['to', "to'i"])
LU = selmaho('LU', ['lu'])
GUhA = selmaho('GUhA', ["gu'a", "gu'e", "gu'i", "gu'o", "gu'u"])
A = selmaho('A', ['a', 'e', 'ji', 'o', 'u'])
VA = selmaho('VA', ['va', 'vi', 'vu'])
GOI = selmaho('GOI', ['goi', 'ne', "no'u", 'pe', 'po', "po'e", "po'u"])
MAhO = selmaho('MAhO', ["ma'o"])
FEhE = selmaho('FEhE', ["fe'e"])
I = selmaho('I', ['i'])
ZOhU = selmaho('ZOhU', ["zo'u"])
FEhU = selmaho('FEhU', ["fe'u"])
Y = selmaho('Y', ['y'])
FIhO = selmaho('FIhO', ["fi'o"])
DOhU = selmaho('DOhU', ["do'u"])
GAhO = selmaho('GAhO', ["ga'o", "ke'i"])
VEhO = selmaho('VEhO', ["ve'o"])
