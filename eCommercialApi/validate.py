from oauth2_provider.oauth2_validators import OAuth2Validator
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()


class MyOAuth2Validator(OAuth2Validator):  # pylint: disable=w0223
    """ Primarily extend the functionality of token generation """

    def validate_user(self, username, password, client, request, *args, **kwargs):
        """ Here, you would be able to access the MOBILE/ OTP fields
            which you will be sending in the request.post body. """
        try:
            user = USER_MODEL.objects.get(telephone=request.telephone)
            if user is not None and user.is_active:
                check_password = user.check_password(password)
                if check_password is True:
                    request.user = user
                    return True

        except:
            print('telephone does not exit')

        return False
