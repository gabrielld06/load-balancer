import socket, errno, sys, config, json
from time import sleep

TCP_PORT = config.TCP_SERVER_PORT
UDP_PORTS = config.UDP_SERVER_PORTS

def do_something(time : int):
    sleep(time)

class TCP_Socket():
    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.bind((socket.gethostname(), TCP_PORT))
        self.sock.listen(5)
    
    def run(self) -> None:
        print(f'TCP Server listening on port {TCP_PORT}')

        while True:
            clientsocket, address = self.sock.accept()

            print(f'Connection from {address} has been established')

            message = clientsocket.recv(1024).decode('utf-8')
            print(f'Message from: {address}', f'Message: {message}', sep='\n')

            data = json.loads(message)

            do_something(data['time'])
            
            clientsocket.send(bytes(f'TCP Server slept for {data["time"]} seconds', 'utf-8'))

            print(f'Message sent to {address}')
            
            clientsocket.close()

class UDP_Socket():
    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            self.sock.bind((socket.gethostname(), UDP_PORTS[0]))
        except:
            self.sock.bind((socket.gethostname(), UDP_PORTS[1]))
    
    def run(self) -> None:
        print(f'UDP Server listening on port {self.sock.getsockname()[1]}')

        while True:
            bytesAddressPair = self.sock.recvfrom(1024)

            message = bytesAddressPair[0].decode('utf-8')

            parsedMessage = json.loads(message)
            data = parsedMessage['data']
            address = (parsedMessage['address'], int(parsedMessage['port']))

            print(f'Message from: {address}', f'Message: {message}', sep='\n')

            do_something(data['time'])

            self.sock.sendto(str.encode(f'UDP Server slept for {data["time"]} seconds'), address)

            print(f'Message sent to {address}')

def Server(connection : str) -> TCP_Socket | UDP_Socket:
    try:
        if connection == 'TCP':
            return TCP_Socket()
        else:
            return UDP_Socket()
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            print(f'Couldn\'t bind to port {TCP_PORT}. Terminating process...')
        else:
            print(e)
        sys.exit(0)

def main(connection) -> None:
    server = Server(connection)
    server.run()

if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) < 1:
        print('Insufficient arguments passed, please provide a connection type.', 'Valid args:\t [TCP, UDP]', 'Usage:\t\t python server.py TCP', '\t\t python server.py UDP', sep='\n')
        sys.exit(0)
    elif len(args) > 1:
        print('Incorrect number of arguments passed, please provide only a connection type.', 'Valid args:\t [TCP, UDP]', 'Usage:\t\t python server.py TCP', '\t\t python server.py UDP', sep='\n')
        sys.exit(0)

    connection = args[0].upper()
    if connection != 'UDP' and connection != 'TCP':
        print('Invalid connection type.', 'Valid args:\t [TCP, UDP]', 'Usage:\t\t python server.py TCP', '\t\t python server.py UDP', sep='\n')
        sys.exit(0)

    main(connection)