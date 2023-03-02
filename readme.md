# Load Balancer

Implementação de um balanceador de carga para 3 servidores (1 TCP e 2 UDP) utilizando round robin para controle dos servidores UDP

## Arquivos
- client.py
- server.py
- load_balancer.py
- config.py : configuração de portas para os servidores e o balanceador de carga
- start_servers_lb.bat : inicializa os 3 servidores assim como o balanceador de carga
- client_test.py : executa client.py 3 vezes, enviando uma mensagem por TCP e duas por UDP

### Execução
- python client.py TCP : para conexão TCP 
- python client.py UDP : para conexão UDP 
- python server.py TCP : para iniciar servidor TCP 
- python server.py UDP : para iniciar servidor UDP
- python load_balancer.py

Os servidores irão executar uma função de sleep para simular a execução de um algoritmo real. O tempo de espera pode ser definido pelo segundo argumento na execução do client. Esse parametro é opcional, o valor padrão é de 5 segundos.
Ex:
    python client.py TCP 10 > irá se conectar com o servidor TCP e executará um sleep de 10 segundos

O arquivo de config.py já vem com portas pré-configuradas, dependendo da disponibilidade dessas portas talvez seja necessário alterá-las.

Os arquivos .bat para execução no windows podem não funcionar caso o python não esteja configurado corretamente no PATH. Se o seu python for executado com um nome diferente como "py" ou "python3", basta fazer a alteração nos arquivos.