import config, socket, sys

TCP_PORT = config.LB_TCP_PORT
UDP_PORT = config.LB_UDP_PORT

def TCP_Connection() -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((socket.gethostname(), TCP_PORT))

    server_socket.send(bytes('Hello TCP Server', 'utf-8'))

    print(f'Message sent to {TCP_PORT}')

    server_socket.close()

def UDP_Connection() -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_socket.sendto(str.encode('Hello UDP Server'), (socket.gethostname(), UDP_PORT))

    print(f'Message sent to {UDP_PORT}')

    server_socket.close()

def main(connection):
    try:
        TCP_Connection() if connection == 'TCP' else UDP_Connection()
    except:
        print('Error couldn\'t connect to server')

if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) < 1:
        print('Insufficient arguments passed, please provide a connection type.', 'Valid args:\t [TCP, UDP]', 'Usage:\t\t python client.py TCP', '\t\t python client.py UDP', sep='\n')
        sys.exit(0)
    elif len(args) > 1:
        print('Incorrect number of arguments passed, please provide only a connection type.', 'Valid args:\t [TCP, UDP]', 'Usage:\t\t python client.py TCP', '\t\t python client.py UDP', sep='\n')
        sys.exit(0)

    connection = args[0].upper()
    if connection != 'UDP' and connection != 'TCP':
        print('Invalid connection type.', 'Valid args:\t [TCP, UDP]', 'Usage:\t\t python client.py TCP', '\t\t python client.py UDP', sep='\n')
        sys.exit(0)

    main(connection)