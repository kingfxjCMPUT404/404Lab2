#!/usr/bin/env python3
import socket, time, sys
from multiprocessing import Process

# Define global address and buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

# TO-DO: get_remote_ip() method
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gainError:
        print('Hostname could not be resolved. Exiting')
        sys.exit()

    print(f'IP address of {host} is {remote_ip}')
    return remote_ip

# TO-DO: handle_request() method
def handle_request(proxy_end, conn):
    # Send data
    send_full_data = conn.recv(BUFFER_SIZE)
    print(f'Sending received data {send_full_data} to Google')
    proxy_end.sendall(send_full_data)

    # Remember to shutdown
    proxy_end.shutdown(socket.SHUT_WR) # shutdown() is different form close()

    data = proxy_end.recv(BUFFER_SIZE)
    print(f'Sending received data {data} to client')
    # Send data back
    conn.send(data)

def main():
    # TO-DO: establish localhost, extern_host (google), port, buffer size
    extern_host = 'www.google.com'
    port = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        # TO-DO: bind, and set to listening mode
        print("Starting proxy server")
        # Allow reused addresses, bind, and set to listening mode
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(5)

        while True:
            # TO-DO: accept incoming connections from proxy_start, print information about connection
            # Connect proxy_start
            conn, addr = proxy_start.accept()
            print('Connected by', addr)

            # Establish "end" of proxy (connects to google)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                # TO-DO: get remote IP of google, connect proxy_end to it
                print('Connecting to Google')
                remote_ip = get_remote_ip(extern_host)

                # Now for the myltiprocessing...
                proxy_end.connect((remote_ip, port))

                # TO-DO: allow for multiple connections with a Process daemon
                # make sure to set target = handle_request when creating the Process
			    # Accept connections and start a Process daemon for handling multiple connections
                p = Process(target=handle_request, args=(proxy_end, conn))
                p.daemon = True
                p.start()
                print('Started process', p)

            # TO-DO: close the connection!
            conn.close()

if __name__ == "__main__":
    main()
