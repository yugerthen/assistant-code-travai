import json
import random
from config import CORPUS_JSON_PATH

with open(CORPUS_JSON_PATH, "r", encoding="utf-8") as f:
    corpus = json.load(f)

print(f"Nombre total de documents : {len(corpus)}")
echantillon = random.sample(corpus, min(5, len(corpus)))
for doc in echantillon:
    print(f"\n[{doc['id']}] {doc['titre']} (theme: {doc['theme']})")
    print(doc['texte'])