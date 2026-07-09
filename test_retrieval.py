from vectordb import VectorDB

db = VectorDB()

questions_test = [
    {"question": "Quelle est la duree legale du travail par semaine ?", "article_attendu": "L3121-27"},
    {"question": "Combien de jours de conges payes par mois de travail ?", "article_attendu": "L3141-3"},
    {"question": "Dans quels cas peut-on conclure un CDD ?", "article_attendu": "L1242-2"},
    {"question": "Quelle est la duree du preavis en cas de licenciement ?", "article_attendu": "L1234-1"},
    {"question": "Comment fonctionne la rupture conventionnelle ?", "article_attendu": "L1237-11"},
]

reussites = 0
for test in questions_test:
    resultats = db.retrieve(test["question"], n=3)
    articles_trouves = [meta["article"] for meta in resultats["metadatas"][0]]
    trouve = test["article_attendu"] in articles_trouves
    reussites += trouve
    statut = "OK" if trouve else "ECHEC"
    print(f"[{statut}] {test['question']}")
    print(f"   Attendu: {test['article_attendu']} | Trouves: {articles_trouves}")

print(f"\nScore : {reussites}/{len(questions_test)}")