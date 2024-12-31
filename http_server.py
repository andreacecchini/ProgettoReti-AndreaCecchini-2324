#!/usr/bin/env python3
"""
Questo script implementa un semplice server HTTP multi-threading utilizzando le librerie standard di Python.

Classi:
    - MIMEType: Classe per determinare il tipo MIME di un file in base alla sua estensione.
    - FilePath: Classe per ottenere il percorso completo di un file dato il percorso relativo.
    - SimpleHTTPRequestHandler: Classe per gestire le richieste HTTP GET.
    - MultiThreadedHTTPServer: Classe che estende ThreadingTCPServer per gestire richieste simultanee.

Funzioni:
    - start(server_class, handler_class, host, port): Funzione per avviare il server HTTP.

Esecuzione:
    - Se eseguito come script principale, il server HTTP viene avviato con i parametri specificati da riga di comando.
    - È possibile specificare l'indirizzo host e la porta tramite gli argomenti '--host' e '--port'.
    - Il server può essere interrotto con un segnale SIGINT(Ctrl+C), che chiama la funzione signal_handler per chiudere il server in modo pulito.
"""
import datetime
from email.utils import formatdate
from urllib.parse import unquote, urlparse
from socketserver import ThreadingTCPServer
from http.server import BaseHTTPRequestHandler
import signal
import os
import argparse


class MIMEType:
    MIME_TYPES = {
        '.html': 'text/html',
        '.css': 'text/css',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg'
    }

    @classmethod
    def guess_type(cls, path):
        """
        Indovina il tipo MIME di un file in base alla sua estensione.
        Args:
            path(str): Il percorso del file di cui si vuole determinare il tipo MIME.
        Returns:
            str: Il tipo MIME corrispondente all'estensione del file. Se l'estensione
            non è riconosciuta, viene restituito 'application/octet-stream'.
        """
        ext = os.path.splitext(path)[1]
        return cls.MIME_TYPES.get(ext, 'application/octet-stream')


class FilePath:
    BASE_DIR = os.path.join(os.getcwd(), 'static')

    @classmethod
    def get_full_path(cls, path):
        """
        Restituisce il percorso completo di un file dato il percorso relativo.
        Args:
            path(str): Il percorso relativo del file richiesto.
        Returns:
            str: Il percorso completo del file all'interno della directory base del server.
        Note:
            Se il percorso richiesto è '/', viene sostituito con '/index.html'.
        """
        if path == '/':
            path = '/index.html'
        return os.path.join(cls.BASE_DIR, path.lstrip('/'))


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def set_headers(self, file_path):
        # Imposto il corretto valore per l'intestazione Content-Type
        self.send_header('Content-Type', MIMEType.guess_type(file_path))
        # Imposto l'intestazione Content-Length
        self.send_header('Content-Length', os.path.getsize(file_path))

    def handle_request(self, method):
        try:
            # Ottengo il path della risorsa richiesta
            parsed_path = urlparse(self.path)
            path = unquote(parsed_path.path)
            file_path = FilePath.get_full_path(path)

            # Se la risorsa esiste
            if os.path.isfile(file_path):
                # Codice di stato 200 - OK
                self.send_response(200)
                self.set_headers(file_path)
                self.end_headers()
                if method == 'GET':
                    # Leggo il file e lo invio come risposta
                    with open(file_path, 'rb') as file:
                        self.wfile.write(file.read())
            else:
                # Se il file non esiste, invio un errore 404
                self.send_error(404, 'File Not Found')
        except Exception as e:
            # Gestione degli errori interni del server
            self.send_error(500, f'Internal Server Error: {e}')

    def do_GET(self):
        # Esegui la richiesta GET
        self.handle_request('GET')

    def do_HEAD(self):
        # Esegui la richiesta HEAD, restituendo solo l'intestazione
        self.handle_request('HEAD')

    def do_POST(self):
        # Metodo non consentito
        self.send_error(405, 'Method Not Allowed')

    def do_PUT(self):
        # Metodo non consentito
        self.send_error(405, 'Method Not Allowed')

    def do_DELETE(self):
        # Metodo non consentito
        self.send_error(405, 'Method Not Allowed')


# Classe che estende ThreadingTCPServer per gestire richieste simultanee
class MultiThreadedHTTPServer(ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def start(server_class=MultiThreadedHTTPServer, handler_class=SimpleHTTPRequestHandler, host='localhost', port=8000):
    global httpd
    server_address = (host, port)
    end_point = f'http://{host}:{port}'
    try:
        httpd = server_class(server_address, handler_class)
        print(f"Server funzionante su: {end_point} ...\n")
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()
    print(f'Il server sta eseguendo sul seguente indirizzo: {end_point}')
    httpd.serve_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple HTTP Server')
    parser.add_argument('--host', type=str, default='localhost',
                        help='Address of the host')
    parser.add_argument('--port', type=int, default=8080,
                        help='Port to listen on')
    args = parser.parse_args()


    def signal_handler(sig, frame):
        print('\nChiusura del server in corso...')
        httpd.server_close()
        print('Chiusura completata...')
        exit(0)


    signal.signal(signal.SIGINT, signal_handler)
    start(host=args.host, port=args.port)
