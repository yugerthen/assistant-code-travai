from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL
from vectordb import VectorDB

AVERTISSEMENT = "Cet assistant ne fournit pas de conseil juridique. Consultez un avocat ou l'inspection du travail pour votre situation personnelle."

class RAG:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.vectordb = VectorDB()
        with open("prompt_system.txt", "r", encoding="utf-8") as f:
            self.prompt_template = f.read()

    def _build_prompt(self, chunks):
        lignes = []
        for i, (doc, meta) in enumerate(zip(chunks["documents"][0], chunks["metadatas"][0])):
            lignes.append(f"[Extrait {i+1} - Article {meta['article']} - {meta['titre']}] {doc}")
        chunks_text = "\n\n".join(lignes)
        return self.prompt_template.replace("{{Chunks}}", chunks_text)

    def answer_question(self, question):
        chunks = self.vectordb.retrieve(question, n=4)
        system_prompt = self._build_prompt(chunks)

        try:
            response = self.client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                temperature=0.1
            )
        except Exception as e:
            raise RuntimeError(f"Erreur lors de l'appel au LLM : {e}")

        reponse = response.choices[0].message.content

        # Garantie technique : l'avertissement est toujours present, meme si le LLM l'omet
        if AVERTISSEMENT not in reponse:
            reponse = reponse.strip() + "\n\n" + AVERTISSEMENT

        return reponse

if __name__ == "__main__":
    rag = RAG()
    print(rag.answer_question("Quelle est la duree legale du preavis pour un CDI ?"))
    print("\n---\n")
    print(rag.answer_question("Quelle est la capitale du Japon ?"))