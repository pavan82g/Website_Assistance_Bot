import json

from Utilites import changeLanguage


def changeFAQ():
    file_path = r"./static/data/faq.json"
    with open(file_path, encoding="utf8") as f:
        faq_data = json.load(f) 

    for key,value in language_data.items():
        temp_faq_data = []
        for faq in faq_data:
            item = {}
            item["Question"] = changeLanguage(faq['Question'],src="en", dest=value['text_code'])
            item["Answer"] = changeLanguage(faq['Answer'],src="en", dest=value['text_code'])
            temp_faq_data.append(item)
            print(item)

        # Uncomment below lines if you want to replace the data
        with open(r"./static/data/FAQ/faq_"+str(value["language"])+".json", 'w', encoding="utf8") as f:
            json.dump(temp_faq_data, f, ensure_ascii=False) 
    print("FAQ has been translated")

def changeBotText():
    file_path = r"./static/data/bot_text.json"
    with open(file_path, encoding="utf8") as f:
        bot_text_data = json.load(f) 

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
        json.dump(temp_bot_text_data, f, ensure_ascii=False)

    print("Bot text has been translated")


if __name__ == "__main__":
    file_path = r"./static/data/language.json"
    language_data = {}
    with open(file_path,) as f: 
        language_data = json.load(f) 

    changeFAQ()
    changeBotText()



    





