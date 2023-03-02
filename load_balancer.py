import socket, select, config

TCP_PORT = config.LB_TCP_PORT
UDP_PORT = config.LB_UDP_PORT
SERVER_PORTS = [config.TCP_SERVER_PORT, config.UDP_SERVER_PORTS[0], config.UDP_SERVER_PORTS[1]]

class LoadBalancer:
    def __init__(self) -> None:
        self.actual_server = 1

        # config TCP connection
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.bind((socket.gethostname(), TCP_PORT))
        self.tcp_socket.listen(5)

        print('-'*49)
        print(f'|\tListening TCP Service on port {TCP_PORT}\t|')

        # config UDP connection
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind((socket.gethostname(), UDP_PORT))

        print(f'|\tListening UDP Service on port {UDP_PORT}\t|')
        print('-'*49, end='\n\n')

        # TCP Connections
        self.sockets_list = [self.tcp_socket, self.udp_socket]
        self.connections = {}
        
    def round_robin(self) -> int:
        self.actual_server += 1
        return (self.actual_server % 2) + 1

    def TCP_Server(self, sock : socket.socket) -> None:
        print('-'*49)
        print('|\tReceived TCP connection\t\t\t|')

        client_socket, address = sock.accept()

        server_socket, port = socket.socket(socket.AF_INET, socket.SOCK_STREAM), SERVER_PORTS[0]

        try:
            server_socket.connect((socket.gethostname(), port))
            
            self.sockets_list.append(client_socket)
            self.sockets_list.append(server_socket)

            self.connections[client_socket] = server_socket
            self.connections[server_socket] = client_socket

            print(f'|\tConnection between {client_socket.getsockname()} and\t|\n|\t {server_socket.getsockname()} has been established\t\t|')
        except:
            print(f'|\tError: couldn\'t establish connection between {address[0]} and\t|\n|\t {port}\t\t|')
        print('-'*49, end='\n\n')

    def TCP_recv(self, sock : socket.socket, data : bytes) -> None:
        self.connections[sock].send(data)

    def TCP_close(self, sock : socket.socket) -> None:
        server_socket = self.connections[sock]

        self.sockets_list.remove(sock)
        self.sockets_list.remove(server_socket)

        del self.connections[sock]
        del self.connections[server_socket]

        print(f'Closed connection between {sock.getsockname()} and {server_socket.getsockname()}')

        sock.close()
        server_socket.close()

    def UDP_Server(self, client_socket : socket.socket) -> None:
        print('-'*49)
        print('|\tReceived UDP connection\t\t\t|')

        bytesAddressPair = client_socket.recvfrom(1024)

        data = bytesAddressPair[0].decode('utf-8')
        address = bytesAddressPair[1]

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        port = SERVER_PORTS[self.round_robin()]

        dataToSend = f'{{ "data" : {data}, "address": "{ address[0] }", "port": "{ address[1] }" }}'
        server_socket.sendto(dataToSend.encode('utf-8'), (socket.gethostname(), port))

        print(f'|\tMessage sent to {port}\t\t\t|')
        print('-'*49, end='\n\n')

        server_socket.close()
    
    def run(self) -> None:
        while True:
            read_list, write_list, exception_list = select.select(self.sockets_list, [], [])
            
            for sock in read_list:
                if sock == self.tcp_socket:
                    self.TCP_Server(sock)
                elif sock == self.udp_socket:
                    self.UDP_Server(sock)
                else:
                    try:
                        data = sock.recv(1024)

                        if data:
                            self.TCP_recv(sock, data)
                        else:
                            self.TCP_close(sock)
                    except:
                        self.TCP_close(sock)

def main() -> None:
    lb = LoadBalancer()
    lb.run()

if __name__ == "__main__":
    main()