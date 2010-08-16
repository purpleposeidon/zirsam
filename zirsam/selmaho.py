# -*- coding: utf-8 -*-

"""
Cmavo data.
To determine the selma'o of a cmavo, look of that cmavo's value in the
SELMAHO dictionary that is defined by this module.
"""

SELMAHO = {}


class Selmaho:
    """Base class for selmaho objects."""
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
    """
    The selma'o for undefined cmavo.
    """
    def __repr__(self):
        return "CIZMAhO"
    def __init__(self):
        SELMAHO['CIZMAhO'] = self
        self.__name__ = 'CIZMAhO'
        self.forms = []

    def __contains__(self, token):
        return token not in SELMAHO


unknown = UnknownSelmaho()

#I count 122 selma'o
#Everything below is more data than code
#Generated using data from cmavo.txt - if you want to regen, take note:
#  spaces/periods in front of cmavo, some selmaho are really weird, like UIa,
#  or UI3. Also, there are combined forms like UI*, don't use those.
#
#NOTE: Have to make some modifications. FA must be in order:
#  ['fa, 'fe', 'fi', 'fo', 'fu'...

BE = Selmaho('BE', ['be'])
SEhU = Selmaho('SEhU', ["se'u"])
BO = Selmaho('BO', ['bo'])
BOI = Selmaho('BOI', ['boi'])
LIhU = Selmaho('LIhU', ["li'u"])
BY = Selmaho('BY', ['by', 'cy', 'dy', 'fy', "ga'e", "ge'o", 'gy', "je'o",
                    "jo'o", 'jy', 'ky', "lo'a", 'ly', 'my', "na'a", 'ny',
                    'py', "ru'o", 'ry', "se'e", 'sy', "to'a", 'ty', 'vy',
                    'xy', "y'y", 'zy'])
LUhU = Selmaho('LUhU', ["lu'u"])
DAhO = Selmaho('DAhO', ["da'o"])
NUhU = Selmaho('NUhU', ["nu'u"])
GIhA = Selmaho('GIhA', ["gi'a", "gi'e", "gi'i", "gi'o", "gi'u"])
NUhI = Selmaho('NUhI', ["nu'i"])
VIhA = Selmaho('VIhA', ["vi'a", "vi'e", "vi'i", "vi'u"])
BAhE = Selmaho('BAhE', ["ba'e", "za'e"])
JOI = Selmaho('JOI', ['ce', "ce'o", "fa'u", "jo'e", "jo'u", 'joi', "ju'e",
                      "ku'a", "pi'u"])
NUhA = Selmaho('NUhA', ["nu'a"])
VEI = Selmaho('VEI', ['vei'])
ZEhA = Selmaho('ZEhA', ["ze'a", "ze'e", "ze'i", "ze'u"])
MOhI = Selmaho('MOhI', ["mo'i"])
NAI = Selmaho('NAI', ['nai'])
ZAhO = Selmaho('ZAhO', ["ba'o", "ca'o", "co'a", "co'i", "co'u", "de'a",
                        "di'a", "mo'u", "pu'o", "za'o"])
GA = Selmaho('GA', ['ga', 'ge', "ge'i", 'go', 'gu'])
JAI = Selmaho('JAI', ['jai'])
TAhE = Selmaho('TAhE', ["di'i", "na'o", "ru'i", "ta'e"])
GI = Selmaho('GI', ['gi'])
VAU = Selmaho('VAU', ['vau'])
KE = Selmaho('KE', ['ke'])
BU = Selmaho('BU', ['bu'])
BEhO = Selmaho('BEhO', ["be'o"])
MAI = Selmaho('MAI', ['mai', "mo'o"])
LAU = Selmaho('LAU', ["ce'a", 'lau', 'tau', 'zai'])
LOhU = Selmaho('LOhU', ["lo'u"])
BEI = Selmaho('BEI', ['bei'])
VUhO = Selmaho('VUhO', ["vu'o"])
KEhE = Selmaho('KEhE', ["ke'e"])
VUhU = Selmaho('VUhU', ["cu'a", "de'o", "fa'i", "fe'a", "fe'i", "fu'u",
                        "ge'a", "gei", "ju'u", "ne'o", "pa'i", "pi'a",
                        "ri'o", "sa'i", "sa'o", "si'i", "su'i", "te'a",
                        "va'a", "vu'u"])
ROI = Selmaho('ROI', ["re'u", 'roi'])
PU = Selmaho('PU', ['ba', 'ca', 'pu'])
CEI = Selmaho('CEI', ['cei'])
JA = Selmaho('JA', ['ja', 'je', "je'i", 'jo', 'ju'])
PA = Selmaho('PA', ['bi', "ce'i", 'ci', "ci'i", "da'a", 'dau', "du'e", 'fei',
                    "fi'u", 'gai', 'jau', "ji'i", "ka'o", "ki'o", "ma'u",
                    "me'i", "mo'a", 'mu', "ni'u", 'no', "no'o", 'pa',
                    'pai', 'pi', "pi'e", "ra'e", 'rau', 're', 'rei',
                    'ro', 'so', "so'a", "so'e", "so'i", "so'o", "so'u",
                    "su'e", "su'o", "te'o", "tu'o", 'vai', 'vo', 'xa',
                    'xo', "za'u", 'ze'])
