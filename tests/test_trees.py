"""Tests for iTree/HyponymTree/HyponymForest and the small wordnet helpers.

The pure tree tests need no data; the wordnet ones skip when the corpus is not installed.
"""

import pytest

import lexis
from lexis import HyponymForest, HyponymTree, iTree


def _tree():
    root = iTree("root")
    a, b, c = iTree("a"), iTree("b"), iTree("c")
    root.children = [a, b]
    a.children = [c]
    return root, a, b, c


def test_itree_iterates_children_before_parents():
    root, a, b, c = _tree()
    assert [n.value for n in root] == ["c", "a", "b", "root"]
    assert [n.value for n in iTree("solo")] == ["solo"]


def test_itree_info_string_indents_by_depth():
    root, *_ = _tree()
    assert root.tree_info_str() == "root\n  a\n    c\n  b\n"
    assert root.tree_info_str(node_2_str=lambda n: n.value.upper(), tab_str="--") == (
        "ROOT\n--A\n----C\n--B\n"
    )


@pytest.fixture(scope="module")
def wn():
    nltk_wn = pytest.importorskip("nltk.corpus").wordnet
    try:
        nltk_wn.synset("terrier.n.01")
    except LookupError:
        pytest.skip("wordnet corpus not installed")
    return nltk_wn


def test_hyponym_tree_from_name_and_synset(wn):
    t = HyponymTree("terrier.n.01")
    assert str(t) == "terrier.n.01" and repr(t) == "terrier.n.01"
    assert len(t.children) == len(wn.synset("terrier.n.01").hyponyms())
    assert HyponymTree(wn.synset("terrier.n.01")).value == t.value
    leaves = t.leafs()
    assert t in leaves and len(leaves) > len(t.children)  # leafs() lists every node, root last
    assert leaves[-1] is t


def test_of_hyponyms_builds_the_same_shape(wn):
    syn = wn.synset("terrier.n.01")
    a, b = HyponymTree(syn), HyponymTree.of_hyponyms(syn)
    assert [n.value for n in a] == [n.value for n in b]


def test_forest_collects_leafs_and_rejects_duplicates(wn):
    f = HyponymForest(["terrier.n.01", "hound.n.01"])
    assert all(isinstance(t, HyponymTree) for t in f.tree_list)
    assert len(f.leafs()) == len(HyponymTree("terrier.n.01").leafs()) + len(
        HyponymTree("hound.n.01").leafs()
    )
    with pytest.raises(AssertionError, match="unique"):
        HyponymForest(["terrier.n.01", "terrier.n.01"])


def test_unknown_node_2_str_method():
    with pytest.raises(ValueError, match="Unknown node_2_str_function"):
        HyponymTree.get_node_2_str_function("nonsense")


def test_wordnet_helpers(wn):
    assert lexis.get_singular("dogs") == "dog"
    assert lexis.get_singular("zzzzqx") == "zzzzqx"  # unknown words come back unchanged
    text = lexis.word_definitions_string("dog")
    assert text.splitlines()[0].startswith("0: ") and "dog.n.01" in text


@pytest.mark.parametrize("method", ["name", "lemma_names", "name_and_def", "lemmas_and_def", "all"])
def test_node_2_str_methods_work_with_current_nltk(wn, method):
    t = HyponymTree("terrier.n.01")
    assert "terrier" in t.tree_info_str(HyponymTree.get_node_2_str_function(method))


def test_df_for_excel_export_and_print_word_lemmas(wn, capsys):
    from lexis import print_word_lemmas

    df = HyponymTree("terrier.n.01")._df_for_excel_export()
    assert len(df) > 1 and "terrier" in df.to_string()
    print_word_lemmas("terrier")
    assert "terrier" in capsys.readouterr().out
