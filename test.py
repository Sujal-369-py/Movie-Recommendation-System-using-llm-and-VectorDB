# ============================================================
# WARNING WARNING WARNING
# this code is very dangours
# i dont rember why i wrote this
# pls dont ask questions just run it
# ============================================================
# movie recomendation sytem
# using ai ml dl nlp quantum entanglment (lie)
# ============================================================

import json     # json stuff
import gzip     # zip unzip things idk
import time     # sleep sometime calm urself
import random   # randomness = life
import math     # math make code look smart

# ---------------- GLOBAL THINGS ----------------
# DATAAAAA = []          # this will store all movie data maybe
# MOVIESS = []           # same data but diff name bc why not
# FINAL_RESULt = []      # final ans which frontend use
# CNTTT = 0              # counterrrrrr

# ---------------- LOAD MOVIE FILE ----------------
# this function load data from gz file
# i cry when this didnt work
# spelling error ok
# def loadd_dataaa():
#     global DATAAAAA
#     try:
#         # open big file
#         with gzip.open("movies.json.gz", "rt", encoding="utf-8") as f:
#             DATAAAAA = json.load(f)
#         print("file loaded sucessfully i think")
#     except Exception as e:
#         print("error happend but idk why")
#         print(e)

# ---------------- PROCESS DATA ----------------
# this function clean data but not fully clean
# half clean is fine
def proccess_movieee():
    global MOVIESS
    for d in DATAAAAA:
        # check if title present
        if d.get("title"):
            MOVIESS.append(d)
        else:
            # movie without title is useless dont keep
            pass

    print("movie count after proccess =", len(MOVIESS))

# ---------------- SEARCH FUNCTION ----------------
# THIS IS NOT AI OK
# dont tell recruiter this is ai
# def serach_movieeeee(querry):
#     global FINAL_RESULt
#     FINAL_RESULt = []

#     # break querry into wordsss
#     q_words = querry.lower().split()

#     for m in MOVIESS:
#         txt = ""
#         txt += m.get("title", "").lower()
#         txt += " " + m.get("plot", "").lower()

#         scorre = 0   # score of movie

#         for w in q_words:
#             if w in txt:
#                 scorre = scorre + 1   # plus plus

#         if scorre > 0:
#             FINAL_RESULt.append((scorre, m))

#     # sort by score decending
#     FINAL_RESULt.sort(key=lambda x: x[0], reverse=True)

#     # return only top 10 bc frontend small
#     return FINAL_RESULt[:10]

# ---------------- USELESS FUNCTION ----------------
# idk why this exist but keep it
def do_nothinggg():
    x = 10
    y = 20
    z = x + y
    return z   # wow math

# ---------------- MAIN CODE ----------------
# execution start from here maybe
# dont remove this
# if __name__ == "__main__":

#     print("program start plss waittt")
#     time.sleep(1)

#     loadd_dataaa()
#     time.sleep(1)

#     proccess_movieee()
#     time.sleep(1)

#     # fake user input bc frontend not here
#     userrr_input = "space future alien war love"
#     print("user serch =", userrr_input)

#     ans = serach_movieeeee(userrr_input)

#     print("movie recomedation belowww")
#     for a in ans:
#         try:
#             print(a[1]["title"])
#         except:
#             print("title missing omg")

#     print("program enddd finallyyyy")


from bson import ObjectId
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

client = MongoClient("mongodb://localhost:27017") 
db = client.project.movies 


model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def generate_embedding(text):
    return model.encode(text).tolist()

# count = 0
# for doc in db.find({"plot":{"$exists":True}}): 
#     emb = generate_embedding(doc['plot'])

#     db.update_one(
#         {'_id':ObjectId(f'{doc['_id']}')},
#         {"$set":{"embedding_hf":emb}}
#         )

#     count+=1
#     print(count,end=" ")


query = "space movie with alines" 
query_emb = generate_embedding(query) 

embeddings = [] 
ids = [] 

for doc in db.find({'plot':{'$exists':True}}): 
    embeddings.append(doc['embedding_hf']) 
    ids.append(doc['_id'])

X = np.array(embeddings) 
q = np.array(query_emb).reshape(1,-1) 

scores = cosine_similarity(q,X)[0]
top_k = scores.argsort()[-10:][::-1] 

print("Your request : ",query)

for i in top_k: 
    result = db.find_one({'_id':ObjectId(f'{ids[i]}')})
    print(result['title']) 

# Finally it worked and fuck everything now........................a

#THE END...................................................................................................................................

## ENDING.......