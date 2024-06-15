
from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_url(self, request, emailconfirmation):

        """
            Changing the confirmation URL to fit the domain that we are working on
        """

        url = (
            "http://localhost:3000/activation/"
            + emailconfirmation.key
        )
        return url

    
    
    