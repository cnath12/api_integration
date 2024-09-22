# API Client Template

This project provides a template for creating a robust API client in Python. It includes features such as authentication, rate limiting, and retry mechanisms.

## Features

- Support for multiple HTTP methods (GET, POST, PUT, DELETE)
- Multiple authentication methods (Basic Auth, API Key, OAuth 2.0)
- Rate limiting
- Retry mechanism with exponential backoff
- Easy to extend and customize

## Project Structure

```
api_client_template/
├── api_client/
│   ├── __init__.py
│   └── base_client.py
├── auth/
│   ├── __init__.py
│   ├── basic_auth.py
│   ├── api_key_auth.py
│   └── oauth2_auth.py
├── utils/
│   ├── __init__.py
│   ├── rate_limiter.py
│   └── retry_mechanism.py
├── tests/
│   ├── __init__.py
│   └── test_api_client.py
├── config.py
├── main.py
└── requirements.txt
```

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/api_client_template.git
   cd api_client_template
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Configure the API client in `config.py`:
   ```python
   API_BASE_URL = "https://api.example.com"
   AUTH_METHOD = "basic"
   AUTH_PARAMS = {
       "username": "your_username",
       "password": "your_password"
   }
   ```

2. Run the main script:
   ```
   python main.py
   ```

3. To run tests:
   ```
   python -m unittest discover tests
   ```

## Customization

To use this template for your specific API:

1. Modify the `BaseApiClient` class in `api_client/base_client.py` to add any API-specific methods.
2. Update the authentication methods in the `auth/` directory if needed.
3. Adjust the rate limiting parameters in `utils/rate_limiter.py` to match your API's requirements.
4. Add more tests in the `tests/` directory for your specific use cases.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
