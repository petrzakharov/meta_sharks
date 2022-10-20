from django.db.models import Sum
from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination

from app.filters import CustomFilterAndOrdering
from app.models import Brand, Color, ModelType, Order
from app.serializers import (BrandReportSerializer, BrandSerializer,
                             ColorReportSerializer, ColorSerializer,
                             ModelTypeSerializer, OrderReadSerializer,
                             OrderSerializer)


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class ColorReportViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = (
        Order.objects.select_related('color')
        .values('color__title')
        .annotate(quantity=Sum('quantity'))
        .order_by('-quantity')
    )
    serializer_class = ColorReportSerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandReportViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = (
        Order.objects.select_related('model__brand')
        .values('model__brand__title')
        .annotate(quantity=Sum('quantity'))
        .order_by('-quantity')
    )
    serializer_class = BrandReportSerializer


class ModelTypeViewSet(viewsets.ModelViewSet):
    queryset = ModelType.objects.select_related('brand')
    serializer_class = ModelTypeSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = (
        Order.objects.select_related(
            'color', 'model', 'model__brand'
        ).all()
    )
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CustomFilterAndOrdering
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return OrderReadSerializer
        return OrderSerializer
