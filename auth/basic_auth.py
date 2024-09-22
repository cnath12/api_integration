import base64

class BasicAuth:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def get_auth_header(self):
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {"Authorization": f"Basic {encoded_credentials}"}