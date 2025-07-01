from ..alphabet import Alphabet
from ..dmath import is_prime

def modify_symbol_only(symbol: str, abc: Alphabet, action) -> str:
    if (abc.has(symbol)):
        return abc.symbols()[action(abc.index(symbol)) % abc.size()]
    return symbol

def caesar(text: str, abc: Alphabet, shift: int) -> str:
    return ''.join(
        modify_symbol_only(s, abc, lambda x: x + shift)
        for s in text
    )

def atbash(text: str, abc: Alphabet) -> str:
    return ''.join(
        modify_symbol_only(s, abc, lambda x: abc.size() - x - 1)
        for s in text
    )

def prime_series(text: str, abc: Alphabet, start_at: int = 2, subtract: bool = False) -> str:
    output = []
    p = start_at
    for ch in text:
        if not abc.has(ch):
            output.append(ch)
            continue

        si = (abc.index(ch) + (-p if subtract else p)) % abc.size()
        output.append(abc.symbols()[si])

        if p == 2:
            p += 1
            continue
        p += 2
        while not is_prime(p): p += 2
    return ''.join(output)

def vigenere(
        text: str,
        key: str | list[int],
        abc: Alphabet,
        subtract: bool = False,
        skip_indices: list[int] = []
) -> str:
    ikey: list[int] = [ abc.index(s) for s in key ] if type(key) is str else key # type: ignore
    output = []
    i, ti = 0, 0
    for ch in text:
        if not abc.has(ch):
            output.append(ch)
            continue
        elif ti in skip_indices:
            output.append(ch)
            ti += 1
            continue

        si = (abc.index(ch) + (-ikey[i] if subtract else ikey[i])) % abc.size()
        output.append(abc.symbols()[si])
        i, ti = (i + 1) % len(ikey), ti + 1

    return ''.join(output)

def multi_vigenere(text: str, keys: list[str | list[int]], abc: Alphabet, subtract: bool = False) -> str:
    ikeys: list[list[int]] = []
    for key in keys:
        ikeys.append([ abc.index(s) for s in key ] if type(key) is str else key) # type: ignore
    output = []
    ids = [0] * len(keys)
    ki = 0
    last_si = None
    for ch in text:
        if not abc.has(ch):
            output.append(ch)
            continue

        si = (abc.index(ch) + (-ikeys[ki][ids[ki]] if subtract else ikeys[ki][ids[ki]])) % abc.size()
        if si == last_si:
            ki = (ki+1) % len(ikeys)
            si = (abc.index(ch) + (-ikeys[ki][ids[ki]] if subtract else ikeys[ki][ids[ki]])) % abc.size()

        output.append(abc.symbols()[si])
        ids[ki] = (ids[ki] + 1) % len(ikeys[ki])

    return ''.join(output)

# affine, vigenere, polybius (encrypt/decrypt)

def autokey(text: str, primer: str | list[int], abc: Alphabet, subtract: bool = False) -> str:
    iprimer: list[int] = [ abc.index(s) for s in primer ] if type(primer) is str else primer # type: ignore
    output = []
    ti, pi = 0, 0
    while pi < len(primer):
        ch = text[ti]
        if not abc.has(ch):
            output.append(ch)
            ti += 1
            continue

        si = (abc.index(ch) + (-iprimer[pi] if subtract else iprimer[pi])) % abc.size()
        output.append(abc.symbols()[si])
        ti, pi = ti+1, pi+1


    return \
        ''.join(output) + \
        vigenere(text[ti:], abc.filter_symbols(text), abc, subtract)
