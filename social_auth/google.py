from google.auth.transport import requests
from google.oauth2 import id_token

class Google:
    """
    Google Class for Social Authentication Management
    """

    @staticmethod
    def validate(auth_token):
        """
        Validate method that queries the Google API to fetch user info
        """
        try:
            id_info = id_token.verify_oauth2_token(auth_token, requests.Request())

            if 'accounts.google.com' in id_info['iss']:
                return id_info
        except Exception as e:
            return "The token is either invalid or has expired."