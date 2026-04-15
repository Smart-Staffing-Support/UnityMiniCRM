from django.contrib.auth import authenticate
from django.db.models import Count, Sum
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import Company, Contact, Deal, Task, Interaction
from .serializers import (
    CompanySerializer,
    ContactSerializer,
    DealSerializer,
    TaskSerializer,
    InteractionSerializer,
    UserSerializer,
)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = str(request.data.get('username', '')).strip()
    password = str(request.data.get('password', '')).strip()

    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout_view(request):
    if request.user.is_authenticated and hasattr(request.user, 'auth_token'):
        request.user.auth_token.delete()
    return Response({'message': 'Logged out successfully'})


@api_view(['GET'])
def dashboard_stats(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

    stats = {
        'total_contacts': Contact.objects.count(),
        'total_companies': Company.objects.count(),
        'total_deals': Deal.objects.count(),
        'total_tasks': Task.objects.count(),
        'total_interactions': Interaction.objects.count(),
        'deals_by_stage': list(Deal.objects.values('stage').annotate(count=Count('id'))),
        'interactions_by_type': list(Interaction.objects.values('interaction_type').annotate(count=Count('id'))),
        'total_deal_value': Deal.objects.aggregate(total=Sum('amount'))['total'] or 0,
        'won_deals_value': Deal.objects.filter(stage='won').aggregate(total=Sum('amount'))['total'] or 0,
        'pending_tasks': Task.objects.filter(status='pending').count(),
        'overdue_tasks': Task.objects.filter(
            due_date__lt=timezone.now(),
            status__in=['pending', 'in_progress']
        ).count(),
        'overdue_follow_ups': Interaction.objects.filter(
            follow_up_date__lt=timezone.now()
        ).count(),
    }
    return Response(stats)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class InteractionViewSet(viewsets.ModelViewSet):
    serializer_class = InteractionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Interaction.objects.select_related(
        'contact', 'company', 'deal', 'created_by'
    ).all()

    def get_queryset(self):
        queryset = super().get_queryset()

        contact_id = self.request.query_params.get('contact')
        company_id = self.request.query_params.get('company')
        deal_id = self.request.query_params.get('deal')
        interaction_type = self.request.query_params.get('interaction_type')
        follow_up_status = self.request.query_params.get('follow_up_status')

        if contact_id:
            queryset = queryset.filter(contact_id=contact_id)

        if company_id:
            queryset = queryset.filter(company_id=company_id)

        if deal_id:
            queryset = queryset.filter(deal_id=deal_id)

        if interaction_type:
            queryset = queryset.filter(interaction_type=interaction_type)

        if follow_up_status == 'overdue':
            queryset = queryset.filter(follow_up_date__lt=timezone.now())

        if follow_up_status == 'upcoming':
            queryset = queryset.filter(follow_up_date__gte=timezone.now())

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)