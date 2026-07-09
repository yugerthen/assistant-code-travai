import os
import json
import chromadb
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL, CHROMA_DB_PATH, CORPUS_JSON_PATH

class VectorDB:
    def __init__(self, collection_name="code_travail"):
        self.client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        self.collection_name = collection_name

        existing_collections = [c.name for c in self.client.list_collections()]

        if collection_name in existing_collections:
            self.collection = self.client.get_collection(collection_name)
            model_name = self.collection.metadata["embedding_model"]
            self.model = SentenceTransformer(model_name)
            print(f"Base rechargee avec le modele : {model_name}")
        elif os.path.exists(CORPUS_JSON_PATH):
            self.model = SentenceTransformer(EMBEDDING_MODEL)
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"embedding_model": EMBEDDING_MODEL}
            )
            self._index_corpus()
            print("Base creee et indexee")
        else:
            raise RuntimeError("Aucune base existante et aucun corpus disponible pour en creer une.")

    def _index_corpus(self):
        with open(CORPUS_JSON_PATH, "r", encoding="utf-8") as f:
            corpus = json.load(f)

        ids = [doc["id"] for doc in corpus]
        texts = [doc["texte"] for doc in corpus]
        metadatas = [
            {"titre": doc["titre"], "theme": doc["theme"], "article": doc["id"]}
            for doc in corpus
        ]

        embeddings = self.model.encode(
            texts,
            batch_size=16,
            normalize_embeddings=True,
            show_progress_bar=True
        )

        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )

    def retrieve(self, question, n=3):
        question_embedding = self.model.encode([question], normalize_embeddings=True)
        results = self.collection.query(
            query_embeddings=question_embedding.tolist(),
            n_results=n
        )
        return results

if __name__ == "__main__":
    db = VectorDB()
    resultats = db.retrieve("Quelle est la duree legale du travail ?", n=3)
    for doc, meta in zip(resultats["documents"][0], resultats["metadatas"][0]):
        print(f"- [{meta['article']}] {doc}")