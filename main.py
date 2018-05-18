import collections

from recipe_scrapers import scrape_me
from nltk import RegexpParser
from textblob import TextBlob

from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

# give the url as a string, it can be url from any site listed below
scrape_me = scrape_me('http://allrecipes.com/Recipe/Apple-Cake-Iv/Detail.aspx')

scrape_me.title()
scrape_me.total_time()
ingredients = scrape_me.ingredients()
scrape_me.instructions()
scrape_me.links()
units_first_chunk_pattern = r"""
  UP: {<CD>+<NN|NNS>{0,1}}   # chunk units of measure
  NP: {<DT|PP\$>?<JJ|VBG|VBD>*<NN>+}   # chunk determiner/possessive, adjectives and noun
      {<NNP>+}                # chunk sequences of proper nouns

"""

units_last_chunk_pattern = r"""
  NP: {<DT|PP\$>?<JJ|VBG|VBD>*<NN>+}   # chunk determiner/possessive, adjectives and noun
      {<NNP>+}                # chunk sequences of proper nouns
  UP: {<CD>+<NN|NNS>{0,1}}   # chunk units of measure
"""
cp = RegexpParser(units_first_chunk_pattern)
for ingredient in ingredients:
    print(ingredient)
    tokens = pos_tag(word_tokenize(ingredient))
    tree = cp.parse(tokens)
    treeList = [x for x in tree]
    if(len(treeList) > 1):
        first, second ,*rest = treeList
        print(first.label())