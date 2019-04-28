from gensim.models import Word2Vec
import pymongo
from nltk.corpus import stopwords 
import string
stop_words = set(stopwords.words('english') + list(string.punctuation))

myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["iiitmkOne"]
table7 = mydb["dbBlob"] #blob noun phrases
table8 = mydb["clusterLabel"]

model_F = Word2Vec.load("FastTextCount1.model")
vocab_F = model_F[model_F.wv.vocab]
X = model_F[model_F.wv.vocab]
l = list(model_F.wv.vocab)

wordindex = []
label = []
for x in table8.find():
    wordindex.append(x["wordInd"])
    label.append(x["labels"])


def sort(docList):
        templist = docList
        for y in range(0,1000):
                flag2 = 0
                for x in range(1,len(templist)):
                        if templist[x][1] > templist[x-1][1]:
                                temp = templist[x]
                                templist[x] = templist[x-1]
                                templist[x-1] = temp
                                flag2 = 1
                if flag2 == 0:
                        break
        lastList=[]
        for x in templist:
            if x not in lastList:
                if x[1] >1:
                    lastList.append(x)
        return lastList



print("Enter to search : \n")
w = input()
if w in l:
    word_ind_of_w = l.index(w)
    cluster_label_w = label[word_ind_of_w]

    word_list = []
    for x in range(0,len(l)):
        if label[x] == cluster_label_w:
            if l[x] not in word_list:
                word_list.append(l[x])
    docList = []
    for x in table7.find():
        for y in range(0,len(x["pages"]["urls"])):
                docSub = []
                count = 0
                for z in word_list:
                    if z in x["pages"]["phrases"][y]:
                        count+=1
                docSub.append(x["pages"]["urls"][y])
                docSub.append(count)
                docList.append(docSub)
    print("** IF - part **")
    print("Document Length :",end=" ")
    print(len(docList))
    rankedDoc = sort(docList)
    for x in rankedDoc:
        print(x)
        print("\n") 
else:
    w_split = w.split(" ")
    w_split_in_l =[]
    for x in w_split:
        if x in l:
            w_split_in_l.append(x)
    search_word = ""
    for x in w_split:
        if x not in stop_words:
            search_word+=x
            search_word+=" "
    if search_word in l:
        word_ind_of_w = l.index(w)
        cluster_label_w = label[word_ind_of_w]

        word_list = []
        for x in range(0,len(l)):
            if label[x] == cluster_label_w:
                if l[x] not in word_list:
                    word_list.append(l[x])
        docList = []
        for x in table7.find():
            for y in range(0,len(x["pages"]["urls"])):
                    docSub = []
                    count = 0
                    for z in word_list:
                        if z in x["pages"]["phrases"][y]:
                            count+=1
                    docSub.append(x["pages"]["urls"][y])
                    docSub.append(count)
                    docList.append(docSub)
        print(search_word)
        print("** IF2 - part **")
        print("Document Length :",end=" ")
        print(len(docList))
        rankedDoc = sort(docList)
        for x in rankedDoc:
            print(x)
            print("\n") 
  
    elif len(w_split_in_l)!=0 : 
        new_w = []
        for x in w_split:
            if x not in stop_words:
                new_w.append(x)
        allPhrases = []
        for x in new_w:
            if x in l:
                word_ind_of_w = l.index(x)
                cluster_label_w = label[word_ind_of_w]
                for x in range(0,len(l)):
                    if label[x] == cluster_label_w:
                        if l[x] not in allPhrases:
                            allPhrases.append(l[x])       
        docList = []
        for x in table7.find():
            for y in range(0,len(x["pages"]["urls"])):
                    docSub = []
                    count = 0
                    for z in allPhrases:
                        if z in x["pages"]["phrases"][y]:
                            count+=1
                    docSub.append(x["pages"]["urls"][y])
                    docSub.append(count)
                    docList.append(docSub)
        print(search_word)
        print("** elIF1 - part **")
        print("Document Length :",end=" ")
        print(len(docList))
        rankedDoc = sort(docList)
        for x in rankedDoc:
            print(x)
            print("\n")

    else :
        similarList = model_F.wv.most_similar(search_word)
        similarPhrases = []
        for x in similarList:
            similarPhrases.append(x[0])
        docList = []
        for x in table7.find():
            for y in range(0,len(x["pages"]["urls"])):
                    docSub = []
                    count = 0
                    for z in similarPhrases:
                        if z in x["pages"]["phrases"][y]:
                            count+=1
                    docSub.append(x["pages"]["urls"][y])
                    docSub.append(count)
                    docList.append(docSub)   
        print(len(docList))
        rankedDoc = sort(docList)
        for x in rankedDoc:
            print(x)
            print("\n")
R =[]




for y in rankedDoc:
    for x in table7.find():
        for z in range(0,len(x["pages"]["urls"])):
            sub = []
            if y[0] == x["pages"]["urls"][z]:
                ss = x["pages"]["datas"][z]
                cc = x["pages"]["datac"][z]
                sss = ""
                if len(cc)<25:
                    lll = len(cc)
                    for i in range(0,lll):
                        sss+=cc[i]
                else:
                    for i in range(0,25):
                        sss+=cc[i]
                sub.append(sss)
                sub.append(y[0])
                ttt =""
                if len(ss)<100:
                    lll = len(ss)
                    for i in range(0,lll):
                        ttt+=ss[i]
                else:
                    for i in range(0,100):
                        ttt+=ss[i]
                sub.append(ttt)
                R.append(sub)
dictList = []
for x in R:
    dic ={"title":x[0],"url":x[1],"text":x[2]}
    dictList.append(dic)
print(dictList[0])