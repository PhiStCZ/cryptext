from ..alphabet import Alphabet
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes


def diff_text(symbols: str | list[str], alphabet: Alphabet) -> list[int]:
    symids: list[int] = []
    symids = [ alphabet.index(s) for s in symbols ]

    return [
        (symids[i+1] - symids[i]) % alphabet.size()
        for i in range(len(symids) - 1)
    ]


class NgramsByIndex:
    def __init__(self, text: str | list[str], alphabet: Alphabet, ngram_len: int = 1):
        self.alphabet = alphabet
        self.ngram_len = ngram_len

        self.occurences: dict[str | tuple[str], list[int]] = {}
        self.count = len(text) - ngram_len + 1

        text = alphabet.filter_symbols(text)

        for idx in range(self.count):
            s = text[idx:idx+ngram_len]
            if type(s) == list: s = tuple(s)
            if self.occurences.get(s) is None: self.occurences[s] = []
            self.occurences[s].append(idx)


def fingerprint(text: str | list[str], alphabet: Alphabet, ngram_len: int = 1) -> dict[str, float]:
    ngrams = NgramsByIndex(text, alphabet, ngram_len)
    return { str(k): (len(v) / ngrams.count) for k, v in ngrams.occurences.items() }


def find_repeated_ngrams(text: str | list[str], alphabet: Alphabet, ngram_len: int = 1):
    ngrams = NgramsByIndex(text, alphabet, ngram_len)
    return { k: v for k, v in ngrams.occurences.items() if len(v) > 1 }


def ioc(text: str | list[str], alphabet: Alphabet, ngram_len: int = 1) -> float:
    '''
    Let ABC be an alphabet with |ABC| letters. Index of coincidence, or IOC,
    is calculated as the probability that a randomly chosen two letters from
    a text are the same.
    The two letters are chosen distinctly (although they can be chosen
    independently, which achieves almost the same result).
    '''
    ngrams = NgramsByIndex(text, alphabet, ngram_len)
    return sum(len(v) * (len(v) - 1) for v in ngrams.occurences.values()) / (ngrams.count * (ngrams.count - 1))

def expected_ioc(alphabet: Alphabet | int, ngram_len: int = 1) -> float:
    # probability of each letter (ngram) (since its random theyre all the same)
    abc_size: int = alphabet.size() if isinstance(alphabet, Alphabet) else alphabet
    ngram_p = (1 / abc_size) ** ngram_len

    # if we pick 2 letters (ngrams), the first one can be any (prob. == 1),
    # the second one must be the same (prob. == ngram_p)
    return ngram_p

def crosstext_ioc(text1: str | list[str] | list[int], text2: str | list[str] | list[int], ngram_len: int = 1) -> float:
    count1, count2 = len(text1) - ngram_len + 1, len(text2) - ngram_len + 1
    counts = {}

    def count_ngrams(text, count, order):
        for i in range(count):
            s = tuple(text[j] for j in range(i, i + ngram_len))
            entry = counts.get(s)
            if entry is None:
                entry = [ 0, 0 ]
                counts[s] = entry
            entry[order] += 1

    count_ngrams(text1, count1, 0)
    count_ngrams(text2, count2, 1)

    return sum(a * b for a, b in counts.values()) / (count1 * count2)


def plot_fingerprint(text: str | list[str], alphabet: Alphabet, expected: str | list[str] | None = None) -> tuple[Figure, Axes]:
    fig, ax = plt.subplots()
    ax.set_xlabel('Letter')
    ax.set_ylabel('Fraction of occurence')

    fp = fingerprint(text, alphabet)
    xs = alphabet.symbols()
    ys = [ fp.get(s) or 0 for s in xs ]
    ax.bar(xs, ys, label='Measured')

    if expected is not None:
        fp = fingerprint(expected or '', alphabet)
        xs = alphabet.symbols()
        ys = [ fp.get(s) or 0 for s in xs ]
        ax.bar(xs, ys, color='#eeaa9999', label='Expected')
        ax.legend()

    return fig, ax

def plot_ioc_split_by_keylengths(text: str | list[str], alphabet: Alphabet, keylen_range = range(1,21)) -> tuple[Figure, Axes]:
    # theoretically also possible with boxplots, but I find this to give good visualizations

    fig, ax = plt.subplots()
    ax.set_xlabel('Hypothetical key length')
    ax.set_ylabel('Index of coincidence')

    xs = keylen_range
    ys = []

    for keylen in keylen_range:
        every = [ ioc(text[start::keylen], alphabet) / expected_ioc(alphabet) for start in range(keylen) ]
        avg = sum(every) / keylen
        ys.append(avg)

    ax.bar(xs, ys)
    ax.set_ylim(bottom=min(max(min(ys) - 0.1, 0), 1))

    return fig, ax
