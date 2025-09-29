from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    """
    Extends the default JWT authentication to add extra logic if needed.
    """

    def authenticate(self, request):
        # Let the parent do the heavy lifting
        user_auth_tuple = super().authenticate(request)

        if user_auth_tuple is None:
            return None  # No valid token

        user, token = user_auth_tuple

        # Example: deny inactive users
        if not user.is_active:
            raise AuthenticationFailed("User account is disabled.")

        return (user, token)
