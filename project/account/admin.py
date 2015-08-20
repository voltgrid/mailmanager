from django.contrib import admin

from .models import Domain, Organisation, Membership
from .filters import filter_domain_queryset, filter_organisation_queryset


class DomainInline(admin.TabularInline):
    model = Domain
    extra = 0
    can_delete = False


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0


class OrganisationListFilter(admin.SimpleListFilter):
    """ Limit the List filter to valid options for the user """
    title = 'Organisation'
    parameter_name = 'organisation__id__exact'

    def lookups(self, request, model_admin):
        # TODO: Add different filtering for super users
        my_orgs = set([m.organisation for m in Membership.objects.filter(user=request.user)])
        return [(m.pk, m.name) for m in my_orgs]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(organisation_id=self.value())
        else:
            return queryset


class DomainOrganisationListFilter(OrganisationListFilter):
    """ Limit the List filter to valid options for the user """
    parameter_name = 'domain_organisation__id__exact'

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(domain__organisation_id=self.value())
        else:
            return queryset


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'organisation', 'name',)
    list_filter = (OrganisationListFilter,)

    def get_queryset(self, request):
        """ Limit results to qs """
        qs = super(DomainAdmin, self).get_queryset(request)
        return filter_domain_queryset(qs, request)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """ Limit choices for 'organisation' field """
        if db_field.name == 'organisation':
            kwargs["queryset"] = filter_organisation_queryset(Organisation.objects.all(), request)
        return super(DomainAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name',)
    list_filter = ('name',)
    inlines = (MembershipInline, DomainInline)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'user', 'organisation')
    list_filter = ('user', 'organisation')