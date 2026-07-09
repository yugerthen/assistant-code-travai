\## Installation

1\. Cloner le depot : git clone https://github.com/yugerthen/assistant-code-travai.git

2\. Creer et activer un environnement virtuel : python -m venv venv puis .\\venv\\Scripts\\Activate.ps1

3\. Installer les dependances : pip install -r requirements.txt

4\. Copier .env.example en .env et renseigner votre cle API Groq (console.groq.com)



\## Usage

python main.py



Puis posez vos questions en langage naturel. Tapez 'quit' pour sortir.



\## Architecture

\- data/corpus.json : corpus juridique (9 articles, 5 themes)

\- vectordb.py : base vectorielle ChromaDB persistante

\- rag.py : orchestration retrieval + generation avec citations

\- main.py : interface CLI interactive

\- config.py : constantes centralisees

\- prompt\_system.txt : prompt systeme externalise

\- test\_retrieval.py : validation du retrieval (jalon 3, score 5/5)

\- check\_corpus.py : controle qualite du corpus



\## Corpus

5 themes couverts, option C (constitution manuelle depuis Legifrance) :

Duree du travail et heures supplementaires, Conges payes, Contrat de travail CDD,

Licenciement (preavis et motif economique), Rupture conventionnelle.

Date de constitution du corpus : 09/07/2026.



\## Compte rendu



\### Difficultes rencontrees

La contrainte de temps (3h au lieu des 8-12h prevues) a impose de limiter le corpus a 9 articles

sur 5 themes via constitution manuelle (option C), plutot qu'une extraction automatisee complete

via l'API Legifrance ou le jeu de donnees LEGI (option A/B), plus longues a mettre en oeuvre.

Le workflow Git par Pull Requests, bien que plus lent qu'un merge local, a permis de garder un

historique clair et traçable de chaque jalon.



\### Decisions de conception

Chunking par article individuel plutot que par section, pour maximiser la precision de citation

(voir Q1). Garantie de l'avertissement juridique implementee a la fois dans le prompt systeme et

dans le code (verification post-generation), pour eviter le risque d'omission par le LLM evoque

dans le sujet.



\### Avec plus de temps

Extraction automatisee via l'API Legifrance ou le corpus LEGI pour couvrir l'intergralite des

8 themes avec plus d'articles par theme. Implementation du jalon 6 (amelioration) : probablement

un score de confiance affichant la similarite du meilleur chunk trouve, pour avertir l'utilisateur

si aucun resultat pertinent n'est disponible. Ajout de tests automatises (pytest) plutot que des

scripts manuels.

