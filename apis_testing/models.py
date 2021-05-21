from django.db import models
from django.contrib.auth.models import User


# Gmail Credentials models
class CredentialsManager(models.Manager):

    def create_credentials(self, user, credentials, valid=True):
        gmail_credentials = self.create(
            user=user,
            token=credentials.token,
            refresh_token=credentials.refresh_token,
            id_token=credentials.id_token,
            token_uri=credentials.token_uri,
            scopes=','.join(credentials.scopes),
            expiry=credentials.expiry,
            valid=valid
        )
        return gmail_credentials


class GmailCredentials(models.Model):
    user = models.OneToOneField(
        User, related_name='credentials', on_delete=models.CASCADE)
    token = models.CharField(max_length=200, null=True)
    refresh_token = models.CharField(max_length=200, null=True)
    id_token = models.CharField(max_length=200, null=True)
    token_uri = models.CharField(max_length=200, null=True)
    scopes = models.CharField(max_length=1000, null=True)
    expiry = models.DateTimeField(blank=True, null=True)
    valid = models.BooleanField(default=True)

    objects = CredentialsManager()
