# from googletrans import Translator
# translator = Translator(service_urls=[
#       'translate.google.com',
#       'translate.google.co.kr',
#     ])

# def changeLanguage(message,src,dest):
#     translation = translator.translate(message,src=src,dest=dest)
#     return translation.text


# try:
#     temp = changeLanguage("navigate to flow start","en","hi")
# except:
#     while True:
#         try:
#             temp = changeLanguage("navigate to flow start","en","hi")
#             break
#         except:
#             continue

# with open(r"./static/data/test.txt", 'w', encoding="utf-8") as f:
#     f.write(str(temp))


import speech_recognition as sr
r = sr.Recognizer()

hellow=sr.AudioFile(r"static\voice\myaudio.webm")
with hellow as source:
    audio = r.record(source)
try:
    s = r.recognize_google(audio)
    print("Text: "+s)
except Exception as e:
    print("Exception: "+str(e))