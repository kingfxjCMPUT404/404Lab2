#!/usr/bin/env python3
import socket
from multiprocessing import Pool

# Define Address, buffer size
HOST = "localhost"
PORT = 8001
BUFFER_SIE = 1024

payload = "GET / HTTP/1.0\r\nHost: www.google.com\n\n\n"

def connect(addr):
    # Create socker, connect, and receive data
    try:
        # Create socket, connect, send & receiver, then shutdown
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(addr)
        s.sendall(payload.encode())
        s.shutdown(socket.SHUT_WR)

        full_data = s.recv(BUFFER_SIE)
        print(full_data)

    except Exception as e:
        print(e)
    finally:
        # Remember to close!!
        s.close()

def main():
    address = [(HOST, PORT)]
    # Establish 10 different connections
    with Pool() as p:
        p.map(connect, address * 5)

if __name__ == "__main__":
    main()
