import facebook

class Facebook:
    """
    Facebook Class for Social Authentication Management
    """

    @staticmethod
    def validate(auth_token):
        """
        Validate method that queries the Google API to fetch user info
        """
        try:
            graph = facebook.GraphAPI(access_token=auth_token)
            profile = graph.request("/me?fields=name,email")

            return profile
        except Exception as e:
            return "The token is either invalid or has expired."