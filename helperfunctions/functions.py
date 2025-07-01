import sys
sys.path.append('../..')
from cryptext.cicada import liberprimus as lp



class PhraseMatch:
    def __init__(self, words: list[str], word_before: str|None = None, word_after: str|None = None):
        self.words: list[str] = words
        self.word_before: str|None = word_before
        self.word_after: str|None = word_after

    def content(self) -> str:
        return '-'.join(self.words)

    def symbols(self) -> str:
        return ''.join(self.words)

def _find_phrase_groups_strict_inner(
        words: list[str],
        word_lens: list[int],
        out_pgroups: dict[tuple[int, ...], list[PhraseMatch]],
        phrase_len: int,
        distinctive_word_len: int = 5,
        include_cross_sentences: bool = False) -> bool:

    if include_cross_sentences and 0 in word_lens: raise Exception('Logic error; inconsistent parameters')
    repeat_found = False

    for i in range(len(word_lens) - phrase_len):
        s = tuple(word_lens[i:i+phrase_len])

        if 0 in s: continue
        if sum(o >= distinctive_word_len for o in s) == 0: continue

        pm = PhraseMatch(words[i:i+phrase_len])
        j = i - 1
        while j >= 0 and word_lens[j] == 0: j -= 1
        pm.word_before = words[j] if j >= 0 else None

        j = i + len(pm.words)
        while j < len(word_lens) and word_lens[j] == 0: j += 1
        pm.word_after = words[j] if j < len(word_lens) else None

        if out_pgroups.get(s) is None: out_pgroups[s] = []
        else: repeat_found = True
        out_pgroups[s].append(pm)

    return repeat_found

def find_phrase_groups_strict(
        section: lp.LiberPrimus | lp.Section,
        exact_phrase_len: int,
        distinctive_word_len: int = 5,
        include_cross_sentences: bool = False) -> list[list[PhraseMatch]]:

    ''' A more naive, and possibly less biased phrase group finder. '''

    if include_cross_sentences:
        words = section.words()
    else:
        words: list[str] = []
        for s in section.sentences(): words += s.words() + [ '' ]

    word_lens = [ len(w) for w in words ]
    pgroups: dict[tuple[int, ...], list[PhraseMatch]] = {}

    _find_phrase_groups_strict_inner(words, word_lens, pgroups, exact_phrase_len, distinctive_word_len, include_cross_sentences)

    return [ pg for pg in pgroups.values() if len(pg) > 1 ]

def find_phrase_groups(
        section: lp.LiberPrimus | lp.Section,
        min_phrase_len: int,
        distinctive_word_len: int = 5,
        include_cross_sentences: bool = False) -> list[list[PhraseMatch]]:

    if include_cross_sentences:
        words = section.words()
    else:
        words: list[str] = []
        for s in section.sentences(): words += s.words() + [ '' ]

    word_lens = [ len(w) for w in words ]
    pgroups: dict[tuple[int, ...], list[PhraseMatch]] = {}

    exact_phrase_len = min_phrase_len
    while True:
        repeat_found = _find_phrase_groups_strict_inner(words, word_lens, pgroups, exact_phrase_len, distinctive_word_len, include_cross_sentences)
        if not repeat_found: break
        exact_phrase_len += 1

    def deduplicate(g_lens, g_size):
        for k in [ g_lens[1:], g_lens[:-1] ]:
            lower_g = pgroups.get(k)
            if lower_g is not None and len(lower_g) <= g_size:
                pgroups.pop(k)
                deduplicate(k, g_size)

    items = [(k, len(v)) for k, v in pgroups.items()]
    for phrase_word_lens, occurence_count in items:
        deduplicate(phrase_word_lens, occurence_count)

    return [ pg for pg in pgroups.values() if len(pg) > 1 ]

def pgroups_to_ppairs(pgroups: list[list[PhraseMatch]]) -> list[list[PhraseMatch]]:
    ppairs: list[list[PhraseMatch]] = []

    for pgroup in pgroups:
        for i in range(len(pgroup) - 1):
            for j in range(i + 1, len(pgroup)):
                ppairs.append([pgroup[i], pgroup[j]])

    return ppairs

