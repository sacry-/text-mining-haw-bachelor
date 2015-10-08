#!/bin/bash

function clear {
  for i in aux idx lof log lot nlo synctex.gz toc blg bbl dvi
  do
    rm -f thesis.$i
  done
}

function copy_resources_to_out {
  cp ../hawstyle.sty .
  cp ../thesis.bib .
  cp -r ../logo .
  cp ../*.tex .
}

function texify {
  /usr/texbin/latex -interaction=batchmode thesis.tex
}

function compile {
  texify
  /usr/texbin/bibtex thesis.aux
  # makeglossaries thesis
  texify
  texify
}

function to_pdf {
  dvips thesis.dvi
  ps2pdf thesis.ps
}

cd "out" && copy_resources_to_out && clear && compile


