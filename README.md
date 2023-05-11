# CSI-CUE-LSAT-Prep-App

### Contibutors
Batool Salloum, Christian Johansson, Inaya Alkhatib, Kevine Shima
CSI CUE: LSAT Prep App
2023
Professor Silveyra

### Description

The LSAT has 3 multiple choice sections:
(1) Logical Reasoning 
(2) Analytical Reasoning
(3) Reading Comprehention

  Our natural language processing model is trained on the LSAT multiple choice section for logical reasoning. The model is written in Python, a commonly used programming language favored for its intuitive syntax and diverse liberties for creating AIs. The logical reasoning section has distinct official categories and multiple unofficial subcategories. The resulting AI’s goal is to tie a connection between a question's defined category and the words in the question that are important to that category. 
  
### Purpose

  The output dataset is used within the Flutter app project LSAT Prep App. 
  https://github.com/bsalloum123/lsat_prep_app_2
  With goals to provide a useful study preparation app for prospective test takers to familiarize themselves with types of questions. The app is developed through Flutter, which will allow for multi-platform development. Usefulness is hinged on the ability for these preppers to be exposed to questions with category correlation emphasized. The app will enable users to take practice exams, flash card practice and category recognition testing. User data will be stored in a database allowing for proper login, registration, profile and settings.
  
### Process and Usage

The process involves creating a category dictionary from CSV LSAT dataset. This includes preprocessing text in standard NLP process. This includes lower case, number and punctuation removal, clearing stop words and word lemmatization. Resulting dictionary categories (keys) contain the words with counts (values) for each said category. Dictionary is saved as a categoryDictionary.JSON file. The json from CategoryDictionary.py is turned back into a dictionary, then processes the questions from the CSV file in the same fashion as before from Test.csv for ranking three words in each for most relevance to category using TF-IDF ranking. The resulting words are then added as three columns in a new CSV file that is a combo of the previous file and these three, called LRappData.csv
