import sys
import time
import client



port = int(sys.argv[1])

x = client.Client(port)

send_port = int(sys.argv[2])


while True:
    choice = raw_input()
    if choice=="echo":
        data = raw_input()
        x.send_echo(('localhost',send_port),data)
    elif choice=="time":
        x.send_time(('localhost',send_port))
    elif choice=="print":       
        data = raw_input()
        x.send_print(('localhost',send_port),data)
    elif choice=='quit':
        break
x.quit()

