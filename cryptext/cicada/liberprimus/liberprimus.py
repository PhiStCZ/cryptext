from ..abc_futhorc import futhorc
from ..gematriaprimus import encode
from ...ciphers import atbash, caesar, vigenere

import os

SEP_LINE = '/'
SEP_LINE_HARD = '\\'
SEP_PAGE = '%'
SEP_SECTION = '$'
SEP_PARAGRAPH = '&'
CTRL_CHARS = ( SEP_LINE, SEP_LINE_HARD, SEP_PAGE, SEP_SECTION, SEP_PARAGRAPH )

SPACE = ' '
SEP_WORD = '-'
SEP_CLAUSE1 = ','
SEP_CLAUSE2 = ';'
SEP_SENTENCE = '.'

APOSTROPHE = '\''
QUOTE = '"'

WORD_SEP_CHARS = [ SPACE, SEP_WORD, SEP_CLAUSE1, SEP_CLAUSE2, QUOTE ]

SECTION_NAMES = (
    'Title',
    'Warning',
    'Chapter 1',
    'Welcome',
    'Some Wisdom',
    'Koan 1',
    'The Loss Of Divinity',
    'Koan 2',
    'An Instruction',
    'Crosses',
    'Spirals',
    'Branches',
    'Moebius',
    'Mayfly',
    'Wing Tree',
    'Cuneiform',
    'Spiral Branches',
    'An End',
    'Parable',
)

LP_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'liber-primus-transcription-transformed.txt')


def _rm_ctrl_chars(text: str) -> str:
    for ch in CTRL_CHARS:
        text = text.replace(ch, '')
    return text

def _trim_last_paragraph_ending(text: str) -> str:
    while text[-1] == SEP_PARAGRAPH: text = text[:-1]
    return text



class Line:
    def __init__(self, content: str):
        self._content = content

    def content(self) -> str:
        ''' Returns the entire text content (slightly prettified, e.g. removed line endings). '''
        return _rm_ctrl_chars(self._content)

    def symbols(self) -> str:
        ''' Returns only futhorc runes (e.g. no spaces). '''
        return futhorc.filter_symbols(self._content)


class Page:
    def __init__(self, content: str):
        self._content = content

    def content(self) -> str:
        ''' Returns the entire text content (slightly prettified, e.g. removed line endings). '''
        return _rm_ctrl_chars(
            _trim_last_paragraph_ending(self._content) \
                .replace(SEP_LINE_HARD, '\n') \
                .replace(SEP_PARAGRAPH, '\n\n')
        )

    def symbols(self) -> str:
        ''' Returns only futhorc runes (e.g. no spaces). '''
        return futhorc.filter_symbols(self._content)

    def lines(self) -> list[Line]:
        ''' Returns the content split into lines. '''
        s = self._content.replace(SEP_LINE_HARD, SEP_LINE).split(SEP_LINE)
        return [ Line(l) for l in s if _rm_ctrl_chars(l) != '' ]

class Sentence:
    def __init__(self, content: str):
        self._content = content

    def content(self) -> str:
        ''' Returns the entire text content (slightly prettified, e.g. removed line endings). '''
        return _rm_ctrl_chars(self._content)

    def symbols(self) -> str:
        ''' Returns only futhorc runes (e.g. no spaces). '''
        return futhorc.filter_symbols(self._content)

    def all_words(self) -> list[str]:
        '''
        Returns the content split into words. Note that words may include non-
        alphabetical symbols such as apostrophes, numbers, and latin characters.
        '''
        content = _rm_ctrl_chars(self._content)
        for ch in WORD_SEP_CHARS:
            content = content.replace(ch, ' ')
        return content.split()

    def words(self) -> list[str]:
        '''
        Returns futhorc runes of the content split into words. Note that fully
        non-rune words are not included, which changes the numbering from all_words.
        '''
        words = self.all_words()
        words = [ futhorc.filter_symbols(w) for w in words ]
        words = [ w for w in words if len(w) > 0 ]
        return words

class Paragraph:
    def __init__(self, content: str):
        self._content = content

    def content(self) -> str:
        ''' Returns the entire text content (slightly prettified, e.g. removed line endings). '''
        return _rm_ctrl_chars(self._content)

    def symbols(self) -> str:
        ''' Returns only futhorc runes (e.g. no spaces). '''
        return futhorc.filter_symbols(self._content)

    def lines(self) -> list[Line]:
        ''' Returns the content split into lines. '''
        sp_content = self._content.replace(SEP_LINE_HARD, SEP_LINE).split(SEP_LINE)
        return [
            Line(l) for l in sp_content
            if _rm_ctrl_chars(l) != ''
        ]

    def sentences(self) -> list[Sentence]:
        ''' Returns the content split into sentences. '''
        sp_content = self._content.split(SEP_SENTENCE)
        return [
            Sentence(s) for s in sp_content
            if _rm_ctrl_chars(s) != ''
        ]

    def all_words(self) -> list[str]:
        '''
        Returns the content split into words. Note that words may include non-
        alphabetical symbols such as apostrophes, numbers, and latin characters.
        '''
        words: list[str] = []
        for s in self.sentences():
            words += s.all_words()
        return words

    def words(self) -> list[str]:
        '''
        Returns futhorc runes of the content split into words. Note that fully
        non-rune words are not included, which changes the numbering from all_words.
        '''
        words: list[str] = []
        for s in self.sentences():
            words += s.words()
        return words

