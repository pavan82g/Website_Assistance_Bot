import goslate
import json

gs = goslate.Goslate()

file_path = r"./static/data/language.json"
f = open(file_path,) 
language_data = json.load(f) 

file_path = r"./static/data/bot_text.json"
f = open(file_path,) 
bot_text_data = json.load(f) 
f.close()

english_data = bot_text_data['English']
english_length = len(english_data)

temp_bot_text_data = {}

for key,value in language_data.items():
    if value['language'] == "English":
        temp_bot_text_data[value['language']] = english_data
    else:
        if value['language'] not in list(bot_text_data.keys()):
            text = list(bot_text_data['English'].values())
            translate_text = gs.translate(text, value['text_code'])
            item = {}
            for i,val in enumerate(translate_text):
                item[str(i+1)] = val.encode('utf8')
            temp_bot_text_data[value['language']] = item

        elif english_length > len(bot_text_data[value['language']]):
            text = []
            for i in range(len(bot_text_data[value['language']])+1,english_length+1):
                text.append(english_data[i])
            translate_text = gs.translate(text, value['text_code'])
            item = bot_text_data[value['language']]
            for i,val in enumerate(translate_text):
                item[str(len(bot_text_data[value['language']]) + i)] = val.encode('utf8')
            temp_bot_text_data[value['language']] = item

        else:
            temp_bot_text_data[value['language']] = bot_text_data[value['language']]

with open(r"./static/data/bot_text.json", 'w') as f:
    # f.write(str(temp_faq_data))
    json.dump(temp_bot_text_data, f) 