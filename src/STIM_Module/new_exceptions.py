class NullGameException(Exception):
    def __str__(self):
        return "No game data returned"


class InvalidParamException(Exception):
    def __init__(self, param_name, message=''):
        self.param_name = param_name
        self.message = message

    def __str__(self):
        return f'Invalid parameter: {self.param_name}\n{self.message}'


class RateLimitException(Exception):
    def __init__(self, one_sec_limit_progress, two_min_limit_progress):
        self.second_limit = 20
        self.second_limit_progress = one_sec_limit_progress
        self.two_min_limit = 100
        self.two_min_limit_progress = two_min_limit_progress

    def __str__(self):
        if self.second_limit - self.second_limit_progress <= self.two_min_limit - self.two_min_limit_progress:
            return f'API calls in the past second: {self.second_limit_progress}\nSlow Down!'
        else:
            return f'API calls in the past two minutes: {self.two_min_limit_progress}\nSlow Down!'


class APICallResponseException(Exception):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return f'Error: Response code {self.code} returned.'
