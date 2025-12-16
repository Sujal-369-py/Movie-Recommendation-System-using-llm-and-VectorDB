import json
import gzip
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from os import getenv
import time

# ================= LOAD ENV =================
load_dotenv()

# ================= EMBEDDINGS (DISABLED) =================
# Originally used sentence-transformers + cosine similarity
# Disabled due to free-tier memory limits on deployment
#
# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity
#
# _model = None
# def generate_embedding(text: str):
#     global _model
#     if _model is None:
#         _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
#     return _model.encode(text).tolist()

# ================= LOAD DATA =================
with gzip.open("movies.json.gz", "rt", encoding="utf-8") as f:
    data = json.load(f)

rows = []
for d in data:
    if d.get("title"):
        rows.append(d)

if not rows:
    raise RuntimeError("No movie data found")

# ================= SEARCH (KEYWORD SCORING) =================
# Lightweight search for production deployment
# Avoids heavy ML models at runtime

def search_movies(query):
    q_words = query.lower().split()
    scored = []

    for doc in rows:
        text = (
            (doc.get("title", "") + " " + doc.get("plot", ""))
            .lower()
        )

        score = sum(1 for w in q_words if w in text)

        if score > 0:
            scored.append((score, doc))

    scored.sort(reverse=True, key=lambda x: x[0])

    result = []
    for _, d in scored[:10]:
        poster = d.get("poster")
        if not poster or not str(poster).startswith("http"):
            poster = None

        result.append({
            "title": d["title"],
            "poster": poster
        })

    return result

# ================= LLM QUERY CLEANER =================
llm = ChatGroq(
    api_key=getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant",
    temperature=0.2
)

def refine_query(q):
    prompt = f"""
        Refine the query.
        Do not add ideas.
        Do not guess.
        Output only refined text.

        Input:
        "{q}"

        Refined:
        """
    r = llm.invoke(prompt)
    return r.content.strip().strip('"').strip("'")

# ================= FASTAPI =================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= FRONTEND =================
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def index():
    return FileResponse("index.html")

# ================= API =================

@app.post("/movie-result")
def movie_result(payload: dict):
    movie_des = payload.get("movie_des")
    if not movie_des:
        raise HTTPException(status_code=400, detail="movie_des required")

    refined = refine_query(movie_des)
    time.sleep(4.5)
    return search_movies(refined)
