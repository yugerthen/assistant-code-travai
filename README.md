\# Assistant Code du travail (RAG)



Assistant juridique qui repond en langage naturel a des questions sur le droit du travail francais,

en citant systematiquement les articles du Code du travail sur lesquels il s'appuie.



\## Avertissement

Cet assistant ne fournit pas de conseil juridique. Consultez un avocat ou l'inspection du travail

pour votre situation personnelle.



\## Questions de reflexion (section 4)



\### Q1 - Granularite du chunking

Les articles de loi sont courts et denses, avec des renvois frequents entre eux. Indexer chaque

article separement offre une granularite fine et une traçabilite exacte (un chunk = un numero

d'article), ce qui facilite la citation precise. Regrouper par section perd en precision de citation

mais capture mieux le contexte d'articles tres courts et interdependants.

Choix retenu : indexation par article individuel, car la traçabilite (obligation de citer un numero

d'article exact) est le critere prioritaire de ce projet. Une approche hybride serait envisageable :

indexer par article, mais enrichir chaque chunk avec le titre de la section parente en metadonnee,

pour donner du contexte au LLM sans sacrifier la precision de citation.



\### Q2 - Tracabilite

Le numero d'article est stocke a la fois dans le texte embedde (implicitement via le contenu) et

explicitement dans les metadonnees de chaque chunk (champ "id"). Le prompt systeme numerote les

extraits fournis au LLM et associe chaque numero d'extrait a son numero d'article reel en

metadonnee, avec une consigne stricte : le LLM ne doit citer que les numeros d'articles presents

dans le contexte fourni, jamais en inventer. Cela limite le risque d'hallucination sur les

references legales.



\### Q3 - Fraicheur

Le systeme affiche la date de constitution du corpus (a definir dans la configuration) et rappelle,

dans chaque reponse via l'avertissement juridique, que la situation personnelle de l'utilisateur

doit etre verifiee aupres d'un professionnel, ce qui couvre implicitement le risque d'obsolescence

du texte de loi entre la date du corpus et la date de consultation.



\### Q4 - Reponses conditionnelles

Le prompt systeme est instruit de fournir une reponse generale assortie de reserves explicites

quand la reponse depend de facteurs non fournis par l'utilisateur (taille d'entreprise, convention

collective), plutot que de deviner ou d'ignorer cette dependance. Le systeme peut aussi inviter

explicitement l'utilisateur a preciser sa situation si cela change fondamentalement la reponse.



\### Q5 - La frontiere du conseil juridique

Une question factuelle (ex: "combien de jours de conges par an ?") a une reponse directement

extractible d'un article de loi. Une question d'interpretation (ex: "mon licenciement est-il

abusif ?") demande d'appliquer la loi a des faits particuliers, ce qui releve du conseil juridique

individualise. Dans ce second cas, le systeme doit exposer le cadre legal general (les criteres

que la loi definit) sans se prononcer sur le cas particulier de l'utilisateur, et orienter vers un

professionnel.

