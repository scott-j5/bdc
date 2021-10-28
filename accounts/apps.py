from django.apps import AppConfig

from allauth.account.apps import AccountConfig
from allauth.socialaccount.apps import SocialAccountConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        import accounts.signals






# Explicitly defining default_auto_field for allauth. Any conflict between the created allauth id types and
# a default specified in settings.py will cause migrations to trigger each time (in a cd pipeline) and wipe perms from
#  sequences as they are "migrated" each time

class AccountConfig(AccountConfig):
	default_auto_field = 'django.db.models.AutoField'

class SocialAccountConfig(SocialAccountConfig):
	default_auto_field = 'django.db.models.AutoField'