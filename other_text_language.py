import goslate
import json
from Utilites import changeLanguage


file_path = r"./static/data/language.json"
f = open(file_path,) 
language_data = json.load(f) 
f.close()

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
            item = {}
            for i,text in enumerate(list(bot_text_data['English'].values())):
                translate_text = changeLanguage(text, "en", value['text_code'])
                item[str(i+1)] = translate_text
            temp_bot_text_data[value['language']] = item

        elif english_length > len(bot_text_data[value['language']]):
            text = []
            for i in range(len(bot_text_data[value['language']])+1,english_length+1):
                translate_text = changeLanguage(english_data[i], "en", value['text_code'])
                temp_bot_text_data[value['language']][str(len(bot_text_data[value['language']]) + i)] = translate_text
        else:
            temp_bot_text_data[value['language']] = bot_text_data[value['language']]

with open(r"./static/data/bot_text.json", 'w', encoding="utf8") as f:
    # f.write(temp_bot_text_data)
    json.dump(temp_bot_text_data, f, ensure_ascii=False)