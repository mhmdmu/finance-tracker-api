class AuthenticationFailed(Exception):
    def __init__(self):
        super().__init__("Authentication failed - Invalid credentials")


class DuplicateUsername(Exception):
    def __init__(self):
        super().__init__("Registeration failed")
