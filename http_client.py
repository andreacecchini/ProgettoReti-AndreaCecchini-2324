#!/usr/bin/env python3
"""
Questo script implementa un semplice client HTTP utilizzando le librerie standard di Python.
"""


def send_request_to_server(server_address='localhost', server_port=8080, resource='/'):
    import socket
    # Creazione socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connessione al server
    s.connect((server_address, server_port))
    # Elaborazione richiesta HTTP
    request = f'GET {resource} HTTP/1.1\r\nHost: {server_address}:{server_port}\r\n\r\n'
    # Invio della richiesta
    s.send(request.encode())
    # Ricezione della risposta
    response = b''
    while True:
        data = s.recv(1024)
        if not data:
            break
        response += data
    # Chiusura connessione
    s.close()
    # Intestazione e contenuto della risposta
    header, body = response.split(b'\r\n\r\n', 1)
    # Se la risorsa non è stata trovata
    if b'404 File Not Found' in header:
        print('Resource Not Found')
    else:
        # Se la risorsa è un'immagine
        if b'Content-Type: image' in header:
            # Salvataggio dell'immagine
            with open('resouce.png', 'wb') as file:
                file.write(body)
                print('Image saved as resource.png')
        else:
            # Stampa della risposta
            print(response.decode())


if __name__ == '__main__':
    import argparse

    # Parsing degli argomenti da linea di comando
    parser = argparse.ArgumentParser(description='Simple HTTP Client')
    parser.add_argument('--server', type=str, default='localhost',
                        help='Address of the server')
    parser.add_argument('--server-port', type=int, default=8080,
                        help='Port where the server listens')
    parser.add_argument('--resource', type=str, default='/', help='Resource to request')
    args = parser.parse_args()
    # Invio della richiesta al server
    send_request_to_server(server_address=args.server, server_port=args.server_port, resource=args.resource)
