import sys
import time

from networkInterface import NetworkInterface
from buffers.MessageBuffer_pb2 import MessageBuffer


enum = {
    'ECHO':0,
    'PRINT':1,
    'TIME':2,
}
rev_enum = {
    0:'ECHO',
    1:'PRINT',
    2:'TIME',
}

class Client(NetworkInterface):
    def __init__(self,port = 5555):
        super(Client,self).__init__(port)


    def _process_message(self,msg):

        try:
            msg_type = rev_enum[msg.msg_type]
        except:
            raise InvalidMessageError(msg.msg_type)
        
        sys.stdout.write("Received Message at %s\n" % str(time.time()))

        if msg_type=='ECHO':
            sys.stderr.write("ERROR: Cannot process ECHO msg\n")
        elif msg_type=='PRINT':
            self._print(msg)
        elif msg_type=='TIME':
            sys.stderr.write("ERROR: Cannot process TIME msg\n")
        else:
            raise InvalidMessageError(msg.msg_type,msg_type)


    def _print(self,msg):
        sys.stdout.write(msg.data+'\n')

    
    def send_echo(self,dest,string):
        msg = MessageBuffer()
        msg.msg_type = enum['ECHO']
        msg.data = string
        
        self.send_message(dest,msg)
    
    def send_time(self,dest):
        msg = MessageBuffer()
        msg.msg_type = enum['TIME']

        self.send_message(dest,msg)

    def send_print(self,dest,string):
        msg = MessageBuffer()
        msg.msg_type = enum['PRINT']
        msg.data = string

        self.send_message(dest,msg)


