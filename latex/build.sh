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

function copy_thesis {
  if [ -f thesis.pdf ]
  then
    mv thesis.pdf ..
  else
    mv thesis.dvi ..
  fi
}

function compile {
  latex -interaction=batchmode thesis.tex
  bibtex thesis.aux
  # makeglossaries thesis
  for i in 1 2
  do
    latex -interaction=batchmode thesis.tex
  done
}

function to_pdf {
  dvips thesis.dvi
  ps2pdf thesis.ps
}


cd "out" && copy_resources_to_out && clear && compile || copy_thesis

