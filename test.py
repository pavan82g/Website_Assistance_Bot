# import json

# from polyglot.text import Text

# def changeLanguage(blob,dest):
# # blob = """flow start hello"""
#     try:
#         text = Text(blob+" hello")
#         # print(text)
#         words = text.transliterate("hi")
#         # print(words)
#         translate_text = ""
#         for x in words[:-1]:
#             translate_text += " "+x
#         print(translate_text)
#         return translate_text
#     except:
#         print(blob)
#         return blob
    

# file_name = r"./static/data/flow.json"
# f = open(file_name,) 
# data = json.load(f)     

# temp_data = data.copy()

# for k,v in data["INITAL"].items():
#     temp_data["INITAL"][k]["command"] = changeLanguage(blob=v["command"],dest="hi")

# for k1,v1 in data["TOTAL"].items():
#     for k2,v2 in data["TOTAL"][k1].items():
#         temp_data["TOTAL"][k1][k2]["command"] = changeLanguage(blob=v2["command"],dest="hi")

# with open(r"./static/data/FLOW/flow_Hindi.json", 'w', encoding="utf8") as f:
#     json.dump(temp_data, f, ensure_ascii=False)     

from nltk.stem import PorterStemmer

main_string = "FACIALing"
ps =PorterStemmer()
main_string = ps.stem(main_string)

print(main_string)