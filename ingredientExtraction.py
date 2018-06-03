from nltk import RegexpParser
from nltk import pos_tag, word_tokenize
from nltk.tree import Tree

from Ingredient import Ingredient
from scraper import scrapeWebsite

# CONSTANTS
NOUN_PHRASE_TAG = "NP"
UNIT_CHUNK_TAG = "UP"
CARDINAL_NUMBER_TAG = "CD"
LEMMA_INDEX = 0
POS_TAG_INDEX = 1
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


def split_unit_chunk(unitChunk):
    amount = []
    units = []
    for thing in unitChunk:
        if thing[POS_TAG_INDEX] == CARDINAL_NUMBER_TAG:
            amount.append(thing[LEMMA_INDEX])
        else:
            units.append(thing[LEMMA_INDEX])
    return amount, units


def extract_full_ingredient_name(ingredientChunk):
    ingredient = []
    for thing in ingredientChunk:
        ingredient.append(thing[LEMMA_INDEX])
    return ingredient


def extract_elements_from_parsed_list_item(parsedListItem):
    amount_number, unit, ingredient = [], [], []
    if len(parsedListItem) > 1:
        amount, unitOfMeasure, *rest = parsedListItem
        if type(amount) is Tree and type(unitOfMeasure) is Tree:
            if amount.label() == UNIT_CHUNK_TAG:
                amount_number, unit = split_unit_chunk(amount)
            if unitOfMeasure.label() == NOUN_PHRASE_TAG:
                ingredient = extract_full_ingredient_name(unitOfMeasure)
    return amount_number, unit, ingredient


def extract_elements_from_list_item(tokenized_list_item, chunk_pattern):
    ingredient_first_parser = RegexpParser(chunk_pattern)
    tree = ingredient_first_parser.parse(tokenized_list_item)
    amount, unit, ingredient = extract_elements_from_parsed_list_item(tree)
    return amount, unit, ingredient


# give the url as a string, it can be url from any site listed below

# give the url as a string, it can be url from any site listed below
title, total_time, ingredients, instructions, links = \
    scrapeWebsite('http://allrecipes.com/Recipe/Apple-Cake-Iv/Detail.aspx')


# go through each ingredient, and chunk it
# first try to get the unit of measure first, and then the ingredient itself
# this works for "5 cups blue eggs"
# if that doesnt work, then get the ingredient first and then the unit of measure
# this works for "5 eggs"
def extract_ingredients_from_list(ingredientList):
    extracted_ingredients = []
    for item in ingredientList:
        extracted_ingredients.append(
            extract_ingredient_from_item(extracted_ingredients, item))
    return extracted_ingredients


def extract_ingredient_from_item(extracted_ingredients, item):
    tokens = pos_tag(word_tokenize(item))
    amount, unit, ingredient = \
        extract_elements_from_list_item(tokens, units_first_chunk_pattern)
    if amount and unit and ingredient:
        return Ingredient(amount, unit, ingredient)
    amount, unit, ingredient = \
        extract_elements_from_list_item(tokens, units_last_chunk_pattern)
    if amount and ingredient:
        return Ingredient(amount, unit, ingredient)


for elm in extract_ingredients_from_list(ingredients):
    print(elm)