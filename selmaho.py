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
    return self._class
  def __init__(self, _class, forms):
    """
    Define a new selma'o.
    "_class" is the selma'o name (like KOhA)
    "forms" is a string listing each member of the selma'o, seperated by a space.
    """
    forms = forms.split(' ')
    for form in forms:
      SELMAHO[form] = self
    #SELMAHO_DICT[_class] = forms
    self._class = _class
    self.forms = forms

  def __contains__(self, token):
    #Returns True if token is a member of the given selma'o
    #I might not use this?
    return token.value in self.forms
    #return any(token.value == _ for _ in self.forms)

"""
What is this?
      '''
      What I want.
      is_selmaho(token, SELMAhO)
      document_root(iter, config)
      '''
For the first item, I can use token.class. "document_root"? Uhm. Whatever, just delete this at some point
"""


#I count 122 selma'o
#Everything below is more data than code
A = selmaho('A', 'a e ji o u')
BAhE = selmaho('BAhE', "ba'e za'e")
BAI = selmaho('BAI', "ba'i bai bau be'i ca'i cau ci'e ci'o ci'u cu'u de'i di'o do'e du'i du'o fa'e fau fi'e ga'a gau ja'e ja'i ji'e ji'o ji'u ka'a ka'i kai ki'i ki'u koi ku'u la'u le'a li'e ma'e ma'i mau me'a me'e mu'i mu'u ni'i pa'a pa'u pi'o po'i pu'a pu'e ra'a ra'i rai ri'a ri'i sau si'u ta'i tai ti'i ti'u tu'i va'o va'u zau zu'e")
BEhO = selmaho('BEhO', "be'o")
BEI = selmaho('BEI', 'bei')
BE = selmaho('BE', 'be')
BIhE = selmaho('BIhE', "bi'e")
BIhI = selmaho('BIhI', "bi'i bi'o mi'i")
BOI = selmaho('BOI', 'boi')
BO = selmaho('BO', 'bo')
BU = selmaho('BU', 'bu')
BY = selmaho('BY', "by cy dy fy ga'e ge'o gy je'o jo'o jy ky lo'a ly my na'a ny py ru'o ry se'e sy to'a ty vy xy y'y zy")
CAhA = selmaho('CAhA', "ca'a ka'e nu'o pu'i")
CAI = selmaho('CAI', "cai cu'i pei ru'e sai")
CEhE = selmaho('CEhE', "ce'e")
CEI = selmaho('CEI', 'cei')
COI = selmaho('COI', "be'e co'o coi fe'o fi'i je'e ju'i ke'o ki'e mi'e mu'o nu'e pe'u re'i ta'a vi'o")
CO = selmaho('CO', 'co')
CUhE = selmaho('CUhE', "cu'e nau")
CU = selmaho('CU', 'cu')
DAhO = selmaho('DAhO', "da'o")
DOhU = selmaho('DOhU', "do'u")
DOI = selmaho('DOI', 'doi')
FAhA = selmaho('FAhA', "be'a bu'u ca'u du'a fa'a ga'u ne'a ne'i ne'u ni'a pa'o re'o ri'u ru'u te'e ti'a to'o vu'a ze'o zo'a zo'i zu'a")
FAhO = selmaho('FAhO', "fa'o")
FA = selmaho('FA', "fa fai fe fi fi'a fo fu")
FEhE = selmaho('FEhE', "fe'e")
FEhU = selmaho('FEhU', "fe'u")
FIhO = selmaho('FIhO', "fi'o")
FOI = selmaho('FOI', 'foi')
FUhA = selmaho('FUhA', "fu'a")
FUhE = selmaho('FUhE', "fu'e")
FUhO = selmaho('FUhO', "fu'o")
GAhO = selmaho('GAhO', "ga'o ke'i")
GA = selmaho('GA', "ga ge ge'i go gu")
GEhU = selmaho('GEhU', "ge'u")
GIhA = selmaho('GIhA', "gi'a gi'e gi'i gi'o gi'u")
GI = selmaho('GI', 'gi')
GOhA = selmaho('GOhA', "bu'a bu'e bu'i co'e du go'a go'e go'i go'o go'u mo nei no'a")
GOI = selmaho('GOI', "goi ne no'u pe po po'e po'u")
GUhA = selmaho('GUhA', "gu'a gu'e gu'i gu'o gu'u")
I = selmaho('I', 'i')
JAI = selmaho('JAI', 'jai')
JA = selmaho('JA', "ja je je'i jo ju")
JOhI = selmaho('JOhI', "jo'i")
JOI = selmaho('JOI', "ce ce'o fa'u jo'e jo'u joi ju'e ku'a pi'u")
KEhE = selmaho('KEhE', "ke'e")
KEI = selmaho('KEI', 'kei')
KE = selmaho('KE', 'ke')
KI = selmaho('KI', 'ki')
KOhA = selmaho('KOhA', "ce'u da da'e da'u de de'e de'u dei di di'e di'u do do'i do'o fo'a fo'e fo'i fo'o fo'u ke'a ko ko'a ko'e ko'i ko'o ko'u ma ma'a mi mi'a mi'o ra ri ru ta ti tu vo'a vo'e vo'i vo'o vo'u zi'o zo'e zu'i")
KUhE = selmaho('KUhE', "ku'e")
KUhO = selmaho('KUhO', "ku'o")
KU = selmaho('KU', 'ku')
LAhE = selmaho('LAhE', "la'e lu'a lu'e lu'i lu'o tu'a vu'i")
LA = selmaho('LA', "la la'i lai")
LAU = selmaho('LAU', "ce'a lau tau zai")
LEhU = selmaho('LEhU', "le'u")
LE = selmaho('LE', "le le'e le'i lei lo lo'e lo'i loi")
LIhU = selmaho('LIhU', "li'u")
LI = selmaho('LI', "li me'o")
LOhO = selmaho('LOhO', "lo'o")
LOhU = selmaho('LOhU', "lo'u")
LUhU = selmaho('LUhU', "lu'u")
LU = selmaho('LU', 'lu')
MAhO = selmaho('MAhO', "ma'o")
MAI = selmaho('MAI', "mai mo'o")
MEhU = selmaho('MEhU', "me'u")
ME = selmaho('ME', 'me')
MOhE = selmaho('MOhE', "mo'e")
MOhI = selmaho('MOhI', "mo'i")
MOI = selmaho('MOI', "cu'o mei moi si'e va'e")
NAhE = selmaho('NAhE', "je'a na'e no'e to'e")
NAhU = selmaho('NAhU', "na'u")
NAI = selmaho('NAI', 'nai')
NA = selmaho('NA', "ja'a na")
NIhE = selmaho('NIhE', "ni'e")
NIhO = selmaho('NIhO', "ni'o no'i")
NOI = selmaho('NOI', 'noi poi voi')
NUhA = selmaho('NUhA', "nu'a")
NUhI = selmaho('NUhI', "nu'i")
NUhU = selmaho('NUhU', "nu'u")
NU = selmaho('NU', "du'u jei ka li'i mu'e ni nu pu'u si'o su'u za'i zu'o")
PA = selmaho('PA', "bi ce'i ci ci'i da'a dau du'e fei fi'u gai jau ji'i ka'o ki'o ma'u me'i mo'a mu ni'u no no'o pa pai pi pi'e ra'e rau re rei ro so so'a so'e so'i so'o so'u su'e su'o te'o tu'o vai vo xa xo za'u ze")
PEhE = selmaho('PEhE', "pe'e")
PEhO = selmaho('PEhO', "pe'o")
PU = selmaho('PU', 'ba ca pu')
RAhO = selmaho('RAhO', "ra'o")
ROI = selmaho('ROI', "re'u roi")
SA = selmaho('SA', 'sa')
SEhU = selmaho('SEhU', "se'u")
SEI = selmaho('SEI', "sei ti'o")
SE = selmaho('SE', 'se te ve xe')
SI = selmaho('SI', 'si')
SOI = selmaho('SOI', 'soi')
SU = selmaho('SU', 'su')
TAhE = selmaho('TAhE', "di'i na'o ru'i ta'e")
TEhU = selmaho('TEhU', "te'u")
TEI = selmaho('TEI', 'tei')
TOI = selmaho('TOI', 'toi')
TO = selmaho('TO', "to to'i")
TUhE = selmaho('TUhE', "tu'e")
TUhU = selmaho('TUhU', "tu'u")
UI = selmaho('UI', "a'a a'e a'i a'o a'u ai au ba'a ba'u be'u bu'o ca'e da'i dai do'a e'a e'e e'i e'o e'u ei fu'i ga'i ge'e i'a i'e i'i i'o i'u ia ie ii io iu ja'o je'u ju'a ju'o ka'u ke'u ki'a la'a le'o li'a mu'a o'a o'e o'i o'o o'u oi pa'e pe'i ra'u re'e ri'e ro'a ro'e ro'i ro'o ro'u ru'a sa'e sa'u se'a se'i se'o su'a ta'o ti'e to'u u'a u'e u'i u'o u'u ua ue ui uo uu va'i vu'e xu za'a zo'o zu'u")
VA = selmaho('VA', 'va vi vu')
VAU = selmaho('VAU', 'vau')
VEhA = selmaho('VEhA', "ve'a ve'e ve'i ve'u")
VEhO = selmaho('VEhO', "ve'o")
VEI = selmaho('VEI', 'vei')
VIhA = selmaho('VIhA', "vi'a vi'e vi'i vi'u")
VUhO = selmaho('VUhO', "vu'o")
VUhU = selmaho('VUhU', "cu'a de'o fa'i fe'a fe'i gei ju'u ne'o pa'i pi'a pi'i re'a ri'o sa'i sa'o si'i su'i te'a va'a vu'u")
XI = selmaho('XI', 'xi')
Y = selmaho('Y', 'y')
ZAhO = selmaho('ZAhO', "ba'o ca'o co'a co'i co'u de'a di'a mo'u pu'o za'o")
ZEhA = selmaho('ZEhA', "ze'a ze'e ze'i ze'u")
ZEI = selmaho('ZEI', 'zei')
ZIhE = selmaho('ZIhE', "zi'e")
ZI = selmaho('ZI', 'za zi zu')
ZOhU = selmaho('ZOhU', "zo'u")
ZOI = selmaho('ZOI', "la'o zoi")
ZO = selmaho('ZO', 'zo')

