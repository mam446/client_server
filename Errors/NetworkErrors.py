


class InvalidMessageError(Exception):
    def __init__(self,msg_code,msg_type=None):
        if not msg_type:
            msg_type = "None"
        self.message = "Message Code: %d \nMessageType: %s" % (
                    msg_code,msg_type)

    def __str__(self):
        return self.message


class MessageLengthError(Exception):
    def __init__(self,real_length,exp_length):
        self.message = "Expected Length: %d \nActual Length: %d" % (
                    exp_length,actual_length)

    def __str__(self):
        return self.message







