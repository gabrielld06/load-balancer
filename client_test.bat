:: Does one TCP connection and two UDP connections
start cmd.exe /k "python client.py TCP"
start cmd.exe /k "python client.py UDP"
start cmd.exe /k "python client.py UDP"
pause