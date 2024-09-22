class ApiKeyAuth:
    def __init__(self, api_key: str, header_name: str = "X-API-Key"):
        self.api_key = api_key
        self.header_name = header_name

    def get_auth_header(self):
        return {self.header_name: self.api_key}