FAhA = Selmaho('FAhA', ["be'a", "bu'u", "ca'u", "du'a", "fa'a", "ga'u",
                        "ne'a", "ne'i", "ne'u", "ni'a", "pa'o", "re'o",
                        "ri'u", "ru'u", "te'e", "ti'a", "to'o", "vu'a",
                        "ze'o", "zo'a", "zo'i", "zu'a"])
FAhO = Selmaho('FAhO', ["fa'o"])
ZO = Selmaho('ZO', ['zo'])
ZI = Selmaho('ZI', ['za', 'zi', 'zu'])
ZOI = Selmaho('ZOI', ["la'o", 'zoi'])
LAhE = Selmaho('LAhE', ["la'e", "lu'a", "lu'e", "lu'i", "lu'o", "tu'a",
                        "vu'i"])
KUhO = Selmaho('KUhO', ["ku'o"])
KUhE = Selmaho('KUhE', ["ku'e"])
ME = Selmaho('ME', ['me'])
CEhE = Selmaho('CEhE', ["ce'e"])
TUhU = Selmaho('TUhU', ["tu'u"])
NAhU = Selmaho('NAhU', ["na'u"])
LEhU = Selmaho('LEhU', ["le'u"])
MOI = Selmaho('MOI', ["cu'o", 'mei', 'moi', "si'e", "va'e"])
UI = Selmaho('UI', ["a'a", "a'e", "a'i", "a'o", "a'u", 'ai', 'au', "ba'a",
                    "ba'u", "be'u", "bu'o", "ca'e", "da'i", 'dai', "do'a",
                    "e'a", "e'e", "e'i", "e'o", "e'u", 'ei', "fu'i", "ga'i",
                    "ge'e", "i'a", "i'e", "i'i", "i'o", "i'u", 'ia', 'ie',
                    'ii', 'io', 'iu', "ja'o", "je'u", "ju'a", "ju'o", "ka'u",
                    "ke'u", "ki'a", "la'a", "le'o", "li'a", "mu'a", "o'a",
                    "o'e", "o'i", "o'o", "o'u", 'oi', "pa'e", "pe'i", "ra'u",
                    "re'e", "ri'e", "ro'a", "ro'e", "ro'i", "ro'o", "ro'u",
                    "ru'a", "sa'e", "sa'u", "se'a", "se'i", "se'o", "su'a",
                    "ta'o", "ti'e", "to'u", "u'a", "u'e", "u'i", "u'o",
                    "u'u", 'ua', 'ue', 'ui', 'uo', 'uu', "va'i", "vu'e",
                    'xu', "za'a", "zo'o", "zu'u", "bi'u", "jo'a", 'kau',
                    "li'o", "na'i", 'pau', "sa'a", "ta'u", "pe'a", "ji'a",
                    "ku'i", "mi'u", "po'o", "si'a"])
ZIhE = Selmaho('ZIhE', ["zi'e"])
TUhE = Selmaho('TUhE', ["tu'e"])
NAhE = Selmaho('NAhE', ["je'a", "na'e", "no'e", "to'e"])
DOI = Selmaho('DOI', ['doi'])
FA = Selmaho('FA', ['fa', 'fe', 'fi', 'fo', 'fu', 'fai', "fi'a"])
COI = Selmaho('COI', ["be'e", "co'o", 'coi', "fe'o", "fi'i", "je'e", "ju'i",
                      "ke'o", "ki'e", "mi'e", "mu'o", "nu'e", "pe'u", "re'i",
                      "ta'a", "vi'o"])
TEI = Selmaho('TEI', ['tei'])
KOhA = Selmaho('KOhA', ["ce'u", 'da', "da'e", "da'u", 'de', "de'e", "de'u",
                        'dei', 'di', "di'e", "di'u", 'do', "do'i", "do'o",
                        "fo'a", "fo'e", "fo'i", "fo'o", "fo'u", "ke'a", 'ko',
                        "ko'a", "ko'e", "ko'i", "ko'o", "ko'u", 'ma', "ma'a",
                        'mi', "mi'a", "mi'o", 'ra', 'ri', 'ru', 'ta', 'ti',
                        'tu', "vo'a", "vo'e", "vo'i", "vo'o", "vo'u", "zi'o",
                        "zo'e", "zu'i"])
