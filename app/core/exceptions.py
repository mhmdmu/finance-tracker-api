class AuthenticationFailed(Exception):
    def __init__(self):
        super().__init__("Authentication failed - Invalid credentials")


class DuplicateUsername(Exception):
    def __init__(self):
        super().__init__("Registeration failed")


class InvalidAccountType(Exception):
    def __init__(self):
        super().__init__("Invalid account type - allowed only (cash, bank, credit)")


class AccountNotFound(Exception):
    def __init__(self, id):
        super().__init__(f"Account not found - id: {id} not exist")
