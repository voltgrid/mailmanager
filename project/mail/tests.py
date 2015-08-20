from django.test import TestCase
from model_mommy import mommy

from project.account.models import Domain
from .models import EmailDomain, EmailUser, EmailForward, EmailAlias, CatchAll


class MailCreationTest(TestCase):

    def test_domain_creation(self):
        domain = mommy.make_recipe('vg.account.domain')
        self.assertTrue(isinstance(domain, Domain))

    def test_email_domain_creation(self):
        email_domain = mommy.make_recipe('vg.mail.email_domain')
        self.assertTrue(isinstance(email_domain, EmailDomain))

    def test_email_user_creation(self):
        email_user = mommy.make_recipe('vg.mail.email_user')
        self.assertTrue(isinstance(email_user, EmailUser))

    def test_email_forward_creation(self):
        email_forward = mommy.make_recipe('vg.mail.email_forward')
        self.assertTrue(isinstance(email_forward, EmailForward))

    def test_email_alias_creation(self):
        email_alias = mommy.make_recipe('vg.mail.email_alias')
        self.assertTrue(isinstance(email_alias, EmailAlias))

    def text_catch_all_creation(self):
        catch_all = mommy.make_recipe('vg.mail.catch_all')
        self.assertTrue(isinstance(catch_all, CatchAll))