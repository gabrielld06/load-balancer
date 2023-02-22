:: Start Servers
start cmd.exe /k "python server.py TCP"
start cmd.exe /k "python server.py UDP"
start cmd.exe /k "python server.py UDP"

:: Start Load Balancer
start cmd.exe /k "python load_balancer.py"