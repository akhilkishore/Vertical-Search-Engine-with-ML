from gensim.models import Word2Vec
from sklearn import cluster
import matplotlib.pyplot as plt
from gensim.models import FastText
import pymongo


myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["iiitmkOne"]
table7 = mydb["dbBlob"] #blob noun phrases
table8 = mydb["clusterLabel"]


model_F = Word2Vec.load("FastTextCount1.model")
vocab_F = model_F[model_F.wv.vocab]
X = model_F[model_F.wv.vocab]

kmeans = cluster.KMeans(n_clusters=50)
kmeans.fit(vocab_F)

labels = kmeans.labels_
centroids = kmeans.cluster_centers_

l = list(model_F.wv.vocab)

print(len(l))
print(len(vocab_F))
print (len(kmeans.labels_))

def clusterLabelUpdate(a,b):
    myq = {"wordInd":a,"labels":b}
    table8.insert_one(myq)

for x in range(0,len(l)):
   clusterLabelUpdate(str(x),str(labels[x]))
plt.scatter(X[:,0], X[:,1], c=kmeans.labels_, cmap='rainbow') 
plt.show()