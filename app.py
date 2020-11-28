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
# from googletrans import Translator
from translate import Translator

from Utilites import get_text_data,similarity,checkSpellings,changeLanguage

app=Flask(__name__)
cors = CORS(app)
# translator = Translator(service_urls=[
#       'translate.google.com',
#       'translate.google.co.kr',
#     ])


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
        position = main_string.lower().find(word["command"].lower())
        if position != -1:
            remaining_text = main_string[0:position] + main_string[position+len(word["command"]):]
            result['website_word'] = str(id)
            result['remaining'] = remaining_text
            return result
    result['website_word'] = None
    result['remaining'] = main_string
    return result


def getAction(message):
    accuracy = {}
    for k,v in common_actions.items():
        # print("k,v",k,v)
        local_accuracy = []
        for line in v:
            # print("message",message)
            # print("line",line)
            # print("similarity",similarity("take me to ",line))
            local_accuracy.append(similarity(message,line))
        # print("local accuracy",local_accuracy)
        accuracy[k] = max(local_accuracy)
    accuracy = sorted(accuracy.items(), key=lambda x: x[1], reverse=True)
    # print("final dictonary",accuracy)
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
        score = similarity(v["command"],word)
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

        file_path = r"./static/data/language.json"
        f = open(file_path,) 
        language_data = json.load(f) 
    
        # Convert any language to english and then process
        # translation = translator.translate(user_message)
        # user_message = translation.text
        user_message = changeLanguage(user_message,language_data[language]['text_code'],"en")

        print(user_message,language)

        split_data = split_action_text(user_message,current_position)
        print("split data",split_data)
        
        # Removing empty space in the text
        # split_data['remaining'] = re.sub(r'[^\w]', '', split_data['remaining'])
        
        if split_data['remaining'].replace(' ','') == "":
            action = ('click',0.7)
            # If got some website word but no action word
            if split_data['website_word'] is not None:
                data = {
                    "action":str(action[0]),
                    "action_name":str(split_data['website_word'])
                }
                return data
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
            text = "Unable to understand"
            text = changeLanguage(text,"en",language_data[language]['text_code'])
            data = {
                "action":text,
                "action_name":suggestion
            }
            return data
        
        data = {
                "action":str(action[0]),
                "action_name":str(split_data['website_word'])
            }
        
        return data


@app.route('/bot_voice',methods=['GET','POST'])
def bot_voice():
    if request.method=='POST':
        user_message = request.files['user_message']
        current_position = request.form['current_position']
        language = request.form['language']

        # Saving the voice file 
        user_message.save('./static/voice/audio.wav')
        # Convert the voice to text 
        # language is not english convert to english
        file_path = r"./static/data/language.json"
        f = open(file_path,) 
        language_data = json.load(f) 

        print("voice data",user_message)
        r = sr.Recognizer()
        try:
            # using google speech recognition
            with sr.AudioFile(r'./static/voice/audio.wav') as source:
                audio_text = r.listen(source)
    
            user_message = r.recognize_google(audio_text, language = language_data[language]['code'])
            print('Converting audio transcripts into text ...')
            print(user_message)
            # return text
        
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
            user_message = checkSpellings(user_message)
            print("after modification",user_message)
            suggestion = getSimilar(flows,user_message)
            data = {
                "action":"Unable to understand",
                "action_name":suggestion
            }
            print(suggestion)
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
        language = request.args.get('language')
        print(language)
        file_path = r"./static/data/language.json"
        f = open(file_path,) 
        language_data = json.load(f) 

        file_name = r"./static/data/FAQ/faq_"+ str(language_data[language]["language"]) +".json"
        f = open(file_name,) 
        data = json.load(f)
        # Convert into respective language
        # TODO: Need to check for some solution
        # for faq in data:
        #     faq["Question"] = changeLanguage(faq["Question"],"en",language_data[language]['text_code'])
        #     faq["Answer"] = changeLanguage(faq["Answer"],"en",language_data[language]['text_code'])
        #     print(faq["Question"])
        #     print(faq["Answer"])
        data = {
            "FAQ":data
        }
        return data


@app.route('/get_change_text',methods=['GET'])
def getChangeText():
    if request.method=='GET':
        language = request.args.get('language')
        print(language)

        file_path = r"./static/data/language.json"
        f = open(file_path,) 
        language_data = json.load(f) 

        file_name = r"./static/data/FAQ/faq_"+ str(language_data[language]["language"]) +".json"
        f = open(file_name,) 
        faq_data = json.load(f)

        file_path = r"./static/data/bot_text.json"
        f = open(file_path,) 
        bot_text_data = json.load(f) 
        bot_text_data = bot_text_data[language_data[language]["language"]]

        file_name = r"./static/data/FLOW/flow_"+ str(language_data[language]["language"]) +".json"
        f = open(file_name,) 
        flow_data = json.load(f) 

        data = {
            "FAQ":faq_data,
            "FLOWS":flow_data,
            "OTHER":bot_text_data
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