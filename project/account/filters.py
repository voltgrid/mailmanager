

def filter_domain_queryset(qs, request):
    user = request.user
    if user.is_superuser:
        return qs
    return qs.filter(organisation_id__in=user.organisations.values_list('organisation_id', flat=True))


def filter_organisation_queryset(qs, request):
    user = request.user
    if user.is_superuser:
        return qs
    return qs.filter(pk__in=request.user.organisations.values_list('organisation_id', flat=True))