class Section:
    def __init__(self, content: str, name: str|None = None):
        self._content = content
        self._name = name

    def name(self) -> str:
        ''' Returns the name of the section. '''
        return self._name or '(unknown)'

    def content(self) -> str:
        ''' Returns the entire text content (slightly prettified, e.g. removed line endings). '''
        return _rm_ctrl_chars(
            _trim_last_paragraph_ending(self._content) \
                .replace(SEP_LINE_HARD, '\n') \
                .replace(SEP_PARAGRAPH, '\n\n')
        )

    def symbols(self) -> str:
        ''' Returns only futhorc runes (e.g. no spaces). '''
        return futhorc.filter_symbols(self._content)

    def pages(self) -> list[Page]:
        ''' Returns the content split into pages. '''
        sp_content = self._content.split(SEP_PAGE)
        return [ Page(p) for p in sp_content if _rm_ctrl_chars(p) != '' ]

    def paragraphs(self) -> list[Paragraph]:
        ''' Returns the content split into paragraphs. '''
        sp_content = self._content.split(SEP_PARAGRAPH)
        return [ Paragraph(p) for p in sp_content if _rm_ctrl_chars(p) != '' ]

    def lines(self) -> list[Line]:
        ''' Returns the content split into lines. '''
        sentences: list[Line] = []
        for p in self.paragraphs():
            sentences += p.lines()
        return sentences

    def sentences(self) -> list[Sentence]:
        ''' Returns the content split into sentences. '''
        sentences: list[Sentence] = []
        for p in self.paragraphs():
            sentences += p.sentences()
        return sentences

    def all_words(self) -> list[str]:
        '''
        Returns the content split into words. Note that words may include non-
        alphabetical symbols such as apostrophes, numbers, and latin characters.
        '''
        words: list[str] = []
        for s in self.paragraphs():
            words += s.all_words()
        return words

    def words(self) -> list[str]:
        '''
        Returns futhorc runes of the content split into words. Note that fully
        non-rune words are not included, which changes the numbering from all_words.
        '''
        words: list[str] = []
        for s in self.paragraphs():
            words += s.words()
        return words

class LiberPrimus:
    def __init__(self, beginning_section_idx: int = 0) -> None:
        with open(LP_PATH, 'r') as reader:
            # newlines in the file are only for user-readability
            self._content = reader.read().replace('\n', '')
            self._beginning_section_idx = beginning_section_idx

    def content(self) -> str:
        ''' Returns the entire text content (slightly prettified, e.g. removed line endings). '''
        return _rm_ctrl_chars(
            _trim_last_paragraph_ending(self._content) \
                .replace(SEP_LINE_HARD, '\n') \
                .replace(SEP_PARAGRAPH, '\n\n') \
                .replace(SEP_SECTION, '~~~\n\n')
        )

    def symbols(self) -> str:
        ''' Returns only futhorc runes (e.g. no spaces). '''
        return futhorc.filter_symbols(self._content)


    def sections(self) -> list[Section]:
        ''' Returns the content split into sections. '''
        sp_content = [
            s for s in self._content.split(SEP_SECTION) if _rm_ctrl_chars(s) != ''
        ]
        return [
            Section(s, n) for s, n in zip(sp_content, SECTION_NAMES[self._beginning_section_idx:])
        ]

    def pages(self) -> list[Page]:
        ''' Returns the content split into pages. '''
        pages: list[Page] = []
        for s in self.sections():
            pages += s.pages()
        return pages

    def paragraphs(self) -> list[Paragraph]:
        ''' Returns the content split into paragraphs. '''
        paragraphs: list[Paragraph] = []
        for s in self.sections():
            paragraphs += s.paragraphs()
        return paragraphs

    def lines(self) -> list[Line]:
        ''' Returns the content split into lines. '''
        lines: list[Line] = []
        for s in self.sections():
            lines += s.lines()
        return lines

    def sentences(self) -> list[Sentence]:
        ''' Returns the content split into sentences. '''
        sentences: list[Sentence] = []
        for s in self.sections():
            sentences += s.sentences()
        return sentences

    def all_words(self) -> list[str]:
        '''
        Returns the content split into words. Note that words may include non-
        alphabetical symbols such as apostrophes, numbers, and latin characters.
        '''
        words: list[str] = []
        for s in self.sections():
            words += s.all_words()
        return words

    def words(self) -> list[str]:
        '''
        Returns futhorc runes of the content split into words. Note that fully
        non-rune words are not included, which changes the numbering from all_words.
        '''
        words: list[str] = []
        for s in self.sections():
            words += s.words()
        return words



