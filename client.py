import config, socket, sys

TCP_PORT = config.LB_TCP_PORT
UDP_PORT = config.LB_UDP_PORT

def TCP_Connection(time : int) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((socket.gethostname(), TCP_PORT))

    sock.send(bytes(f'{{"time" : {time}}}', 'utf-8'))

    print(f'Message sent to {TCP_PORT}')

    message = sock.recv(1024).decode('utf-8')
    print(f'Message from: {(socket.gethostname(), TCP_PORT)}', f'Message: {message}', sep='\n')

    sock.close()

def UDP_Connection(time : int) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.sendto(str.encode(f'{{"time" : {time}}}'), (socket.gethostname(), UDP_PORT))

    print(f'Message sent to {UDP_PORT}')

    bytesAddressPair = sock.recvfrom(1024)

    message = bytesAddressPair[0].decode('utf-8')
    address = bytesAddressPair[1]

    print(f'Message from: {address}', f'Message: {message}', sep='\n')

    sock.close()

def main(connection, time):
    try:
        TCP_Connection(time) if connection == 'TCP' else UDP_Connection(time)
    except:
        print('Error couldn\'t connect to server')

if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) < 1:
        print('Insufficient arguments passed, please provide a connection type.', 'Valid args:\t [TCP, UDP]', 'Usage:\t\t python client.py TCP', '\t\t python client.py UDP', sep='\n')
        sys.exit(0)
    elif len(args) > 2:
        print('Incorrect number of arguments passed, please a connection type and the sleep time if want.', 'Valid args:\t [TCP, UDP]', 'Usage:\t\t python client.py TCP', '\t\t python client.py UDP', '\t\t python client.py UDP 10', sep='\n')
        sys.exit(0)

    connection = args[0].upper()
    if connection != 'UDP' and connection != 'TCP':
        print('Invalid connection type.', 'Valid args:\t [TCP, UDP]', 'Usage:\t\t python client.py TCP', '\t\t python client.py UDP', sep='\n')
        sys.exit(0)
    
    try:
        if len(args) < 2:
            time = 5
        else:
            time = int(args[1])
    except:
        print('Invalid argument. Please provide a integer for the sleep time.')
        sys.exit(0)

    main(connection, time)