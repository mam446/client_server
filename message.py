from buffers.MessageBuffer_pb2 import MessageBuffer
import time

enum = {
    'ECHO':0,
    'PRINT':1,
    'TIME':2,
}


class Message(object):
    def __init__(self,data=None):
        
        self.raw_message = MessageBuffer()
        if data:
            self.raw_message.ParseFromString(data)


    def set_message(self,msg_type,msg_data):
        self.raw_message.msg_type = enum[msg_type]
        self.raw_message.data = msg_data










