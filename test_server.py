import sys

import server



port = int(sys.argv[1])

x = server.Server(port)

raw_input()

x.quit()



