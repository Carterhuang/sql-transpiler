class TranspilerError(Exception):
    def __init__(self, msg):
        super(TranspilerError, self).__init__(msg)