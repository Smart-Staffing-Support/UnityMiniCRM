from rest_framework import viewsets, status, serializers
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta

from .models import Company, Contact, Deal, Task, TimelineEvent, Notification
from .serializers import (
    CompanySerializer, ContactSerializer, DealSerializer,
    TaskSerializer, UserSerializer, TimelineEventSerializer, NotificationSerializer
)
from .utils.email import send_html_email

import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout_view(request):
    if request.user.is_authenticated:
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
        'deals_by_stage': list(Deal.objects.values('stage').annotate(count=Count('id'))),
        'total_deal_value': Deal.objects.aggregate(total=Sum('amount'))['total'] or 0,
        'won_deals_value': Deal.objects.filter(stage='won').aggregate(total=Sum('amount'))['total'] or 0,
        'pending_tasks': Task.objects.filter(status='pending').count(),
        'overdue_tasks': Task.objects.filter(
            due_date__lt=timezone.now(),
            status__in=['pending', 'in_progress']
        ).count() if 'timezone' in dir() else 0,
    }
    return Response(stats)


# ---------------------------
# VIEWSETS + TIMELINE LOGGING
# ---------------------------

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        company = serializer.save(created_by=self.request.user)
        event = TimelineEvent.objects.create(
            event_type="company_created",
            description=f"Created company {company.name}",
            user=self.request.user,
            related_company=company
        )

        Notification.objects.create(
            user=self.request.user, timeline_event=event)

        try:
            self.send_company_email(company)
        except Exception as e:
            logger.error(
                f"Failed to send company email for {company.name}: {str(e)}")
            raise serializers.ValidationError({"email_error": str(e)})

    def send_company_email(self, company):
        deals = company.deals.all()
        if company.email:
            send_html_email(
                subject=f"Welcome {company.name}!",
                template_name="emails/company_created.html",
                context={"company": company, "deals": deals},
                recipient_list=[company.email]
            )

    def perform_update(self, serializer):
        company = serializer.save()
        event = TimelineEvent.objects.create(
            event_type="company_updated",
            description=f"Updated company {company.name}",
            user=self.request.user,
            related_company=company
        )

        Notification.objects.create(
            user=self.request.user, timeline_event=event)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        contact = serializer.save(created_by=self.request.user)
        TimelineEvent.objects.create(
            event_type="contact_created",
            description=f"Created contact {contact.full_name}",
            user=self.request.user,
            related_contact=contact,
            related_company=contact.company
        )

    def perform_update(self, serializer):
        contact = serializer.save()
        TimelineEvent.objects.create(
            event_type="contact_updated",
            description=f"Updated contact {contact.full_name}",
            user=self.request.user,
            related_contact=contact,
            related_company=contact.company
        )

class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        deal = serializer.save(created_by=self.request.user)
        event = TimelineEvent.objects.create(
            event_type="deal_created",
            description=f"Created deal {deal.title}",
            user=self.request.user,
            related_deal=deal,
            related_company=deal.company
        )

        Notification.objects.create(
            user=self.request.user, timeline_event=event)

        if deal.company and deal.company.email:
            send_html_email(
                subject=f"New Deal Created: {deal.title}",
                template_name="emails/deal_created.html",
                context={"deal": deal},
                recipient_list=[deal.company.email]
            )

    def perform_update(self, serializer):
        existing = self.get_object()
        old_stage = existing.stage

        deal = serializer.save()

        if old_stage != deal.stage:
            event = TimelineEvent.objects.create(
                event_type="deal_stage_changed",
                description=f"Deal '{deal.title}' moved from {old_stage} → {deal.stage}",
                user=self.request.user,
                related_deal=deal,
                related_company=deal.company
            )

            Notification.objects.create(
                user=self.request.user, timeline_event=event)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        task = serializer.save(created_by=self.request.user)
        TimelineEvent.objects.create(
            event_type="task_created",
            description=f"Created task '{task.title}'",
            user=self.request.user,
            related_task=task,
            related_deal=task.deal,
            related_contact=task.contact
        )

    def perform_update(self, serializer):
        existing = self.get_object()
        old_status = existing.status
        old_assigned = existing.assigned_to
        task = serializer.save()

        if old_status != task.status and task.status == "completed":
            TimelineEvent.objects.create(
                event_type="task_completed",
                description=f"Completed task '{task.title}'",
                user=self.request.user,
                related_task=task,
                related_deal=task.deal,
                related_contact=task.contact
            )
        if old_assigned != task.assigned_to and task.assigned_to:
            TimelineEvent.objects.create(
                event_type="task_assigned",
                description=f"Task '{task.title}' assigned to {task.assigned_to.username}",
                user=self.request.user,
                related_task=task
            )


# ---------------------------
# TIMELINE VIEW
# ---------------------------

class TimelineViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TimelineEvent.objects.all().order_by("-created_at")
    serializer_class = TimelineEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = TimelineEvent.objects.filter(
            created_at__lte=timezone.now()
        ).order_by("-created_at")

        period = self.request.query_params.get("period")
        now = timezone.now()

        if period == "today":
            start = timezone.localtime(now).replace(
                hour=0, minute=0, second=0, microsecond=0)
            qs = qs.filter(created_at__gte=start)
        elif period == "last_week":
            start = timezone.localtime(now) - timedelta(days=7)
            qs = qs.filter(created_at__gte=start)
        elif period == "last_month":
            start = timezone.localtime(now) - timedelta(days=30)
            qs = qs.filter(created_at__gte=start)

        raw_event_types = self.request.query_params.getlist("event_type")
        event_types = []
        for item in raw_event_types:
            event_types.extend(item.split(","))
        event_types = [e.strip() for e in event_types if e.strip()]

        if event_types:
            qs = qs.filter(event_type__in=event_types)

        return qs


# ---------------------------
# NOTIFICATION VIEWSET
# ---------------------------

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-created_at")

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.read = True
        notification.save()
        return Response({'status': 'marked as read'})

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        notifications = self.get_queryset().filter(read=False)
        count = notifications.update(read=True)
        return Response({'status': f'{count} notifications marked as read'})
