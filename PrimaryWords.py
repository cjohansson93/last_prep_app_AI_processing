"""
Batool Salloum, Christian Johansson, Inaya Alkhatib, Kevine Shima
CSI CUE: LSAT Prep App
2023
Professor Silveyra
This file
"""

import csv
import json
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import math


"""
Main
"""
def main():
    categoryDictionary = jsonToDict()
    questionsList = processQuestions()
    questionsListTFIDF = calcTFIDF(questionsList,categoryDictionary)
    topThreeWordsList = topThreeWords(questionsListTFIDF)
    csvBuilder(topThreeWordsList)


def jsonToDict():
    with open("categoryDictionary.json") as jsonFile:
        dictionary = json.load(jsonFile)
    return dictionary


def processQuestions():
    processedList = list()
    with open('Analytical Reasoning/reclor_data/test.csv') as csvFile:
        reader = csv.reader(csvFile)
        headers = True
        for row in reader:
            # Doesn't store the fieldnames
            if headers:
                headers = False
            else:
                # Remove capitalization
                lowerCaseText = row[1].lower()
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
                processedList.append([lemmatizedText,row[7]])
    return processedList


def calcTFIDF(questionsList,categoryDictionary):
    for questionANDcategory in questionsList:
        category = questionANDcategory[1]
        wordDict = dict()
        for words in questionANDcategory[0]:
            wordDict[words] = wordDict.get(words, 0) + 1
        questionANDcategory[0] = list(wordDict.keys())
        for word in questionANDcategory[0]:
            wordFreq = categoryDictionary[category].get(word)
            totalNumWords = sum(categoryDictionary[category].values())
            numberCategories = len(categoryDictionary)
            categoryPrevalence = 0
            for cat in categoryDictionary:
                if word in categoryDictionary[cat]:
                    categoryPrevalence += 1
            tfidf = (wordFreq/totalNumWords)*math.log(numberCategories/categoryPrevalence)
            questionANDcategory[0][questionANDcategory[0].index(word)] = [word,tfidf]
    return questionsList


def topThreeWords(questionsListTFIDF):
    threeWords = list()
    for questionANDcategory in questionsListTFIDF:
        res = sorted(questionANDcategory[0], key=lambda x: x[1], reverse=True)[:3]
        if len(res) > 2:
            threeWords.append([res[0][0],res[1][0],res[2][0]])
        else:
            threeWords.append([res[0][0], res[1][0]])
    return threeWords


def csvBuilder(topThreeWordsList):
    topThreeWordsList.insert(0,["word_one", "word_two", "word_three"])
    with open('LRappData.csv', 'w', newline='') as csvfileWriter:
        writer = csv.writer(csvfileWriter)
        with open('Analytical Reasoning/reclor_data/test.csv') as csvFileReader:
            reader = csv.reader(csvFileReader)
            for i in range(len(topThreeWordsList)):
                writer.writerow(reader.__next__()+topThreeWordsList[i])


if __name__ == '__main__':
    main()
