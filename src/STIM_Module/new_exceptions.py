class NullGameException(Exception):
    def __str__(self):
        return "No game data returned"
