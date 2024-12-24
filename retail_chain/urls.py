from django.urls import path, include
from rest_framework.routers import DefaultRouter

from retail_chain.apps import RetailChainConfig
from retail_chain.views import CompanyViewSet

app_name = RetailChainConfig.name

router1 = DefaultRouter()
router1.register(r"companies", CompanyViewSet, basename="companies")
urlpatterns = [
    path("", include(router1.urls)),
    # path("get_book/", GetBookView.as_view()),
    # path("get_qr_book/", QRCodeAPIView.as_view())
]
