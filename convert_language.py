import json
# from translate import Translator

from googletrans import Translator
translator = Translator()

file_path = r"./static/data/language.json"
f = open(file_path,) 
language_data = json.load(f) 

file_path = r"./static/data/faq.json"
f = open(file_path,) 
faq_data = json.load(f) 

for key,value in language_data.items():
    temp_faq_data = []
    for faq in faq_data:
        item = {}
        item["Question"] = changeLanguage(faq['Question'],src="en", dest=value['text_code'])
        item["Answer"] = changeLanguage(faq['Answer'],src="en", dest=value['text_code'])

        # translator = Translator(to_lang=value['text_code'])
        # item["Question"] = translator.translate(faq['Question'])
        # item["Answer"] = translator.translate(faq['Answer'])
        temp_faq_data.append(item)
        print(item)

    # with open(r"./static/data/FAQ/faq_"+str(value["language"])+".json", 'w', encoding="utf8") as f:
    #     # f.write(str(temp_faq_data))
    #     json.dump(temp_faq_data, f, ensure_ascii=False) 

    # result = translator.translate(contents, dest=value['text_code']).text
    # print(result.text)


