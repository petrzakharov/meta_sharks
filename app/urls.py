from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app import views

router = DefaultRouter()
router.register('orders', views.OrderViewSet, basename='orders')
router.register('colors', views.ColorViewSet, basename='colors')
router.register('brands', views.BrandViewSet, basename='brands')
router.register('models', views.ModelTypeViewSet, basename='models')
router.register('colors-report', views.ColorReportViewSet, basename='colors-report')
router.register('brands-report', views.BrandReportViewset, basename='brands-report')

urlpatterns = [
    path('', include(router.urls)),
]
