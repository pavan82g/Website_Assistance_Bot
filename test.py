import goslate
import json

gs = goslate.Goslate()

file_path = r"./static/data/language.json"
f = open(file_path,) 
language_data = json.load(f) 

file_path = r"./static/data/faq.json"
f = open(file_path,) 
faq_data = json.load(f) 

for key,value in language_data.items():
    temp_faq_data = []
    question_text = []
    answer_text = []
    for faq in faq_data:
        question_text.append(faq["Question"])
        answer_text.append(faq["Answer"])
        
    # print("text",text)
    question_translate = gs.translate(question_text, value['text_code'])
    answer_translate = gs.translate(answer_text, value['text_code'])
    # print("translate",translate)
    for question in question_translate:
        # print(tr)
        item = {}
        item["Question"] = gs.translate(faq['Question'], value['text_code'])
        item["Answer"] = gs.translate(faq['Answer'], value['text_code']) 

        temp_faq_data.append(item)
        # print(item)

