# lexis

The key-value (i.e. dict-list) wrapper to nltk.corpus.wordnet.

Your no fuss gateway to (English) words.

The easiest way to get nltk.corpus.wordnet is

```text
pip install nltk
```

in your terminal, and then in a python console:

```text
>>> import nltk; nltk.download('wordnet')  # doctest: +SKIP
```

If you don’t like that way, [see here](https://www.nltk.org/install.html) for other
ways to get wordnet.

The central construct of this module is the Synset
(a set of synonyms that share a common meaning).
To see a few things you can do with Synsets, naked,
[see here](https://www.nltk.org/howto/wordnet.html).

Here we put a py2store wrapper around this stuff.

What is WordNet? [https://wordnet.princeton.edu/](https://wordnet.princeton.edu/)

## Classes

| [`KvLemma`](#lexis.KvLemma)   |                                                                                                         |
|------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|
| [`KvSynset`](#lexis.KvSynset)  | A thin layer on top of nltk.corpus.reader.wordnet.Synset that will give us a dict-like interface of it. |
| [`Synsets`](#lexis.Synsets)   |                                                                                                         |
| [`Lemmas`](#lexis.Lemmas)    | Acts as a Mapping abc, but with default \_\_len_\_ (implemented by counting keys)                       |

## Functions

| [`callable_attr_names`](#lexis.callable_attr_names)(obj)          | Set of attributes that are not callable                          |
|------------------------------------------------------------------------------------|------------------------------------------------------------------|
| [`fully_defaulted_method_names`](#lexis.fully_defaulted_method_names)(obj) | Set of method names whose arguments all have defaults            |
| [`keyable_attr_names`](#lexis.keyable_attr_names)(obj)           | Set of attribute names of object that can be used as keys        |
| [`is_noun`](#lexis.is_noun)(word)                     | Returns True iff word is a noun.                                 |
| [`is_drawable`](#lexis.is_drawable)(word)                 | Returns True if the word is a physical entity that can be drawn. |
| [`get_singular`](#lexis.get_singular)(word)                | Get the singular form of a word using nltk's wordnet             |

## Package Contents

### lexis.callable_attr_names(obj)

Set of attributes that are not callable

### lexis.fully_defaulted_method_names(obj)

Set of method names whose arguments all have defaults
(so are callable without arguments).

### lexis.keyable_attr_names(obj)

Set of attribute names of object that can be used as keys
(because not callable, or callable without args). Private and dunder names are left out.

### *class* lexis.KvLemma(store=dict)

Bases: `wordnet_element_store_base`(`Lemma`)

```pycon
>>> lm = KvLemma.from_name('vocal.a.01.vocal')
>>> assert len(lm) == len(dict(lm)) == 33
>>> sorted(lm.dict_of_non_empty_values().items())
[('antonyms', [KvLemma('instrumental.a.01.instrumental')]),
 ('count', 1),
 ('derivationally_related_forms', [KvLemma('vocalize.v.02.vocalize')]),
 ('key', 'vocal%3:01:02::'),
 ('lang', 'eng'),
 ('name', 'vocal'),
 ('pertainyms', [KvLemma('voice.n.02.voice')]),
 ('synset', KvSynset('vocal.a.01')),
 ('syntactic_marker', None)]
```

### *class* lexis.KvSynset(store=dict)

Bases: `wordnet_element_store_base`(`Synset`)

A thin layer on top of nltk.corpus.reader.wordnet.Synset that will give us a dict-like interface of it.

Think of “synset” as a “concept”.
For a list (or rather “dict”) of these, checkout `lexis.Synsets`

```pycon
>>> ss = KvSynset.from_name('sound.n.01')
>>> ss
KvSynset('sound.n.01')
```

`ss` is a Mapping (meaning “dict-like”)

```pycon
>>> from typing import Mapping
>>> assert isinstance(ss, Mapping)
```

So let’s list it’s keys:

```pycon
>>> keys = set(ss)
>>> expected_keys = set((
...     'also_sees attributes causes definition entailments examples '
...     'frame_ids hypernym_distances hypernym_paths hypernyms hyponyms in_region_domains '
...     'in_topic_domains in_usage_domains instance_hypernyms instance_hyponyms lemma_names '
...     'lemmas lexname max_depth member_holonyms member_meronyms min_depth name offset '
...     'part_holonyms part_meronyms pos region_domains root_hypernyms similar_tos '
...     'substance_holonyms substance_meronyms topic_domains usage_domains verb_groups'
... ).split())
>>> assert expected_keys <= keys  # newer nltk versions add a few more (e.g. mst)
```

So lots of info about that concept.

```pycon
>>> ss['definition']
'the particular auditory effect produced by a given cause'
>>> ss['examples']
['the sound of rain on the roof', 'the beautiful sound of music']
>>> ss['lemma_names']  # a.k.a. "words used for that concept"
['sound']
```

Retrieve everything at once:

```pycon
>>> d = dict(ss)
>>> len(d.keys() & {'definition', 'also_sees', 'hypernyms'})
3
```

Display items for non-empty values

```pycon
>>> for k, v in sorted(ss.items()):
...     if v:
...         print(f"{k}: {v}")
definition: the particular auditory effect produced by a given cause
examples: ['the sound of rain on the roof', 'the beautiful sound of music']
hypernym_distances: {(KvSynset('attribute.n.02'), 3), (KvSynset('sound_property.n.01'), 1),
...     (KvSynset('property.n.02'), 2), (KvSynset('entity.n.01'), 5), (KvSynset('sound.n.01'), 0),
...     (KvSynset('abstraction.n.06'), 4)}
hypernym_paths: [[KvSynset('entity.n.01'), KvSynset('abstraction.n.06'), KvSynset('attribute.n.02'),
...     KvSynset('property.n.02'), KvSynset('sound_property.n.01'), KvSynset('sound.n.01')]]
hypernyms: [KvSynset('sound_property.n.01')]
hyponyms: [KvSynset('noisiness.n.01'), KvSynset('ring.n.01'), KvSynset('unison.n.03'), KvSynset('voice.n.01')]
lemma_names: ['sound']
lemmas: [KvLemma('sound.n.01.sound')]
lexname: noun.attribute
max_depth: 5
min_depth: 5
name: sound.n.01
offset: 4981139
pos: n
root_hypernyms: [Synset('entity.n.01')]
```

### *class* lexis.Synsets(pos=None)

Bases: `dol.mixins.ReadOnlyMixin`, `dol.Store`

```pycon
>>> s = Synsets()
>>> len(s)
117659
>>> list(s)[:5]
['able.a.01', 'unable.a.01', 'abaxial.a.01', 'adaxial.a.01', 'acroscopic.a.01']
>>> ss = s['sound.n.01']
>>> ss
KvSynset('sound.n.01')
```

And what can you do with a KvSynset?
Well, you’ll just have to check out it’s documentation!

### *class* lexis.Lemmas

Bases: `dol.KvReader`

Acts as a Mapping abc, but with default \_\_len_\_ (implemented by counting keys)
and head method to get the first (k, v) item of the store

### lexis.is_noun(word)

Returns True iff word is a noun.

Warning

```pycon
>>> is_noun('dog')
True
>>> is_noun('run')
False
>>> is_noun('dogs')
True
>>> is_noun('doggy')
True
>>> is_noun('doggies')
True
```

But:

```pycon
>>> is_noun('eat')  # should be False
True
```

### lexis.is_drawable(word)

Returns True if the word is a physical entity that can be drawn.

```pycon
>>> is_drawable('dog')
True
>>> is_drawable('doggies')
True
>>> is_drawable('happy')
False
>>> is_drawable('eat')
False
```

### lexis.get_singular(word)

Get the singular form of a word using nltk’s wordnet

#### SEE ALSO
`get_singular_w_inflect()`, in the `idiom` package, which creates plurals
through a different method, (a rule-based approach).
Once the data is loaded, the present `nltk` is faster than the one made
with `inflect`, but gives less accurate results, since it’s idea of singular is
“the base concept”.

* **Return type:**
  [*str*](https://docs.python.org/3/builtins/stdtypes.html#str)
