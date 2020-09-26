from spellchecker import SpellChecker 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from difflib import SequenceMatcher 

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
    print(accuracy)
    action = accuracy[0]
    return action

def run():
    while True:
        user_message = input()
        bot_message = ""

        split_data = split_action_text(user_message)
        print(split_data)
        action = getAction(split_data['remaining'])

        if action[1] < 0.45:
            print("Unable to understand")
            print("select 1 for greet")
            print("select 2 for click")
            option = int(input())
            if option == 1:
                with open(r".data/greet.txt",'a') as file:
                    file.write('\n')
                    file.write(str(split_data['remaining']))
            elif option == 2:
                with open(r".data/action1.txt",'a') as file:
                    file.write('\n')
                    file.write(str(split_data['remaining']))
            else:
                print("Invalid option")
            load_data()
            continue

        if split_data['website_word'] != "" :
            bot_message += str(action[0]) +" "+ str(split_data['website_word'])
        else:
            bot_message += str(action[0])
        
        print(bot_message)

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
    file_data = open(r".data/greet.txt").read()
    common_actions['greet'] = get_data(file_data)
    file_data = open(r".data/action1.txt").read()
    common_actions['click'] = get_data(file_data)

if __name__ == "__main__":
    # chnage the below words as required
    website_words = {"home":"0","help":"1","about":"2","settings":"3"}
    # actions the bot can perform (understand the given english)
    # to add another action a text file should be created
    common_actions = {"greet":[],"click":[]}
    load_data()
    run()