import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name='sender__username', lookup_expr='icontains')
    sent_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Message
        fields = ['user', 'sent_at']
