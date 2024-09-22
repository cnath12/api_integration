from api_client.base_client import BaseApiClient
from config import API_BASE_URL, AUTH_METHOD, AUTH_PARAMS, COSMOS_CONFIG

def main():
    # Initialize the API client
    client = BaseApiClient(API_BASE_URL, AUTH_METHOD, AUTH_PARAMS, COSMOS_CONFIG)

    # Example GET request
    # response = client.get("users")
    # print("GET response:", response)

    # Example POST request
    new_user = {"id": "22", "name": "Doe", "job":"dev", "email": "abc@gmail.com"}
    response = client.post("users", data=new_user)
    print("POST response:", response)

    # Example PUT request
    # updated_user = {"name": "John Smith", "email": "john.smith@example.com"}
    # response = client.put("users/1", data=updated_user)
    # print("PUT response:", response)

    # # Example DELETE request
    # response = client.delete("users/1")
    # print("DELETE response:", response)

if __name__ == "__main__":
    main()