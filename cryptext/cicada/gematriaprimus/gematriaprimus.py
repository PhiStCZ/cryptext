from ..abc_futhorc import futhorc
from ...alphabet import Alphabet, latin
from ...dmath import primes

DATA = (
    ('ᚠ', 'f'),
    ('ᚢ', 'v'),
    ('ᚢ', 'u'),
    ('ᚦ', 'th'),
    ('ᚩ', 'o'),
    ('ᚱ', 'r'),
    ('ᚳ', 'c'),
    ('ᚳ', 'k'),
    ('ᚷ', 'g'),
    ('ᚹ', 'w'),
    ('ᚻ', 'h'),
    ('ᚾ', 'n'),
    ('ᛁ', 'i'),
    ('ᛄ', 'j'),
    ('ᛇ', 'eo'),
    ('ᛈ', 'p'),
    ('ᛉ', 'x'),
    ('ᛋ', 's'),
    ('ᛋ', 'z'),
    ('ᛏ', 't'),
    ('ᛒ', 'b'),
    ('ᛖ', 'e'),
    ('ᛗ', 'm'),
    ('ᛚ', 'l'),
    ('ᛝ', 'ing'),
    ('ᛝ', 'ng'),
    ('ᛟ', 'oe'),
    ('ᛞ', 'd'),
    ('ᚪ', 'a'),
    ('ᚫ', 'ae'),
    ('ᚣ', 'y'),
    ('ᛡ', 'io'),
    ('ᛡ', 'ia'),
    ('ᛠ', 'ea'),
    ('ᚳ', 'q'),   # extra Q
    ('ᚳᚹ', 'qu'), # extra QU
)

def _translate_one_from_buffer(isrc: int, buffer: list[str]) -> tuple[int, str] | None:
        idst = 1 - isrc
        best_match = None

        for e in DATA:
            if best_match is not None and len(e[isrc]) <= len(best_match[isrc]):
                continue
            if len(buffer) < len(e[isrc]):
                continue
            if all(buffer[i] == e[isrc][i] for i in range(len(e[isrc]))):
                best_match = e

        if best_match is None: return None
        return (len(best_match[isrc]), best_match[idst])

def _gp_code(text: str, abcsrc: Alphabet, isrc: int):
        buffer: list[str] = []
        output: list[str] = []

        def consume_buffer():
            nonlocal buffer, output
            while len(buffer) != 0:
                translated = _translate_one_from_buffer(isrc, buffer)
                if translated is None:
                    raise Exception('Gematria Primus: Failed to translate text.')
                num_consumed, out_sym = translated
                buffer = buffer[num_consumed:]
                output.append(out_sym)

        for ch in text:
            if abcsrc.has(ch): buffer.append(ch)
            else:
                consume_buffer()
                output.append(ch)
        consume_buffer()
        return ''.join(output)

def encode(text: str) -> str:
    ''' Translates a text from latin characters to futhorc runes. '''
    return _gp_code(text, latin, 1)

def decode(text: str) -> str:
    ''' Translates a text from futhorc runes to latin characters. '''
    return _gp_code(text, futhorc, 0)

PRIMES = primes(110)

def sum_text(text: str) -> int:
    ''' Returns the gematria-primus-defined sum of a given text. '''
    if not any(futhorc.has(ch) for ch in text):
        text = encode(text)

    summands = [ futhorc.index(ch) for ch in text if futhorc.has(ch) ]
    return sum(PRIMES[i] for i in summands)
