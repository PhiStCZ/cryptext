'''
This module implements functions for finding patterns in text, which can be
used to help identify the used cipher.
'''

from .analytics import \
    diff_text, \
    fingerprint, \
    find_repeated_ngrams, \
    ioc, \
    expected_ioc, \
    crosstext_ioc, \
    plot_fingerprint, \
    plot_ioc_split_by_keylengths
