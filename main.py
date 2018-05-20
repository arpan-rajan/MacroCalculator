import collections

from recipe_scrapers import scrape_me
from nltk import RegexpParser
from textblob import TextBlob

from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
#index for the actual text of the word in a parse tree
LEMMA_INDEX = 0
#index for part of speed tag of a word in a parse tree
POS_TAG_INDEX = 1
# give the url as a string, it can be url from any site listed below
scrape_me = scrape_me('http://allrecipes.com/Recipe/Apple-Cake-Iv/Detail.aspx')

scrape_me.title()
scrape_me.total_time()
ingredients = scrape_me.ingredients()
scrape_me.instructions()
scrape_me.links()
units_first_chunk_pattern = r"""
  UP: {<CD>+<NN|NNS>{0,1}}   # chunk units of measure
  NP: {<DT|PP\$>?<JJ|VBG|VBD>*<NN|NNS>+}   # chunk determiner/possessive, adjectives and noun
      {<NNP>+}                # chunk sequences of proper nouns

"""

units_last_chunk_pattern = r"""
  NP: {<DT|PP\$>?<JJ|VBG|VBD>*<NN|NNS>+}   # chunk determiner/possessive, adjectives and noun
      {<NNP>+}                # chunk sequences of proper nouns
  UP: {<CD>+<NN|NNS>{0,1}}   # chunk units of measure
"""
cp = RegexpParser(units_first_chunk_pattern)


def splitUnitPhrase(unitChunk):
    amount = []
    units = []
    for thing in unitChunk:
        if (thing[POS_TAG_INDEX] == "CD"):
            amount.append(thing[LEMMA_INDEX])
        else:
            units.append(thing[LEMMA_INDEX])
    return amount, units


def extractFullIngredientName(ingredientChunk):
    ingredient = []
    for thing in ingredientChunk:
        ingredient.append(thing[LEMMA_INDEX])
    return ingredient


def extractElementsFromListItem(parsedListItem):
    amountNumber, unit, ingredient = [],[],[]
    if (len(parsedListItem) > 1):
        amount, unitOfMeasure, *rest = parsedListItem
        if type(amount) is Tree and type(unitOfMeasure) is Tree:
            if (amount.label() == "UP"):
                amountNumber, unit = splitUnitPhrase(amount)
            if (unitOfMeasure.label() == "NP"):
                ingredient = extractFullIngredientName(unitOfMeasure)
    return amountNumber, unit, ingredient


# go through each ingredient, and chunk it
# first try to get the unit of measure first, and then the ingredient itself
# this works for "5 cups blue eggs"
# if that doesnt work, then get the ingredient first and then the unit of measure
# this works for "5 eggs"
for item in ingredients:
    tokens = pos_tag(word_tokenize(item))
    tree = cp.parse(tokens)
    amount, unit, ingredient = extractElementsFromListItem(tree)
    if(amount and unit and ingredient):
        print(amount, unit, ingredient)
        continue
    ingredient_first_parser = RegexpParser(units_last_chunk_pattern)
    tree = ingredient_first_parser.parse(tokens)
    amount, unit, ingredient = extractElementsFromListItem(tree)
    print(amount, unit, ingredient)