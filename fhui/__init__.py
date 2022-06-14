from typing import List, Dict, Optional

class DisplayCharSet:
    CharSet = {}
    
    @classmethod
    def decode(cls, codes : List[int], replacement_str : str = "_") -> str:
        retval = ""
        for i in codes:
            retval += cls.CharSet.get(i, replacement_str)

        return retval

    @classmethod
    def encode(cls, string: str, replacement_code : int = 0x5f) -> List[Optional[int]]:
        retval = list()
        for char in string:
            this_code = replacement_code
            for (key, value) in cls.CharSet.items():
                if value == char:
                    this_code = key
                    break
            retval.append(this_code)

        return retval

class SmallDisplayCharSet(DisplayCharSet):
    CharSet = {
        0x00 : "ì",
        0x01 : "↑",
        0x02 : "→",
        0x03 : "↓",
        0x04 : "←",
        0x05 : "¿",
        0x06 : "à",
        0x07 : "Ø",
        0x08 : "ø",
        0x09 : "ò",
        0x0a : "ù",
        0x0b : "Ň",
        0x0c : "Ç",
        0x0d : "ê",
        0x0e : "Ê",
        0x0f : "ê",
        0x10 : "è",
        0x11 : "Æ",
        0x12 : "æ",
        0x13 : "Å",
        0x14 : "å",
        0x15 : "Ä",
        0x16 : "ä",
        0x17 : "Ö",
        0x18 : "ö",
        0x19 : "Ü",
        0x1a : "ü",
        0x1b : "℃",
        0x1c : "℉",
        0x1d : "ß",
        0x1e : "£",
        0x1f : "¥",
        0x7e : "~",
        0x7f : "🮕",
            }
    
    for i in range(0x20,0x7e):
        CharSet[i] = chr(i)
    
    pass

class LargeDisplayCharSet(DisplayCharSet):
    CharSet = {
        0x19 : "♪",
        0x1a : "℃",
        0x1b : "℉",
        0x1c : "⏷",
        0x1d : "⏵",
        0x1e : "⏴",
        0x1f : "⏶",
        0x7e : "→",
        0x7f : "←",
            }

    for i in range(0x20,0x7e):
        CharSet[i] = chr(i)
    
    pass


