from django.contrib.auth import authenticate
from django.db.models import Count, Sum
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Company, Contact, Deal, Task
from .serializers import (
    CompanySerializer,
    ContactSerializer,
    DealSerializer,
    TaskSerializer,
    UserSerializer,
)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user": UserSerializer(user).data}
        )
    return Response(
        {"error": "Invalid credentials"},
        status=status.HTTP_401_UNAUTHORIZED,
    )


@api_view(["POST"])
def logout_view(request):
    request.user.auth_token.delete()
    return Response({"message": "Logged out successfully"})


@api_view(["GET"])
def dashboard_stats(request):
    return Response({
        "total_contacts": Contact.objects.count(),
        "total_companies": Company.objects.count(),
        "total_deals": Deal.objects.count(),
        "total_tasks": Task.objects.count(),
        "deals_by_stage": list(
            Deal.objects.values("stage").annotate(count=Count("id"))
        ),
        "total_deal_value": Deal.objects.aggregate(total=Sum("amount"))[
            "total"
        ]
        or 0,
        "won_deals_value": Deal.objects.filter(stage="won").aggregate(
            total=Sum("amount")
        )["total"]
        or 0,
        "pending_tasks": Task.objects.filter(status="pending").count(),
        "overdue_tasks": Task.objects.filter(
            due_date__lt=timezone.now(), status__in=["pending", "in_progress"]
        ).count()
        if "timezone" in dir()
        else 0,
    })


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
