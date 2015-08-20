from django.db import models
from django.contrib.auth.models import User


class Organisation(models.Model):

    name = models.CharField("Organisation Name", unique=True, max_length=32)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return "%s" % self.name


class Membership(models.Model):
    user = models.ForeignKey(User, related_name='organisations')
    organisation = models.ForeignKey(Organisation, related_name='members')

    class Meta:
        unique_together = ('user', 'organisation')

    def __unicode__(self):
        return "%s : %s" % (self.user, self.organisation)


class Domain(models.Model):

    organisation = models.ForeignKey(Organisation, related_name='domains')
    name = models.CharField(max_length=253, unique=True, help_text='Domain Name')

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return "%s" % self.name

    # def clean(self):
    #     validate_hostname_string(self.name)

    @property
    def owner_src(self):
        return self.organisation