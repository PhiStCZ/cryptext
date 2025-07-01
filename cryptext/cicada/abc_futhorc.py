from ..alphabet import Alphabet
# from .liberprimus import section_the_loss_of_divinity

import random

class Futhorc(Alphabet):
    def __init__(self) -> None:
        super().__init__('futhorc', (
        'ᚠ', 'ᚢ', 'ᚦ', 'ᚩ', 'ᚱ', 'ᚳ', 'ᚷ', 'ᚹ', 'ᚻ', 'ᚾ', 'ᛁ', 'ᛄ', 'ᛇ',
        'ᛈ', 'ᛉ', 'ᛋ', 'ᛏ', 'ᛒ', 'ᛖ', 'ᛗ', 'ᛚ', 'ᛝ', 'ᛟ', 'ᛞ', 'ᚪ', 'ᚫ',
        'ᚣ', 'ᛡ', 'ᛠ' # ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ
    ))

    ''' Generate text with a given probability of same-rune doublets (may be 0). '''
    def random_symbols_doublet_p(self, length: int, probability) -> str:
        if length == 0: return ''

        ids = [ random.randint(0, self.size() - 1) ] + \
            [
                (
                    -1 if random.random() <= probability
                    else random.randint(0, self.size() - 2)
                ) for _ in range(length - 1)
            ]

        for i in range(len(ids) - 1):
            if ids[i + 1] == -1:
                ids[i + 1] = ids[i]
            elif ids[i + 1] >= ids[i]:
                ids[i + 1] += 1

        return ''.join(
            self.symbols()[id] for id in ids
        )

    ''' Generate RLD (random low-doublets) text as in the Liber Primus. '''
    def random_ld(self, length: int):
        return self.random_symbols_doublet_p(length, 0.00663836356619066)


futhorc = Futhorc()
''' A variant of the old anglo-saxon runic alphabet, as used in Liber Primus. '''