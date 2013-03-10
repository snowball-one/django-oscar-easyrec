

class EasyRecException(Exception):

    def __init__(self, errors):
        self.errors = errors
        msgs = []
        if isinstance(errors, dict):
            errors = [errors,]
        for error in errors:
            msgs.append("(%s) %s" % (error["@code"], error["@message"]))
        super(EasyRecException, self).__init__(", ".join(msgs))
