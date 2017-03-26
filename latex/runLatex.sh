#!/bin/bash

texBin="/Library/TeX/texbin"

function clear {
  for i in aux idx lof log lot nlo synctex.gz toc blg bbl dvi
  do
    rm -f thesis.$i
  done
}

function copy_resources_to_out {
  cp ../*.sty .
  cp ../thesis.bib .
  cp -r ../logo .
  cp -r ../images/*.png .
  cp ../*.tex .
}

function texify {
  $texBin/pdflatex -interaction=batchmode thesis.tex
}

function compile {
  texify
  $texBin/bibtex thesis.aux
  # makeglossaries thesis
  texify
  texify
}

cd "out" && copy_resources_to_out && clear && compile && open thesis.pdf