def load_all():
    ''' Loads the entire known Liber Primus. '''
    return LiberPrimus()

def load_unsolved():
    ''' Loads Liber Primus' sections from Crosses to Spiral branches. '''
    lp = LiberPrimus(SECTION_NAMES.index('Crosses'))
    sheogmiaf_idx = lp._content.index('ᛋᚻᛖᚩᚷᛗᛡᚠ')
    an_end_idx = lp._content.index('ᚫᛄ-ᛟᛋᚱ')
    lp._content = lp._content[sheogmiaf_idx:an_end_idx]
    return lp

def load_fake_unsolved():
    ''' Loads random low-doublet symbols with the structure of unsolved Liber Primus (all content except the rune values remains the same). '''
    lp = load_unsolved()
    fake_runes = futhorc.random_ld(len(lp.symbols()))
    new_content = []
    lpi, flpi = 0, 0
    while lpi != len(lp._content):
        if futhorc.has(lp._content[lpi]):
            new_content.append(fake_runes[flpi])
            lpi += 1
            flpi += 1
        else:
            new_content.append(lp._content[lpi])
            lpi += 1

    lp._content = ''.join(new_content)
    return lp

def load_before_unsolved():
    ''' Loads Liber Primus' sections from its beginning to the last section before Crosses. '''
    lp = LiberPrimus()
    sheogmiaf_idx = lp._content.index('ᛋᚻᛖᚩᚷᛗᛡᚠ')
    lp._content = lp._content[:sheogmiaf_idx]
    return lp

def section_title(): return LiberPrimus().sections()[0]

def section_warning(): return LiberPrimus().sections()[1]

def section_chapter_1(): return LiberPrimus().sections()[2]

def section_welcome(): return LiberPrimus().sections()[3]

def section_some_wisdom(): return LiberPrimus().sections()[4]

def section_koan_1(): return LiberPrimus().sections()[5]

def section_the_loss_of_divinity(): return LiberPrimus().sections()[6]

def section_koan_2(): return LiberPrimus().sections()[7]

def section_an_instruction(): return LiberPrimus().sections()[8]

def section_crosses(): return LiberPrimus().sections()[9]

def section_spirals(): return LiberPrimus().sections()[10]

def section_branches(): return LiberPrimus().sections()[11]

def section_moebius(): return LiberPrimus().sections()[12]

def section_mayfly(): return LiberPrimus().sections()[13]

def section_wing_tree(): return LiberPrimus().sections()[14]

def section_cuneiform(): return LiberPrimus().sections()[15]

def section_spiral_branches(): return LiberPrimus().sections()[16]

def section_an_end(): return LiberPrimus().sections()[17]

def section_parable(): return LiberPrimus().sections()[18]

def paragraph_54_55_jpg(): return section_spiral_branches().paragraphs()[-1]


def _decrypt_warning(text: str): return atbash(text, futhorc)
def _decrypt_welcome(text: str): return vigenere(text, encode('divinity'), futhorc, True, [48, 74, 84, 132, 159, 160, 250, 421, 443, 465, 514])
def _decrypt_koan_1(text: str): return caesar(atbash(text, futhorc), futhorc, 3)
def _decrypt_koan_2(text: str): return vigenere(text, encode('firfumferenfe'), futhorc, True, [49, 58])

def decrypt_using_lambda(section: Section, lbd) -> Section: #: Callable[[str], str]):
    section._content = lbd(section._content)
    return section

def section_warning_decrypted():
    return decrypt_using_lambda(section_warning(), _decrypt_warning)

def section_welcome_decrypted():
    return decrypt_using_lambda(section_welcome(), _decrypt_welcome)

def section_koan_1_decrypted():
    return decrypt_using_lambda(section_koan_1(), _decrypt_koan_1)

def section_koan_2_decrypted():
    return decrypt_using_lambda(section_koan_2(), _decrypt_koan_2)

def load_before_unsolved_decrypted():
    lp = load_before_unsolved()
    sections = lp._content.split(SEP_SECTION)

    lp._content = SEP_SECTION.join(
        fn(s) if fn is not None else s for s, fn in zip(sections, [
            None,
            _decrypt_warning,
            None,
            _decrypt_welcome,
            None,
            _decrypt_koan_1,
            None,
            _decrypt_koan_2,
            None,
        ]))

    return lp
