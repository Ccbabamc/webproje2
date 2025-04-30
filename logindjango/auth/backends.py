from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()

class TCAuthenticationBackend(ModelBackend):
    """
    Allows authentication using either username (which stores TC) or the dedicated tc_kimlik_no field.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Try authenticating with username first (which might be TC)
        user = super().authenticate(request, username=username, password=password, **kwargs)

        if user is None and username is not None:
            # If username auth failed, try authenticating with tc_kimlik_no
            try:
                # Check if a user with the given identifier as tc_kimlik_no exists
                user = UserModel.objects.get(tc_kimlik_no=username)
                if user.check_password(password) and self.user_can_authenticate(user):
                    return user
            except UserModel.DoesNotExist:
                # No user found with that tc_kimlik_no either
                return None
        
        return user # Return the user found by username or None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
