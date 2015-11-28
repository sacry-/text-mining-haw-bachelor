
### Bachelor ###

- <a href="http://www.haw-hamburg.de/fakultaeten-und-departments/ti/fakultaetsservicebuero/abschlussarbeiten.html#c107779" target="_blank">Informatik Bachelor Material</a>

- <a href="http://www.haw-hamburg.de/fileadmin/user_upload/FakTI/FSB_TI/Abschlussarbeiten/I/haw-vorlage_LaTeX.zip" target="_blank">LaTex zip Download Link</a>


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

# Wikipedia
# dump
https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2
# Libraries for working on wikipedia dumps or APIs
http://pythonhosted.org/mediawiki-utilities/
```


### ENVIRONMENT ###
Setup your environment by either configuring the <b>config/app_config.json</b> with absolute paths or set the following variables to your global <b>ENV</b>

1. "stanford_ner_jar" : "full/path/to/stanford-ner.jar"
2. "stanford_classifier" : "full/path/to/classifiers/english.muc.7class.distsim.crf.ser.gz"
3. "logpath" : "full/path/to/logs"
4. "redis_host" : "localhost"
5. "redis_port" : "6379"
6. "elastic_host" : "localhost"
7. "elastic_port" : "9200"


### Command line tool ###
If you have anything setup and your environment configured you can setup the command line tool like so, in your global configuration point at the file news-clusty/news_clusty_facade.py e.g.

alias news-clusty="full/path/to/news-clusty/news_clusty_facade.py" and use it like this:

```python
  news-clusty --help
  news-clusty scrape
  news-clusty preprocess
  news-clusty cluster strategy
```

Note that this tool is not a generalized abstraction. It is great to scrape and preprocess your data, the clustering only happens if you provide scripts that are used from the shell (not done).

As of now this is no release. There are a lot of open questions and it is clear that some designs need to be rethought. There need to be more options etc. etc.



