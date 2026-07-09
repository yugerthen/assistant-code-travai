# Assistant Code du travail (RAG)

Assistant juridique qui repond en langage naturel a des questions sur le droit du travail francais,
en citant systematiquement les articles du Code du travail sur lesquels il s'appuie.

## Avertissement
Cet assistant ne fournit pas de conseil juridique. Consultez un avocat ou l'inspection du travail
pour votre situation personnelle.

## Questions de reflexion (section 4)

### Q1 - Granularite du chunking
Les articles de loi sont courts et denses, avec des renvois frequents entre eux. Indexer chaque
article separement offre une granularite fine et une traçabilite exacte (un chunk = un numero
d'article), ce qui facilite la citation precise. Regrouper par section perd en precision de citation
mais capture mieux le contexte d'articles tres courts et interdependants.
Choix retenu : indexation par article individuel, car la traçabilite (obligation de citer un numero
d'article exact) est le critere prioritaire de ce projet. Une approche hybride serait envisageable :
indexer par article, mais enrichir chaque chunk avec le titre de la section parente en metadonnee,
pour donner du contexte au LLM sans sacrifier la precision de citation.

### Q2 - Tracabilite
Le numero d'article est stocke a la fois dans le texte embedde (implicitement via le contenu) et
explicitement dans les metadonnees de chaque chunk (champ "id"). Le prompt systeme numerote les
extraits fournis au LLM et associe chaque numero d'extrait a son numero d'article reel en
metadonnee, avec une consigne stricte : le LLM ne doit citer que les numeros d'articles presents
dans le contexte fourni, jamais en inventer. Cela limite le risque d'hallucination sur les
references legales.

### Q3 - Fraicheur
Le systeme affiche la date de constitution du corpus et rappelle, dans chaque reponse via
l'avertissement juridique, que la situation personnelle de l'utilisateur doit etre verifiee
aupres d'un professionnel, ce qui couvre implicitement le risque d'obsolescence du texte de loi
entre la date du corpus et la date de consultation.

### Q4 - Reponses conditionnelles
Le prompt systeme est instruit de fournir une reponse generale assortie de reserves explicites
quand la reponse depend de facteurs non fournis par l'utilisateur (taille d'entreprise, convention
collective), plutot que de deviner ou d'ignorer cette dependance.

### Q5 - La frontiere du conseil juridique
Une question factuelle a une reponse directement extractible d'un article de loi. Une question
d'interpretation demande d'appliquer la loi a des faits particuliers, ce qui releve du conseil
juridique individualise. Dans ce second cas, le systeme doit exposer le cadre legal general sans
se prononcer sur le cas particulier de l'utilisateur, et orienter vers un professionnel.

## Installation
1. Cloner le depot : git clone https://github.com/yugerthen/assistant-code-travai.git
2. Creer et activer un environnement virtuel : python -m venv venv puis .\venv\Scripts\Activate.ps1
3. Installer les dependances : pip install -r requirements.txt
4. Copier .env.example en .env et renseigner votre cle API Groq (console.groq.com)

## Usage
python main.py

Puis posez vos questions en langage naturel. Tapez quit pour sortir.

## Architecture
- data/corpus.json : corpus juridique (9 articles, 5 themes)
- vectordb.py : base vectorielle ChromaDB persistante
- rag.py : orchestration retrieval + generation avec citations
- main.py : interface CLI interactive
- config.py : constantes centralisees
- prompt_system.txt : prompt systeme externalise
- test_retrieval.py : validation du retrieval (jalon 3, score 5/5)
- check_corpus.py : controle qualite du corpus

## Corpus
5 themes couverts, option C (constitution manuelle depuis Legifrance) :
Duree du travail et heures supplementaires, Conges payes, Contrat de travail CDD,
Licenciement (preavis et motif economique), Rupture conventionnelle.
Date de constitution du corpus : 09/07/2026.

## Compte rendu

### Difficultes rencontrees
La contrainte de temps (3h au lieu des 8-12h prevues) a impose de limiter le corpus a 9 articles
sur 5 themes via constitution manuelle (option C). Le workflow Git par Pull Requests a permis de
garder un historique clair et traçable de chaque jalon.

### Decisions de conception
Chunking par article individuel plutot que par section, pour maximiser la precision de citation.
Garantie de l'avertissement juridique implementee a la fois dans le prompt systeme et dans le code.

### Avec plus de temps
Extraction automatisee via l'API Legifrance pour couvrir l'integralite des 8 themes. Implementation
du jalon 6 (score de confiance sur la similarite). Tests automatises via pytest.
