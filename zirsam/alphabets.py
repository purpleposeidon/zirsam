# -*- coding: utf-8 -*-

"""
mapping information for converting non-standard orthographies into latin.
"""

import string
import zirsam.orthography


class GlyphTable(dict):
    """
    Provides an interface for converting characters.
    """
    tables = {} #Dictionary of the GlyphTable objects
    def __repr__(self):
        return "<GlyphTable {0}>".format(self.name)

    def get_char(self, config):
        """
        Return a list of retrieved characters. If at EOF, the list is empty.
        """
        while 1:
            char = config.stdin.read(1)
            config.old_chars += char
            
            val = self.get(char, char)
         
            if val == None:
                continue

            if val == '':
                return []

            ret = []
            for char in val:
                if char == '\n':
                    config.position.pushline()
                else:
                    config.position.pushcol()
                ret.append(zirsam.orthography.Character(char, config))
            return ret

    def __init__(self, name, mapping):
        """
        mapping is a dictionary with keys of single 'foreign' characters,
        and values of their latin equivalents.
        Some special cases:
            End Of File character: ''
            Ignored Character: None

        A single foreign character may map to multiple latin characters
        (such as '1' to 'pa'). More advanced implementations than this are
        free to map multiple foreign characters to any amount of latin ones
        (maybe 'lol' to "u'i").

        TODO: These implementations don't exist.

        If the mapping doesn't define how to handle some character, that
        character's actual value is returned.
        """
        dict.__init__(self, mapping)
        self.name = name
        GlyphTable.tables[self.name] = self



#Doesn't convert anything. Everything above orthography expects very strict
#lojban orthography, weird characters will be counted as garbage.
STRICT = GlyphTable("strict", {})



#Maps upper case letters to lower case letters
__latin__ = dict(zip(string.ascii_uppercase, string.ascii_lowercase))
for _ in "AEIOU": del __latin__[_]
LATIN = GlyphTable("latin", __latin__)



#From http://dag.github.com/cll/3/10/
#Someone who is good with IPA should test this
IPA = GlyphTable("ipa", {
    'ʔ': '.',
    'ɑ': 'a',
    'β': 'v',
    'ɛ': 'e',
    'ə': 'y',
    'ɸ': 'f',
    'ɪ': None,
    'ɨ': None,
    'j': 'i',
    'l̩': 'l',
    'm̩': 'm',
    'n̩': 'n',
    'ŋ': 'n',
    'ɔ': 'o',
    'ɹ': 'r',
    'ɾ': 'r',
    'ʀ': 'r',
    'r̩': 'r',
    'ɹ̩': 'r',
    'ɾ̩': 'r',
    'ʃ': 'c',
    'ʂ': 's',
    'θ': "'",
    'ʏ': None,
    'ʒ': 'j',
    'ʐ': 'z'
#XXX - needs accent
})

#From http://dag.github.com/cll/3/12/
#Also in want of testing
CYRILLIC = GlyphTable("cyrillic", {
    "а": 'a',
    "б": 'b',
    "в": 'c',
    "г": 'd',
    "д": 'e', "Д": 'E',
    "е": 'f',
    "ж": 'g',
    "з": 'i', 'З': 'I',
    "и": 'j',
    "к": 'k',
    "л": 'l',
    "м": 'm',
    "н": 'n',
    "о": 'o', 'О':'O',
    "п": 'p',
    "р": 'r',
    "с": 's',
    "т": 't',
    "у": 'u', 'У': 'U',
    "ф": 'v',
    "х": 'x',
    "ш": 'z',
    "ъ": 'y',
})

#From http://www.lojban.org/tiki/CLL,+aka+Reference+Grammar,+Errata
SAMPA = GlyphTable("sampa", {
    'h':"'",
    '-':',', #I'm not so sure about that
    '?':'.',
    'S':'c', 's`':'c',
    'E':'e',
    'f':'f',
    'p\\':'f',
    'Z':'j',
    'z`':'j',
    'l=': 'l',
    'm=':'m',
    'n=':'n',
    'N':'n',
    'N=':'n',
    'O':'o',
    'r\\':'r',
    '4':'r',
    'R\\':'r',
    'r=':'r',
    'r\\=':'r',
    '4=':'r',
    'R\\=':'r',
    'B':'v',
    '@':'y',
    #Probably could also use an accent?
})

TEST = GlyphTable("test", {
    'a':'a',
    'e':'a',
    'i':'a',
    'o':'a',
    'u':'a',
    'b':'c',
    'c':'c',
    'd':'c',
    'f':'c',
    'g':'c',
    'j':'c',
    'k':'c',
    'l':'c',
    'm':'c',
    'n':'c',
    'p':'c',
    'r':'c',
    's':'c',
    't':'c',
    'v':'c',
    'x':'c',
    'z':'c',
})




#And now for the more interesting alphabets...


__PA1_map__ = {'1':'pa', '2':'re', '3':'ci', '4':'vo', '5':'mu',
             '6':'xa', '7':'ze', '8':'bi', '9':'so', '0':'no'}


#P3rm1t teh 1337s
LEET = GlyphTable("leet", __PA1_map__)

#Not like there exists any functions in, say, unicodedata to do this better.
__accent_map__ = {
    'á':'A',
    'Á':'A',
    'à':'A', #These are graves, actually, and should probably not be included
    'À':'A',
    
    'é':'E',
    'É':'E',
    'è':'E',
    'È':'E',
    
    'í':'I',
    'Í':'I',
    'ì':'I',
    'Ì':'I',
    
    'ó':'O',
    'Ó':'O',
    'ò':'O',
    'Ò':'O',
    
    'ú':'U',
    'Ú':'U',
    'ù':'U',
    'Ù':'U',
}

#Permíts all mannèr of áccents
ACCENT = GlyphTable("latin+accent", __accent_map__)

#And now combine both of them into something far too terrible to imagine
__leet_accent__ = dict(__PA1_map__, **__accent_map__)
LEET_ACCENT = GlyphTable("leet+accent", __leet_accent__)

#Allow additional horrors and terrors
LIBERAL = GlyphTable("liberal",
    dict(
        dict(__latin__, **__leet_accent__),
        **{
            'Y':'y',
            'h':"'",
            'H':"'",
            '`':"'",
            '!':'sai',
        }
    )
)

#Ignore a few symbols
MICROBLOG = GlyphTable("microblog", {
    '@':None,
    '!':None,
    '#':None,
})

