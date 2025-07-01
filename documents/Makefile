.PHONY: all clean

qmds := $(wildcard *.qmd)
files := $(patsubst %.qmd, %.html, $(qmds))

all: $(files)

clean:
	rm -r *.html
	rm -r *_files

%.html: %.qmd
	quarto render $*.qmd
