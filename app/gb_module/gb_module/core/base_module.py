class BaseModule:

    def __init__(self):
        self.secrets = []
        self.parameters = []
        self.log = BaseModule.default_log

    @staticmethod
    def default_log(message):
        print(message)