MAX_WORDLEN = 15 # 1 reserve, because why not

class RuneMatchStats:
    def __init__(self):
        # Uhhh, yeah, I don't really know how to make this nicer
        self.pairs = 0

        self.runes = 0
        self.rune_matches = 0
        self.words = 0
        self.word_begin_matches = 0

        self.first_word_runes = 0
        self.first_word_rune_matches = 0

        self.first_word_of_length_above = [0] * (MAX_WORDLEN + 1)
        self.first_word_nth_rune_matches = [0] * MAX_WORDLEN
        self.first_word_last_rune_matches = 0

        self.last_word_first_rune_matches = 0
        self.last_rune_matches = 0

        self.first_word_filter_prev_nth_rune_options = [0] * MAX_WORDLEN
        self.first_word_filter_prev_nth_rune_matches = [0] * MAX_WORDLEN

        self.first_word_filter_first_nth_rune_options = [0] * MAX_WORDLEN
        self.first_word_filter_first_nth_rune_matches = [0] * MAX_WORDLEN

        self.word_before_pairs = 0
        self.word_before_first_rune_matches = 0
        self.word_before_last_rune_matches = 0


def _add_phrase_pair(stats: RuneMatchStats, phrase1: PhraseMatch, phrase2: PhraseMatch):
    stats.pairs += 1

    # Total match rate
    stats.runes += sum(len(w) for w in phrase1.words)
    stats.rune_matches += sum(
        sum(r1 == r2 for r1, r2 in zip(w1, w2))
        for w1, w2 in zip(phrase1.words, phrase2.words)
    )

    # First letter of word match rate
    stats.words += len(phrase1.words)
    stats.word_begin_matches += sum(w1[0] == w2[0] for w1, w2 in zip(phrase1.words, phrase2.words))

    firstw1, firstw2 = phrase1.words[0], phrase2.words[0]

    stats.first_word_runes += len(firstw1)
    stats.first_word_rune_matches += sum(r1 == r2 for r1, r2 in zip(firstw1, firstw2))

    for fwi in range(0, MAX_WORDLEN - 1):
        if len(firstw1) > fwi and len(firstw2) > fwi:
            stats.first_word_of_length_above[fwi] += 1

            if firstw1[fwi] == firstw2[fwi]:
                stats.first_word_nth_rune_matches[fwi] += 1

                if len(firstw1) > fwi+1 and len(firstw2) > fwi+1:
                    stats.first_word_filter_prev_nth_rune_options[fwi+1] += 1

                    if firstw1[fwi+1] == firstw2[fwi+1]:
                        stats.first_word_filter_prev_nth_rune_matches[fwi+1] += 1

            if firstw1[0] == firstw2[0]:
                stats.first_word_filter_first_nth_rune_options[fwi] += 1

                if firstw1[fwi] == firstw2[fwi]:
                    stats.first_word_filter_first_nth_rune_matches[fwi] += 1

    if firstw1[-1] == firstw2[-1]:
        stats.first_word_last_rune_matches += 1
    if phrase1.words[-1][0] == phrase2.words[-1][0]:
        stats.last_word_first_rune_matches += 1
    if phrase1.words[-1][-1] == phrase2.words[-1][-1]:
        stats.last_rune_matches += 1

    wb1, wb2 = phrase1.word_before, phrase2.word_before
    if wb1 is not None and wb2 is not None:
        stats.word_before_pairs += 1
        stats.word_before_first_rune_matches += (wb1[0] == wb2[0])
        stats.word_before_last_rune_matches += (wb1[-1] == wb2[-1])

def count_rune_matches(phrases: list[list[PhraseMatch]]) -> RuneMatchStats:
    stats = RuneMatchStats()

    for occurences in phrases:
        for i in range(len(occurences) - 1):
            for j in range(i + 1, len(occurences)):
                _add_phrase_pair(stats, occurences[i], occurences[j])

    return stats
