# Server Web Semplice

Questo progetto implementa un semplice server web in Python capace di servire file statici come HTML, CSS e immagini. Il
server gestisce richieste HTTP GET di base e può gestire più richieste simultanee.

## Struttura del Progetto

```
simple-web-server
├── src
│   ├── http_server.py       # Implementazione del semplice server web
│   └── static
│       ├── index.html       # Homepage del server web
│       ├── styles.css       # Stili CSS per il documento HTML
│       └── image.jpg        # Un file immagine servito dal server web
└── README.md                # Documentazione del progetto
```

## Per Iniziare

Per eseguire il server, segui questi passaggi:

1. **Clona il repository**:
   ```
   git clone <repository-url>
   cd simple-web-server
   ```

2. **Esegui il server**:
   Esegui il seguente comando per avviare il server:
   ```
   python http_server.py --host=localhost --port=8080
   ```

3. **Prova il server**:
   Apri il tuo browser web e naviga a `http://localhost:8080` per visualizzare la homepage.

## Funzionalità

- Il server serve file statici dalla directory `src/static`.
- Può gestire più richieste simultanee.
- Supporta la fornitura di file HTML, CSS e immagini.
