from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly

from retail_chain.models import Company, Product, Contacts
from retail_chain.paginators import Pagination
from retail_chain.permissions import IsUserModerator, IsUserOwner
from retail_chain.serializers import (
    CompanySerializer,
    CompanyAllFieldsSerializer,
    ProductSerializer,
    ContactsSerializer,
)


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

    def create(self, request, *args, **kwargs):
        """Метод , запрещяющий добавлять через АПИ задолженость"""
        serializer = self.get_serializer(data=request.data)
        if (
            request.data.get("debt") is None
            and request.data.get("debt_currency") is None
        ):
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        data = {"error": f"Ошибка с кодом 403. Вы не можете указывать задолженность"}
        return JsonResponse(
            data["error"],
            safe=False,
            status=status.HTTP_400_BAD_REQUEST,
            json_dumps_params={"ensure_ascii": False},
        )

    def perform_update(self, serializer):
        """Метод , запрещяющий обновлять через АПИ задолженость"""
        if self.request.data.get("debt"):
            data = {"error": f"Ошибка с кодом 403. Вы не можете менять задолженность"}
            return JsonResponse(
                data["error"],
                safe=False,
                status=status.HTTP_400_BAD_REQUEST,
                json_dumps_params={"ensure_ascii": False},
            )
        serializer.save()
        Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = Pagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["product_name", "product_model", "product_date"]

    def get_permissions(self):
        if self.request.user.is_active:
            if self.action in ["update", "retrieve", "create", "destroy"]:
                self.permission_classes = (IsUserModerator | IsUserOwner | IsAdminUser,)
            elif self.action == "list":
                self.permission_classes = (IsAuthenticatedOrReadOnly,)
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (
            request.data.get("product_name") is None
            or request.data.get("product_model")
            or request.data.get("product_name").isdigit()
        ):
            data = {"error": f"Ошибка с кодом 400. Укажите название продукта"}
            return JsonResponse(
                data["error"],
                safe=False,
                status=status.HTTP_400_BAD_REQUEST,
                json_dumps_params={"ensure_ascii": False},
            )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ContactsViewSet(viewsets.ModelViewSet):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer
    pagination_class = Pagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["country"]

    def get_permissions(self):
        if self.request.user.is_active:
            if self.action:
                self.permission_classes = (IsUserModerator | IsUserOwner | IsAdminUser,)
        return super().get_permissions()
