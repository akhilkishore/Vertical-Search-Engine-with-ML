from gensim.models import Word2Vec
from gensim.models import FastText
import pymongo
from textblob import TextBlob
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
#import gensim
import string
stop_words = set(stopwords.words('english') + list(string.punctuation))


myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["iiitmkOne"]
table7 = mydb["dbBlob"] #blob noun phrases

finalBagOfWords = []

for x in table7.find():
    for y in x["pages"]["phrases"]:
        finalBagOfWords.append(y)
count = 0
for x in finalBagOfWords:
    for y in finalBagOfWords:
        count+=1
print(count)

#model = Word2Vec(finalBagOfWords, size=150, window=10, min_count=1, workers=10)
#model.train(finalBagOfWords, total_examples=len(finalBagOfWords), epochs=10)

#print(len(model.wv.vocab))

#print(model.wv.most_similar("beach"))

#model = FastText(finalBagOfWords, size=100, window=5, min_count=5, workers=4,sg=1) #giveing top words in the vocab
#model = FastText(finalBagOfWords, size=100, window=5, min_count=1, workers=4,sg=1) 

model_F = Word2Vec.load("FastTextCount1.model")
X = model_F[model_F.wv.vocab]
print(len(X))

#model.save("FastTextCount1.model")
#model.save("Word2VecCount1.model")
w = "backwater in alapuzha . where to find paragliding "
#w = word_tokenize(w)

print(model_F.wv.most_similar(w))