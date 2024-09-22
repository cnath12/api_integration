class OAuth2Auth:
    def __init__(self, access_token: str):
        self.access_token = access_token

    def get_auth_header(self):
        return {"Authorization": f"Bearer {self.access_token}"}