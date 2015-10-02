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

function tex_thesis {
  latex -interaction=batchmode thesis.tex
}

function compile {
  tex_thesis
  bibtex thesis.aux
  # makeglossaries thesis
  tex_thesis
  tex_thesis
}

function to_pdf {
  dvips thesis.dvi
  ps2pdf thesis.ps
}

cd "out" && copy_resources_to_out && clear && compile


