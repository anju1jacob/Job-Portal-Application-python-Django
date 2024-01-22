import django_filters
from jobportalapp.models import job

class Jobfilter(django_filters.FilterSet):
    title=django_filters.CharFilter(lookup_expr='icontains')
    location=django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model=job
        fields=['title', 'location', 'job_type']


