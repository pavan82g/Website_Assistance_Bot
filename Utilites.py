from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from spellchecker import SpellChecker 
import time

# function to read text file and give list as output 
# where each item in list is line in text file
def get_text_data(file_path):
    data = []
    file_data = open(file_path).read()
    for line in file_data.split("\n"):
        data.append(line)
    return data 

# To measure the similarity between  
# two sentences using cosine similarity.
def similarity(X,Y):
    X = X.lower()
    Y = Y.lower()
    # tokenization 
    X_list = word_tokenize(X)  
    Y_list = word_tokenize(Y) 
    
    # sw contains the list of stopwords 
    sw = stopwords.words('english')  
    l1 =[];l2 =[] 
    
    # remove stop words from the string 
    X_set = {w for w in X_list if not w in sw}  
    Y_set = {w for w in Y_list if not w in sw} 
    
    # form a set containing keywords of both strings  
    rvector = X_set.union(Y_set) 
    
    for w in rvector: 
        if w in X_set: l1.append(1) # create a vector 
        else: l1.append(0) 
        if w in Y_set: l2.append(1) 
        else: l2.append(0) 
    c = 0
    
    # cosine formula  
    for i in range(len(rvector)): 
            c+= l1[i]*l2[i] 
    if sum(l1) < 1 or sum(l2) < 1:
        return 0.0
    cosine = c / float((sum(l1)*sum(l2))**0.5) 
    # print("similarity: ", cosine) 
    return cosine


# Function for checking spelling mistake in the given text 
def checkSpellings(text):
    spell = SpellChecker() 
    spell.word_frequency.load_text_file('./static/data/words.txt')
    new_text = ""

    for word in text.split():
        new_text += spell.correction(word)
        new_text += " "

    return new_text



# Functions for language translations
from googletrans import Translator
translator = Translator(service_urls=[
      'translate.google.com',
      'translate.google.co.kr',
    ])
def changeLanguage(message,src,dest):
    while True:
        try:
            translation = translator.translate(message,src=src,dest=dest)
            return translation.text
        except:
            time.sleep(2)
            print("Exception")
            continue
        

# from translate import Translator
# def changeLanguage(message,src,dest):
#     # print("message",message)
#     # print("Source",src)
#     # print("Destionation",dest)
#     translator = Translator(to_lang=dest,from_lang=src)
#     translation = translator.translate(message)
#     return str(translation)


# from textblob import TextBlob
# def changeLanguage(message,src,dest):
#     while True:
#         try:
#             text_blob = TextBlob(message)
#             translation = text_blob.translate(to=dest)
#             return translation
#         except:
#             time.sleep(2)
#             print("Exception")
#             continue