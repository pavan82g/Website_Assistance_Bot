from spellchecker import SpellChecker 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from difflib import SequenceMatcher 
from flask import Flask, request


app=Flask(__name__)

def get_data(file_data):
    data = []
    # file_data = open(path).read()
    for i, line in enumerate(file_data.split("\n")):
        data.append(line)
    return data 

def split_action_text(main_string):
    result = {"website_word":"","remaining":""}
    position = None
    # TODO: logic for if there are more than one website word in the main string
    for word in website_words:
        position = main_string.find(word)
        if position != -1:
            remaining_text = main_string[0:position] + main_string[position+len(word):]
            result['website_word'] = word
            result['remaining'] = remaining_text
            return result

    result['remaining'] = main_string
    return result

def checkSpellings(text):
    spell = SpellChecker() 
    new_text = ""

    for word in text.split():
        new_text += spell.correction(word)
        new_text += " "

    return new_text

def getAction(message):
    accuracy = {}
    for k,v in common_actions.items():
        local_accuracy = []
        for line in v:
            local_accuracy.append(similarity(message,line))
        accuracy[k] = max(local_accuracy)
    accuracy = sorted(accuracy.items(), key=lambda x: x[1], reverse=True)
    # print(accuracy)
    action = accuracy[0]
    return action

# def similarity(str1,str2):
#     return SequenceMatcher(None, str1, str2).ratio() 
def similarity(X,Y):
    # Program to measure the similarity between  
    # two sentences using cosine similarity. 
    
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

def load_data():
    file_data = open(r"./data/greet.txt").read()
    common_actions['greet'] = get_data(file_data)
    file_data = open(r"./data/action1.txt").read()
    common_actions['click'] = get_data(file_data)


@app.route('/bot',methods=['GET'])
def home():
    if request.method=='GET':
        user_message = request.args.get('user_message')
        # user_message = "hello there"

        bot_message = ""

        split_data = split_action_text(user_message)
        
        action = getAction(split_data['remaining'])

        if action[1] < 0.45:
            data = {
                "action":"Unable to understand",
                "action_name":list(website_words.keys())
            }
            return data

        data = {
                "action":str(action[0]),
                "action_name":str(split_data['website_word'])
            }
        
        return data
        

if __name__ == '__main__':
    # change the below words as required
    website_words = {"home":"0","help":"1","about":"2","settings":"3"}
    # actions the bot can perform (understand the given english)
    # to add another action a text file should be created
    common_actions = {"greet":[],"click":[]}
    load_data()
    app.run(port=5000,debug=True)