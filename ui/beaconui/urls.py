from django.urls import path
from django.views.generic import TemplateView

from .views import (BeaconQueryView,
                    BeaconSNPView,
                    BeaconRegionView,
                    BeaconAccessLevelsView,
                    BeaconFilteringTermsView,
                    TestingView,
                    BeaconSamplesView)
from .auth import BeaconLoginView, BeaconLogoutView

urlpatterns = [
    # Query endpoints
    path('', BeaconQueryView.as_view(), name='query'),
    path('snp', BeaconSNPView.as_view(), name='snp'),
    path('region', BeaconRegionView.as_view(), name='region'),
    path('samples', BeaconSamplesView.as_view(), name='samples'),
    # Access Levels
    path('access-levels', BeaconAccessLevelsView.as_view(), name='levels'),
    # Filtering terms
    path('terms', BeaconFilteringTermsView.as_view(), name='filters'),
    path('terms/', BeaconFilteringTermsView.as_view(), name='filters/'),
    path('terms/<term>', BeaconFilteringTermsView.as_view(), name='filters-term'),
    # Login endpoints
    path('login', BeaconLoginView.as_view(), name='login'),
    path('privacy', TemplateView.as_view(template_name='privacy.html'), name='privacy'),
    path('logout', BeaconLogoutView.as_view(), name='logout'),
    # Testing
    path('testing', TestingView.as_view(), name='testing')
]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
