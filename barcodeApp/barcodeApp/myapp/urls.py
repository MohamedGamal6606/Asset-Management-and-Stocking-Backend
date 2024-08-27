from django.urls import path
from .views import (
    AssetViewSet, 
    AssetCountListView,
    CountryListView,
    AreaListView, 
    BuildingListView, 
    OfficeListView,
    GovernateListView,
    BarcodeViewSet,
    CategoryViewSet,
    CustomAuthToken,
    ConfigurationViewSet
    )
from django.conf import settings
from django.conf.urls.static import static





urlpatterns = [
    path('configuration/', ConfigurationViewSet.as_view(), name='configuration-list'),
    path('barcode/', BarcodeViewSet.as_view(), name='barcode-list'),
    path('category/', CategoryViewSet.as_view(), name='category-list'),
    path('assets/', AssetViewSet.as_view(), name='asset-list-create'),
    path('assetcounts/', AssetCountListView.as_view(), name='assetcount-list'),
    path('api/login/',  CustomAuthToken.as_view(), name='api_login'),
    path('countries/', CountryListView.as_view(), name='country-list'),
    path('governate/', GovernateListView.as_view(), name='governate-list'),
    path('areas/', AreaListView.as_view(), name='area-list'),
    path('buildings/', BuildingListView.as_view(), name='building-list'),
    path('offices/', OfficeListView.as_view(), name='office-list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)