from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from nltk.stem import PorterStemmer

set(stopwords.words('english'))

text = """take me to icounting"""

# stop_words = set(stopwords.words('english')) 
  
# word_tokens = word_tokenize(text) 
    
# filtered_sentence = [] 
  
# for w in word_tokens: 
#     if w not in stop_words: 
#         filtered_sentence.append(w) 

# Stem_words = []
# ps =PorterStemmer()
# for w in filtered_sentence:
#     rootWord=ps.stem(w)
#     Stem_words.append(rootWord)
# # print(filtered_sentence)
# print(Stem_words)
ps =PorterStemmer()
print(ps.stem(text))