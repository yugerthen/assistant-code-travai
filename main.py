from rag import RAG

def main():
    print("=== Assistant Code du travail ===")
    print("Posez vos questions sur le droit du travail francais (tapez 'quit' pour sortir)\n")

    rag = RAG()

    while True:
        question = input("Votre question : ").strip()
        if question.lower() in ("quit", "exit", "q"):
            print("Au revoir.")
            break
        if not question:
            continue

        print("\nRecherche en cours...\n")
        try:
            reponse = rag.answer_question(question)
            print(reponse)
        except Exception as e:
            print(f"Erreur : {e}")
        print("\n" + "-"*60 + "\n")

if __name__ == "__main__":
    main()