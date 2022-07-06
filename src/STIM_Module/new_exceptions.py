class NullGameException(Exception):
    def __str__(self):
        return "No game data returned"


class InvalidParamException(Exception):
    def __init__(self, param_name):
        self.param_name = param_name

    def __str__(self):
        return f'Invalid parameter: {self.param_name}'
