"""
Batool Salloum, Christian Johansson, Inaya Alkhatib, Kevine Shima
CSI CUE: LSAT Prep App
2023
Professor Silveyra
This file creates a category dictionary from CSV LSAT dataset. This includes preprocessing text in standard NLP process.
Resulting dictionary categories (keys) contain the words with counts (values) for each said category.
"""
import csv


def main():
    categoryDictionary = makeDictionary()
    processDictionary(categoryDictionary)
    saveDictionary(categoryDictionary)


def makeDictionary():
    dictionary = dict()
    with open('Logical Reasoning/train_lr.csv') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            print(row)

    return dictionary


def processDictionary(dictionary):
    pass


def saveDictionary(dictionary):
    pass


if __name__ == '__main__':
    main()
