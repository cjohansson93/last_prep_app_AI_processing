"""
Batool Salloum, Christian Johansson, Inaya Alkhatib, Kevine Shima
CSI CUE: LSAT Prep App
2023
Professor Silveyra
This file turns the json from CategoryDictionary.py to dictionary, then processes the questions from the CSV file
Test.csv for ranking three words in each for most relevance to category using TF-IDF ranking. The resulting words
are then added as three columns in a new CSV file that is a combo of the previous file and these three, called
LRappData.csv
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
Main, calls json to dictionary, processing question, ranking, finding top three words and building CSV file
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


"""
Preprocesses each question in preparation for TF-IDF ranking, with attached category
@return Returns the list of preprocessed questions
"""
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
                processedList.append([lemmatizedText,row[7]])  # Plus category
    return processedList


"""
Calculates the TF-IDF for each word in the questions from the list and appends that to them
@param questionsList List of questions preprocesses
@param categoryDictionary Dictionary containing all the categories and their bag of words plus counts
@return List of processed questions with TF-IDF value attached to each word
"""
def calcTFIDF(questionsList,categoryDictionary):
    # Iterate through each question
    for questionANDcategory in questionsList:
        # Seperate out category for question
        category = questionANDcategory[1]
        wordDict = dict()
        # Fill small dictionary with words and count
        for words in questionANDcategory[0]:
            wordDict[words] = wordDict.get(words, 0) + 1
        # Removes duplicates
        questionANDcategory[0] = list(wordDict.keys())
        # Gets components of TF-IDF equation
        for word in questionANDcategory[0]:
            wordFreq = categoryDictionary[category].get(word)
            totalNumWords = sum(categoryDictionary[category].values())
            numberCategories = len(categoryDictionary)
            categoryPrevalence = 0
            for cat in categoryDictionary:
                if word in categoryDictionary[cat]:
                    categoryPrevalence += 1
            # Calculates TF-IDF for that word, then appends it to that word in the list
            tfidf = (wordFreq/totalNumWords)*math.log(numberCategories/categoryPrevalence)
            questionANDcategory[0][questionANDcategory[0].index(word)] = [word,tfidf]
    return questionsList

"""
Get the 3 words with the highest TF-IDF value for each question and puts them into a list
@param questionListTFIDF List of question words with their TF-IDF values
@return Returns the top three words for every question in one list of lists
"""
def topThreeWords(questionsListTFIDF):
    threeWords = list()
    for questionANDcategory in questionsListTFIDF:
        res = sorted(questionANDcategory[0], key=lambda x: x[1], reverse=True)[:3]
        if len(res) > 2:
            threeWords.append([res[0][0],res[1][0],res[2][0]])
        else:
            threeWords.append([res[0][0], res[1][0]])
    return threeWords

"""
Makes a new CSV file with the old CSV file plus three columns with the top three words for each row
@param topThreeWordsList List of top three words for each question
"""
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
