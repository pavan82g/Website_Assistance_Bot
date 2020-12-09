import json

from polyglot.text import Text

def changeLanguage(blob,dest):
# blob = """flow start hello"""
    try:
        text = Text(blob+" hello")
        # print(text)
        words = text.transliterate("hi")
        # print(words)
        translate_text = ""
        for x in words[:-1]:
            translate_text += " "+x
        print(translate_text)
        return translate_text
    except:
        print(blob)
        return blob
    

file_name = r"./static/data/flow.json"
f = open(file_name,) 
data = json.load(f)     

temp_data = data.copy()

for k,v in data["INITAL"].items():
    temp_data["INITAL"][k]["command"] = changeLanguage(blob=v["command"],dest="hi")

for k1,v1 in data["TOTAL"].items():
    for k2,v2 in data["TOTAL"][k1].items():
        temp_data["TOTAL"][k1][k2]["command"] = changeLanguage(blob=v2["command"],dest="hi")

with open(r"./static/data/FLOW/flow_Hindi.json", 'w', encoding="utf8") as f:
    json.dump(temp_data, f, ensure_ascii=False)     


# def changeFlows():
#     file_name = r"./static/data/flow.json"
#     f = open(file_name,) 
#     data = json.load(f) 

#     for key,value in language_data.items():
#         temp_data = data.copy()
#         if value['language'] == "English":
#             continue
#         else:
#             print(value['language'])
#             for k,v in data["INITAL"].items():
#                 temp_data["INITAL"][k]["command"] = changeLanguage(blob=v["command"],dest=value['text_code'])

#             for k1,v1 in data["TOTAL"].items():
#                 for k2,v2 in data["TOTAL"][k1].items():
#                     # print(v2["command"])
#                     # print(changeLanguage(v2["command"],"en",value['text_code']))
#                     temp_data["TOTAL"][k1][k2]["command"] = changeLanguage(blob=v2["command"],dest=value['text_code'])

#             with open(r"./static/data/FLOW/flow_"+str(value["language"])+".json", 'w', encoding="utf8") as f:
#                 json.dump(temp_data, f, ensure_ascii=False) 
#     print("Bot flows has been translated")


# if __name__ == "__main__":
#     file_path = r"./static/data/language.json"
#     language_data = {}
#     with open(file_path,) as f: 
#         language_data = json.load(f) 

#     changeFlows()