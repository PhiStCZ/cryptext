# Cryptext

Cryptext is a Python commandline library / application for working with text-based ciphers. At this point, I only really use it for solving Cicada 3301's Liber Primus, but the code is designed to be reusable for other, similar endeavors.

Cryptext is designed to be versatile, allowing it to work with non-traditional alphabets. It also aims for ease-of-use, so that using it as a library is as easy as possible. It does *not* aim for performance at this point, which could cause problems to anyone who tries bruteforcing ciphers with it, but for most use-cases, it should suffice.

## Installation

To run Cryptext yourself, you will need Python 3, and with it (actually with it's package manager `pip`), install the packages in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

To compile the exploration report documents (in the `documents/` directory), you will also need a [Quarto](https://quarto.org/) package installed externally. Once that's done, you can simply use the `documents/Makefile` to build any/all of the report documents (note that if you use a python virtual environment, you need to activate it before running `make`).

## Credits

Thanks to the creators of the [3301 Files repo](https://github.com/rtkd/iddqd) for the transcription of the Liber Primus to plaintext, this repo uses a slightly modified custom version (either because of mistakes in the original, or for increased clarity, or just for fun).
