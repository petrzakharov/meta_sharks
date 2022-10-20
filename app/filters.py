from django_filters import rest_framework as filters

from app.models import Order


class CustomFilterAndOrdering(filters.FilterSet):
    brand = filters.CharFilter(field_name='model__brand__title', lookup_expr='contains')
    sort = filters.OrderingFilter(
        fields=(
            ('quantity', 'quantity'),
        )
    )

    class Meta:
        model = Order
        fields = ['brand']
