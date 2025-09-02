Per questo progetto sto utilizzando l'ambiente di sviluppo in PyCharm con un virtual environment dedicato e 
integrando Ollama. Sto utilizzando Lllama 3.2 per comprendere domande in linguaggio naturale. Ho registrato la
mia chiave API di Europeana e l'ho gestita tramite file .env per mantenerla separata dal codice.
Ho realizzato uno script in Python che permette di interrogare Europeana in maniera dinamica, l'utente può
scrivere il nome di un artista o di una persone e ottenere come risposta una lista di risultati che contengono
titolo, anno, descrizione e link diretto alla fonte. Al momento ho due moduli principali: uno che si occupa
di interpretare la domanda dell'utente con Ollama ed estrarre il soggetto, e uno che interroga Europeana e 
restituisce le informazioni. 


Esempio di funzionamento:

<img width="1917" height="1017" alt="Esempio" src="https://github.com/user-attachments/assets/5320b2c0-c2f0-41eb-84c7-40b4678f28de" />
