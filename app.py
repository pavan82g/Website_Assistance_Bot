from spellchecker import SpellChecker 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from difflib import SequenceMatcher 
from flask import Flask, request
from flask_cors import CORS, cross_origin
import json
import re
from werkzeug.utils import secure_filename
import os
import speech_recognition as sr

from Utilites import get_text_data,similarity,checkSpellings

app=Flask(__name__)
cors = CORS(app)


def get_current_flows(current_position):
    if current_position == "0" or current_position == "":
        return inital_flows
    else:
        if current_position in remaining_flows.keys():
            return remaining_flows[current_position]
    return None

def split_action_text(main_string,current_position):
    result = {"website_word":"","remaining":""}
    position = None
    # TODO: logic for if there are more than one website word in the main string
    website_words = get_current_flows(current_position)
    if website_words is None:
        result['website_word'] = None
        result['remaining'] = main_string
        return result
    for id,word in website_words.items():
        position = main_string.lower().find(word.lower())
        if position != -1:
            remaining_text = main_string[0:position] + main_string[position+len(word):]
            result['website_word'] = str(id)
            result['remaining'] = remaining_text
            return result
    result['website_word'] = None
    result['remaining'] = main_string
    return result


def getAction(message):
    accuracy = {}
    for k,v in common_actions.items():
        print("k,v",k,v)
        local_accuracy = []
        for line in v:
            print("message",message)
            print("line",line)
            print("similarity",similarity("take me to ",line))
            local_accuracy.append(similarity(message,line))
        print("local accuracy",local_accuracy)
        accuracy[k] = max(local_accuracy)
    accuracy = sorted(accuracy.items(), key=lambda x: x[1], reverse=True)
    print("final dictonary",accuracy)
    action = accuracy[0]
    return action


def load_action():
    greet_path = r"./static/data/greet.txt"
    common_actions['greet'] = get_text_data(greet_path)
    action_path = r"./static/data/action1.txt"
    common_actions['click'] = get_text_data(action_path)


def get_json():
    file_name = r"./static/data/flow.json"
    f = open(file_name,) 
    data = json.load(f) 
    return data


def getSimilar(flows,word):
    similar_words = []
    for k,v in flows.items():
        score = similarity(v,word)
        # print(l,word,score)
        if score > 0.25:
            similar_words.append(k)

    if len(similar_words) < 1:
        similar_words = list(flows.keys())
    return similar_words


@app.route('/getlanguage',methods=['GET'])
def getLanguage():
    if request.method == "GET":
        file_path = r"./static/data/language.json"
        f = open(file_path,) 
        data = json.load(f) 
        # print(type(data))
        return data
            

@app.route('/bot_text',methods=['GET'])
def bot_text():
    if request.method=='GET':
        user_message = request.args.get('user_message')
        current_position = request.args.get('current_position')
        language = request.args.get('language')
        # user_message = "hello there"

        # Convert any language to english and then process

        print(user_message)

        split_data = split_action_text(user_message,current_position)
        print("split data",split_data)
        
        # Removing empty space in the text
        # split_data['remaining'] = re.sub(r'[^\w]', '', split_data['remaining'])
        
        if split_data['remaining'].replace(' ','') == "":
            action = ('click',0.7)
        else:
            action = getAction(split_data['remaining'])
            print(action)

        print(action)
        print(split_data['website_word'])
        if action[1] > 0.45 and action[0] == 'greet':
            data = {
                "action":str(action[0]),
                "action_name":str(action[0])
            }
            return data

        if action[1] < 0.45 or split_data['website_word'] is None:
            print("if confition")
            flows = get_current_flows(current_position)
            suggestion = getSimilar(flows,user_message)
            data = {
                "action":"Unable to understand",
                "action_name":suggestion
            }
            return data
        
        data = {
                "action":str(action[0]),
                "action_name":str(split_data['website_word'])
            }
        
        return data


@app.route('/bot_voice',methods=['GET'])
def bot_voice():
    if request.method=='GET':
        user_message = request.args.get('user_message')
        current_position = request.args.get('current_position')
        language = request.args.get('language')

        # Convert the voice to text 
        # language is not english convert to english
        file_path = r"./static/data/language.json"
        f = open(file_path,) 
        language_data = json.load(f) 

        r = sr.Recognizer()
        try:
            # using google speech recognition
            text = r.recognize_google(user_message, language = language_data[language]['code'])
            print('Converting audio transcripts into text ...')
            print(text)
            return text
        
        except:
            print('Sorry.. run again...')
            return "error"

        # bot_message = ""
        print(user_message)

        split_data = split_action_text(user_message,current_position)
        print("split data",split_data)
        
        # Removing empty space in the text
        # split_data['remaining'] = re.sub(r'[^\w]', '', split_data['remaining'])
        
        if split_data['remaining'].replace(' ','') == "":
            action = ('click',0.7)
        else:
            action = getAction(split_data['remaining'])
            print(action)

        print(action)
        print(split_data['website_word'])
        if action[1] > 0.45 and action[0] == 'greet':
            data = {
                "action":str(action[0]),
                "action_name":str(action[0])
            }
            return data

        if action[1] < 0.45 or split_data['website_word'] is None:
            print("if confition")
            flows = get_current_flows(current_position)
            suggestion = getSimilar(flows,user_message)
            data = {
                "action":"Unable to understand",
                "action_name":suggestion
            }
            return data
        
        data = {
                "action":str(action[0]),
                "action_name":str(split_data['website_word'])
            }
        
        return data

        
@app.route('/suggestion',methods=['GET'])
def get_suggestion():
    if request.method=='GET':
        user_message = request.args.get('user_message')
        user_message = checkSpellings(user_message)
        data = {
            "suggestion":user_message
        }
        return data

@app.route('/get_faq',methods=['GET'])
def get_faq():
    if request.method=='GET':
        file_name = "./static/data/faq.json"
        f = open(file_name,) 
        data = json.load(f) 
        data = {
            "FAQ":data
        }
        return data

@app.route('/upload',methods=['POST'])
def upload():
    if request.method=='POST':
        file = request.files['document']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join("./static/database/", filename))
            print(os.path.join("./static/database/", filename))
            return "Document has been sucessfully uploaded"
        else:
            return "No file recivied"


if __name__ == '__main__':
    # # change the below words as required
    # website_words = {"home":"0","help":"1","about":"2","settings":"3"}
    flow = get_json()
    inital_flows = flow['INITAL']
    common_flows = flow['SAME']
    remaining_flows = flow['TOTAL']
    # actions the bot can perform (understand the given english)
    # to add another action a text file should be created
    common_actions = {"greet":[],"click":[]}
    load_action()
    app.run(port=8000,debug=True)