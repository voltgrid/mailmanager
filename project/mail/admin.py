from django.contrib import admin

import reversion

from .models import *


class CatchAllInline(admin.TabularInline):
    model = CatchAll
    extra = 0


class EmailAliasInline(admin.TabularInline):
    model = EmailAlias
    extra = 0


class EmailForwardInline(admin.TabularInline):
    model = EmailForward
    extra = 0


class EmailUserInline(admin.TabularInline):
    model = EmailUser
    extra = 0


@admin.register(EmailDomain)
class EmailDomainAdmin(admin.ModelAdmin):
    inlines = [EmailUserInline, CatchAllInline]
    list_display = ('__unicode__', 'users')
    list_filter = ('domain__organisation', )


@admin.register(EmailUser)
class EmailUserAdmin(reversion.VersionAdmin):
    inlines = [EmailAliasInline, EmailForwardInline, CatchAllInline]
    list_filter = ('domain', )
    list_display = ('__unicode__', 'aliases', 'forwards')
