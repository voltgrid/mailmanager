from passlib.hash import sha512_crypt  # Runtime import

from django.db import models
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from project.account.models import Domain


# TODO: Add support for 'Domain Aliases' where all the local parts of the other domain_a are aliased to domain_b.


class EmailDomain(models.Model):

    domain = models.ForeignKey(Domain)
    #domain_aliases = models.ManyToManyField(Domain)  # This might work

    class Meta:
        ordering = ['domain']
        verbose_name_plural = 'Domains'

    def __unicode__(self):
        return "%s" % self.domain

    @property
    def owner_src(self):
        return self.domain.owner_src

    def users(self):
        return self.emailuser_set.count()


class EmailUser(models.Model):

    domain = models.ForeignKey(EmailDomain)
    name = models.CharField(max_length=64, help_text="Local part of email address")
    password = models.CharField(max_length=256, help_text="Hashed Password")
    quota = models.IntegerField(default=512, help_text='Quota in MB')

    class Meta:
        ordering = ['name', 'domain']
        unique_together = (('domain', 'name'),)
        verbose_name_plural = 'Users'

    def __unicode__(self):
        return "%s@%s" % (self.name, self.domain)

    def save(self, *args, **kwargs):
        """ hash password on change or create """
        try:
            e = EmailUser.objects.get(pk=self.pk)
            if not e.password == self.password:
                self.password = sha512_crypt.encrypt(self.password)
        except EmailUser.DoesNotExist:
            self.password = sha512_crypt.encrypt(self.password)
        super(EmailUser, self).save(*args, **kwargs)

    def aliases(self):
        return self.emailalias_set.count()

    def forwards(self):
        return self.emailforward_set.count()

    @property
    def description(self):
        return 'Hosted Email Account (%s)' % self.__unicode__()

    @property
    def owner_src(self):
        return self.domain.owner_src


class EmailForward(models.Model):

    user = models.ForeignKey(EmailUser)
    destination = models.EmailField()

    class Meta:
        unique_together = (('user', 'destination'),)

    def __unicode__(self):
        return "%s -> %s" % (self.user, self.destination)

    @property
    def owner_src(self):
        return self.user.owner_src


class EmailAlias(models.Model):

    user = models.ForeignKey(EmailUser)
    alias = models.CharField(max_length=64, help_text="Alias (local part)")

    class Meta:
        ordering = ['alias']
        unique_together = (('user', 'alias'),)
        verbose_name_plural = 'Email Alias'

    def __unicode__(self):
        return "%s@%s -> %s@%s" % (self.alias, self.user.domain, self.user.name, self.user.domain)

    @property
    def owner_src(self):
        return self.user.owner_src


class CatchAll(models.Model):
    """ Catch all unaddressed email for domain and send to user """
    # FIXME: I think these are broken.
    domain = models.ForeignKey(EmailDomain)
    user = models.ForeignKey(EmailUser)

    class Meta:
        ordering = ['domain', 'user']
        unique_together = (('domain', 'user'))
        verbose_name_plural = 'Catch All'

    def __unicode__(self):
        return "@%s -> %s@%s" % (self.domain, self.user.name, self.user.domain)

    def clean(self):
        try:
            if self.domain.domain.organisation.id != self.user.domain.domain.organisation.id:
                raise ValidationError('User not in same organisation as Domain.')
        except ObjectDoesNotExist:
            # In case that web_app fails to validate
            pass

    @property
    def owner_src(self):
        return self.user.owner_src