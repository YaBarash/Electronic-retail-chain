from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly

from retail_chain.models import Company
from retail_chain.paginators import Pagination
from retail_chain.permissions import IsUserModerator, IsUserOwner
from retail_chain.serializers import CompanySerializer, CompanyAllFieldsSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanyAllFieldsSerializer
    pagination_class = Pagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["type", "name", "supplier", "level", "date_created"]

    def get_permissions(self):
        if not self.request.user.is_staff and self.request.user.is_active:
            if self.action in ["update", "retrieve", "create", "destroy"]:
                self.permission_classes = (IsUserModerator | IsUserOwner,)
            elif self.action == "list":
                self.permission_classes = (IsAuthenticatedOrReadOnly,)
        return super().get_permissions()
        serializer_class = CompanySerializer
        if self.action:
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()
