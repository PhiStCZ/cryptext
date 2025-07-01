import random

class Alphabet:
    '''
    Defines an ordered sequence of letters for texts and ciphers to work with.
    '''

    @staticmethod
    def _check_valid_name(name: str) -> bool:
        return len(name) > 0

    @staticmethod
    def _check_valid_symbols(symbols: tuple[str, ...]) -> bool:
        if len(symbols) == 0: return False
        for s in symbols:
            if len(s) == 0: return False
        for i in range(len(symbols)):
            for j in range(i + 1, len(symbols)):
                if symbols[i] == symbols[j]: return False
        return True

    def __init__(self, name: str, symbols: tuple[str, ...]) -> None:
        if (not Alphabet._check_valid_name(name) or
            not Alphabet._check_valid_symbols(symbols)):
            raise Exception('Badly formed alphabet')

        self._name, self._symbols = name, symbols
        self._max_sym_len = max(len(s) for s in symbols)

    def _sym_to_string(self, symidx) -> str:
        return self._symbols[symidx]

    def name(self) -> str:
        return self._name

    def size(self) -> int:
        return len(self._symbols)

    def symbols(self) -> tuple[str, ...]:
        return self._symbols

    def forbidden_non_symbols(self) -> tuple[str, ...]:
        return self._symbols

    def has(self, symbol: str) -> bool:
        return symbol in self._symbols

    def index(self, symbol: str) -> int:
        for i in range(len(self._symbols)):
            if self._symbols[i] == symbol: return i
        raise Exception("Could not find index of '{}'".format(symbol))


    def filter_symbols(self, text: str | list[str]) -> str:
        return ''.join(s for s in text if self.has(s))

    def extract_words(self, text: str) -> list[str]:
        '''
        Extracts continuous strings of the alphabet's symbols from a given text.

        Warning: does not count with apostrophes or any other non-alphabetical
        symbol.
        '''
        words = []

        istart = None
        for i in range(len(text)):
            if istart is None and self.has(text[i]):
                istart = i
            if istart is not None and not self.has(text[i]):
                words.append(text[istart:i])

        if istart is not None:
            words.append(text[istart:])
        return words

    def random_symbols(self, length: int) -> str:
        return ''.join(
            self.symbols()[random.randint(0, self.size() - 1)]
            for _ in range(length)
        )

latin = Alphabet('latin', (
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    ))
''' The standard latin alphabet of letters from a to z. '''

latin_punctuation = Alphabet('latin-punctuation', (
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        ' ', '.', '?'
    ))
''' An extension of the latin alphabet, additionally containing the space, comma, and period characters. '''

cyrilic = Alphabet('cyrilic', (
        'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л',
        'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш',
        'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я'
    ))
''' The cyrilic alphabet used in Russia and some other eastern-european countries. '''

ascii = Alphabet('ascii', tuple(
        chr(i) for i in range(128)
    ))
''' The alphabet of the basic 128 ascii character set. Note that some characters are not printable. '''

''' for now I am not supporting multi-symbol alphabets
binary = Alphabet('binary', tuple(
        ('0123456789abcdef'[i // 16] + '0123456789abcdef'[i % 16]) for i in range(256)
    ))
'''
