"""
Batool Salloum, Christian Johansson, Inaya Alkhatib, Kevine Shima
CSI CUE: LSAT Prep App
2023
Professor Silveyra
This file creates a category dictionary from CSV LSAT dataset. This includes preprocessing text in standard NLP process.
Resulting dictionary categories (keys) contain the words with counts (values) for each said category.
"""

import csv
import re
import string
import json
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def main():
    categoryDictionary = makeDictionary()
    processDictionary(categoryDictionary)
    saveDictionary(categoryDictionary)


def makeDictionary():
    dictionary = dict()
    with open('Analytical Reasoning/reclor_data/test.csv') as csvFile:
        reader = csv.reader(csvFile)
        headers = True
        for row in reader:
            if headers:
                headers = False
            else:
                dictionary[row[7]] = dictionary.get(row[7], "") + row[1]
    return dictionary


def processDictionary(dictionary):
    for category in dictionary:
        lowerCaseText = dictionary.get(category).lower()
        numRemoval = re.sub(r'\d+', '', lowerCaseText)
        punctuationFree = "".join([word if word not in string.punctuation else " " for word in numRemoval])
        noWhiteSpace = punctuationFree.split()

        stop_words = stopwords.words("english")
        filteredText = " ".join([word for word in noWhiteSpace if word not in stop_words])

        wordnet_lemmatizer = WordNetLemmatizer()
        lemmatizedText = [wordnet_lemmatizer.lemmatize(word) for word in (filteredText.split())]

        categoryDict = dict()
        for word in lemmatizedText:
            categoryDict[word] = categoryDict.get(word, 0) + 1

        dictionary[category] = categoryDict


def saveDictionary(dictionary):
    with open("categoryDictionary.json", "w") as outfile:
        json.dump(dictionary, outfile)

if __name__ == '__main__':
    main()
