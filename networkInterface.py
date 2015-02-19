import socket
import threading
from Queue import PriorityQueue
import struct
import sys
import time

from Errors.NetworkErrors import MessageLengthError
from Errors.GenericErrors import FunctionNotDefinedError
from buffers.MessageBuffer_pb2 import MessageBuffer


class NetworkInterface(object):
    def __init__(self,port = 5555):
        self.address = ('localhost',port)
    
        self.socket = socket.socket()
        self.socket.bind(self.address)
        
        
        
        self.received_messages = PriorityQueue()
        
        self.messages_to_process = PriorityQueue()

        self.receiver = threading.Thread(None,self._receiving_thread)
        self.receiver.start()
        
        self.receiver_lock = threading.Lock()
        self.stop_receiver = False


        self.processor = threading.Thread(None, self._processing_thread)
        self.processor.start()

        self.processor_lock = threading.Lock()
        self.stop_processor = False




    def _processing_thread(self):
        while(1):
            cur_message = self.messages_to_process.get()
            if not cur_message:
                print "Processing Thread Closing"
                return
            else:
                self._process_message(cur_message)


    def _receiving_thread(self):
        self.socket.listen(5)
        connection,recv_addr = self.socket.accept()
        
        
        while(1):
            try:
                #receive message length
                total_length = connection.recv(4)

                total_length = struct.unpack('>I',total_length)[0]
                message_length = total_length-4

                #receive message
                msg = connection.recv(message_length)

                #check message length
                if len(msg)!=message_length:
                    raise MessageLengthError(len(msg),message_length)

                parsed_msg = MessageBuffer()
                parsed_msg.ParseFromString(msg)

                self.messages_to_process.put(parsed_msg)
                
            
            except struct.error as e:
                self.receiver_lock.acquire()
                if self.stop_receiver:
                    self.receiver_lock.release()
                    print "Receiving Thread Closing"
                    return
                else:
                    self.receiver_lock.release()
                
                connection,recv_addr = self.socket.accept()

            self.receiver_lock.acquire()
            if self.stop_receiver:
                self.receiver_lock.release()
                print "Receiving Thread Closing"
                return
            else:
                self.receiver_lock.release()

        print "Receiving Thread Closing"


    def _process_message(self,msg):
        """
        This will raise an error. This function should be implemented
        by the inheriting class
        """
        pass

    def send_message(self,dest,msg):
        try:
            sending_socket = socket.socket()
            sending_socket.connect(dest)
            
            msg.sent_time = str(time.localtime())
            msg.from_addr = str(self.address)
            msg.to_addr = str(dest)

            raw_message = msg.SerializeToString()

            msg_length = 4+len(raw_message)
            package = struct.pack('>I',msg_length)
            sending_socket.sendall(package+raw_message)

            sending_socket.close()
        except socket.error as e:
            sys.stderr.write(str(e)+'\n')

        except:
            sys.stderr.write("ERROR")
            self.quit()

    def quit(self):
        #process last of received messages but accept no more
        self.receiver_lock.acquire()
        self.stop_receiver = True
        self.receiver_lock.release()

        socket.socket(socket.AF_INET,socket.SOCK_STREAM).connect(
                                            self.address)
        self.socket.close()



        self.messages_to_process.put(None)













