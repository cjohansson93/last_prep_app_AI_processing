"""
Batool Salloum, Christian Johansson, Inaya Alkhatib, Kevine Shima
CSI CUE: LSAT Prep App
2023
Professor Silveyra
This file creates a category dictionary from CSV LSAT dataset. This includes preprocessing text in standard NLP process.
This includes lower case, number and punctuation removal, clearing stop words and word lemmatization.
Resulting dictionary categories (keys) contain the words with counts (values) for each said category. Dictionary is
saved as a categoryDictionary.JSON file.
"""

import csv
import re
import string
import json
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


"""
Main, calls methods for creating dictionary, preprocessing dictionary values and saving dictionary as JSON.
"""
def main():
    categoryDictionary = makeDictionary()
    processDictionary(categoryDictionary)
    saveDictionary(categoryDictionary)


"""
Creates dictionary of questions(values) for 16 different question categories (keys) from Logical Reasoning test csv.
@return Returns dictionary
"""
def makeDictionary():
    dictionary = dict()
    with open('Analytical Reasoning/reclor_data/test.csv') as csvFile:
        reader = csv.reader(csvFile)
        headers = True
        for row in reader:
            # Doesn't store the fieldnames as categories
            if headers:
                headers = False
            # Stores question category at key and questions as value
            else:
                dictionary[row[7]] = dictionary.get(row[7], "") + " " + row[1]
    return dictionary


"""
Preprocesses text (value) in standard NLP process for each category (key) in dictionary. This includes lower case, 
number and punctuation removal, clearing stop words and word lemmatization.
@param dictionary Dictionary created in nameDictionary()
"""
def processDictionary(dictionary):
    for category in dictionary:
        # Remove capitalization
        lowerCaseText = dictionary.get(category).lower()
        # Remove numbers
        numRemoval = re.sub(r'\d+', '', lowerCaseText)
        # Remove punctuation, ie !"#$%&'()*+, -./:;<=>?@[\]^_`{|}~
        punctuationFree = "".join([word if word not in string.punctuation else " " for word in numRemoval])
        # Split words on whitespace into list for nltk stopword removal and lemmatization
        noWhiteSpace = punctuationFree.split()
        # Removes stop words that match nltk stopword list
        stop_words = stopwords.words("english")
        filteredText = " ".join([word for word in noWhiteSpace if word not in stop_words])

        # Lemmatizes words to root according to nltk word map
        wordnet_lemmatizer = WordNetLemmatizer()
        lemmatizedText = [wordnet_lemmatizer.lemmatize(word) for word in (filteredText.split())]

        # Words in each category(key) become keys in sub-dictionary under each category with word count as value
        categoryDict = dict()
        for word in lemmatizedText:
            categoryDict[word] = categoryDict.get(word, 0) + 1

        dictionary[category] = categoryDict


"""
Stores dictionary as JSON file: categoryDictionary.JSON
"""
def saveDictionary(dictionary):
    with open("categoryDictionary.json", "w") as outfile:
        json.dump(dictionary, outfile)


if __name__ == '__main__':
    main()
