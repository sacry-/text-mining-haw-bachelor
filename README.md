
### Bachelor ###

[Informatik Bachelor Material](http://www.haw-hamburg.de/fakultaeten-und-departments/ti/fakultaetsservicebuero/abschlussarbeiten.html#c107779)

[LaTex zip Download Link](http://www.haw-hamburg.de/fileadmin/user_upload/FakTI/FSB_TI/Abschlussarbeiten/I/haw-vorlage_LaTeX.zip)

### Setup ###

Scraping and Indexing
```python
# Generally just cool, does almost what I actually want to create.. :)
$ pip3 install newspaper
# Great for any scraping http://scrapy.org/doc/
$ pip3 install scrapy
# detecting language of articles
$ pip3 install langdetect
```

Parsing and Text Processing
```python
# Python version 3.4.2 used
# Scientific computing in python
$ pip3 install numpy
$ pip3 install scipy
$ pip3 install matplotlib
# Python NLTK 3.0 http://www.nltk.org/install.html
# Installing the SciPy Stack — SciPy.org

# Parsing...
$ pip3 install beautifulsoup4

# English dictionary
$ brew install enchant
$ pip3 install pyenchant

# Pos Tagging, Tokenization, Awesome Preprocessing!
# https://honnibal.wordpress.com/2013/09/11/a-good-part-of-speechpos-tagger-in-about-200-lines-of-python/
$ pip3 install -U git+https://github.com/sloria/textblob-aptagger.git@dev

# http://honnibal.github.io/spaCy/index.html
# $ pip3 install spacy
# $ python -m spacy.en.download

# https://textblob.readthedocs.org/
$ pip3 install textblob

# interface from python to the 
# Stanford NER Tagger download Project
```

Clustering
```python
# https://radimrehurek.com/gensim/install.html
pip3 install -U gensim
```

Infrastructure
```python
# Install Redis
$ brew install redis
$ pip3 install redis-py

# Install Elastic Search
pip3 install elasticsearch
pip3 install elasticsearch-dsl
```

