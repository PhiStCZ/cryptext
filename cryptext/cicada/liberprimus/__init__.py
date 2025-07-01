'''
This module implements classes and functions for working with content
of Liber Primus.

The loaded content can be split into parts according to this (transitive)
inclusion relation:

```
#  Book (or chapter - Intus)
#             ^
#             |
#          Section
#     +-----^  ^-----+
#     |              |
# Paragraph         Page
#    ^   ^-------+---^
#    |           |
# Sentence     Line
#    ^
#    |
#   Word
```

While the content is partitioned to the best of the developer's knowledge,
there are some assumptions made, e.g. that sections are on distinct pages,
which it is not confirmed.
'''


from .liberprimus import \
    load_all, \
    load_unsolved, \
    load_before_unsolved, \
    load_fake_unsolved, \
    section_title, \
    section_warning, \
    section_chapter_1, \
    section_welcome, \
    section_some_wisdom, \
    section_koan_1, \
    section_the_loss_of_divinity, \
    section_koan_2, \
    section_an_instruction, \
    section_crosses, \
    section_spirals, \
    section_branches, \
    section_moebius, \
    section_mayfly, \
    section_wing_tree, \
    section_cuneiform, \
    section_spiral_branches, \
    section_an_end, \
    section_parable, \
    paragraph_54_55_jpg, \
    section_warning_decrypted, \
    section_welcome_decrypted, \
    section_koan_1_decrypted, \
    section_koan_2_decrypted, \
    load_before_unsolved_decrypted, \
    LiberPrimus, \
    Section, \
    Paragraph, \
    Sentence, \
    Page, \
    Line