PEhE = Selmaho('PEhE', ["pe'e"])
MOhE = Selmaho('MOhE', ["mo'e"])
NA = Selmaho('NA', ["ja'a", 'na'])
RAhO = Selmaho('RAhO', ["ra'o"])
PEhO = Selmaho('PEhO', ["pe'o"])
FOI = Selmaho('FOI', ['foi'])
FUhA = Selmaho('FUhA', ["fu'a"])
CUhE = Selmaho('CUhE', ["cu'e", 'nau'])
FUhE = Selmaho('FUhE', ["fu'e"])
MEhU = Selmaho('MEhU', ["me'u"])
FUhO = Selmaho('FUhO', ["fu'o"])
NU = Selmaho('NU', ["du'u", 'jei', 'ka', "li'i", "mu'e", 'ni', 'nu', "pu'u",
                    "si'o", "su'u", "za'i", "zu'o"])
SEI = Selmaho('SEI', ['sei', "ti'o"])
NIhE = Selmaho('NIhE', ["ni'e"])
XI = Selmaho('XI', ['xi'])
CO = Selmaho('CO', ['co'])
NIhO = Selmaho('NIhO', ["ni'o", "no'i"])
CAhA = Selmaho('CAhA', ["ca'a", "ka'e", "nu'o", "pu'i"])
JOhI = Selmaho('JOhI', ["jo'i"])
CU = Selmaho('CU', ['cu'])
NOI = Selmaho('NOI', ['noi', 'poi', 'voi'])
KEI = Selmaho('KEI', ['kei'])
KI = Selmaho('KI', ['ki'])
ZEI = Selmaho('ZEI', ['zei'])
SU = Selmaho('SU', ['su'])
LOhO = Selmaho('LOhO', ["lo'o"])
SI = Selmaho('SI', ['si'])
KU = Selmaho('KU', ['ku'])
GOhA = Selmaho('GOhA', ["bu'a", "bu'e", "bu'i", "co'e", 'du', "go'a", "go'e",
               "go'i", "go'o", "go'u", 'mo', 'nei', "no'a"])
SA = Selmaho('SA', ['sa'])
SE = Selmaho('SE', ['se', 'te', 've', 'xe'])
BIhI = Selmaho('BIhI', ["bi'i", "bi'o", "mi'i"])
BIhE = Selmaho('BIhE', ["bi'e"])
CAI = Selmaho('CAI', ['cai', "cu'i", 'pei', "ru'e", 'sai'])
TOI = Selmaho('TOI', ['toi'])
TEhU = Selmaho('TEhU', ["te'u"])
GEhU = Selmaho('GEhU', ["ge'u"])
BAI = Selmaho('BAI', ["ba'i", 'bai', 'bau', "be'i", "ca'i", 'cau', "ci'e",
                      "ci'o", "ci'u", "cu'u", "de'i", "di'o", "do'e", "du'i",
                      "du'o", "fa'e", 'fau', "fi'e", "ga'a", 'gau', "ja'e",
                      "ja'i", "ji'e", "ji'o", "ji'u", "ka'a", "ka'i", 'kai',
                      "ki'i", "ki'u", 'koi', "ku'u", "la'u", "le'a", "li'e",
                      "ma'e", "ma'i", 'mau', "me'a", "me'e", "mu'i", "mu'u",
                      "ni'i", "pa'a", "pa'u", "pi'o", "po'i", "pu'a", "pu'e",
                      "ra'a", "ra'i", 'rai', "ri'a", "ri'i", 'sau', "si'u",
                      "ta'i", 'tai', "ti'i", "ti'u", "tu'i", "va'o", "va'u",
                      'zau', "zu'e"])
LE = Selmaho('LE', ['le', "le'e", "le'i", 'lei', 'lo', "lo'e", "lo'i", 'loi'])
LA = Selmaho('LA', ['la', "la'i", 'lai'])
SOI = Selmaho('SOI', ['soi'])
VEhA = Selmaho('VEhA', ["ve'a", "ve'e", "ve'i", "ve'u"])
LI = Selmaho('LI', ['li', "me'o"])
TO = Selmaho('TO', ['to', "to'i"])
LU = Selmaho('LU', ['lu'])
GUhA = Selmaho('GUhA', ["gu'a", "gu'e", "gu'i", "gu'o", "gu'u"])
A = Selmaho('A', ['a', 'e', 'ji', 'o', 'u'])
VA = Selmaho('VA', ['va', 'vi', 'vu'])
GOI = Selmaho('GOI', ['goi', 'ne', "no'u", 'pe', 'po', "po'e", "po'u"])
MAhO = Selmaho('MAhO', ["ma'o"])
FEhE = Selmaho('FEhE', ["fe'e"])
I = Selmaho('I', ['i'])
ZOhU = Selmaho('ZOhU', ["zo'u"])
FEhU = Selmaho('FEhU', ["fe'u"])
Y = Selmaho('Y', ['y'])
FIhO = Selmaho('FIhO', ["fi'o"])
DOhU = Selmaho('DOhU', ["do'u"])
GAhO = Selmaho('GAhO', ["ga'o", "ke'i"])
VEhO = Selmaho('VEhO', ["ve'o"])
