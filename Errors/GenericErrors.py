
class FunctionNotDefinedError(Exception):
    def __init__(self,function_name,class_name):
        self.message = "%s not defined in the %s database class" % (
                    function_name,class_name)

    def __str__(self):
        return self.message
