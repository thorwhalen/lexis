
# lexis
Wordnet wrapper - Easy access to words and their relationships

To install:	```pip install lexis```

The key-value (i.e. dict-list) wrapper to nltk.corpus.wordnet.

Your no fuss gateway to (English) words.

The easiest way to get nltk.corpus.wordnet is

The `nltk` dependency is installed for you when installing 
`lexis`, but the wordnet data is not downloaded automatically.
To do so (only once), go to a python console and do:
```
>>> import nltk; nltk.download('wordnet')  # doctest: +SKIP
```

If you don't like that way, [see here](https://www.nltk.org/install.html) 
for other ways to get wordnet.

The central construct of this module is the Synset 
(a set of synonyms that share a common meaning).
To see a few things you can do with Synsets, naked, 
[see here](https://www.nltk.org/howto/wordnet.html).

Here we put a py2store wrapper around this stuff.

What is WordNet? https://wordnet.princeton.edu/
