from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.core import mail
from tasks.models import Company, Deal, Notification, TimelineEvent
from django.utils import timezone

class CompanyEmailTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        mail.outbox = []

    def test_company_creation_creates_timeline_notification_and_sends_email(self):
        """Creating a company should:
           - return 201
           - create a TimelineEvent with event_type 'company_created'
           - create a Notification for the current user referencing that event
           - send exactly one email to the company's email
        """
        data = {"name": "Test Company", "email": "test@example.com"}

        response = self.client.post("/api/companies/", data, format='json')
        self.assertEqual(response.status_code, 201)

        events = TimelineEvent.objects.filter(
            event_type="company_created",
            related_company__name="Test Company"
        )
        self.assertEqual(events.count(), 1)
        event = events.first()
        self.assertIn("Created company", event.description)
        self.assertEqual(event.user, self.user)

        notifications = Notification.objects.filter(user=self.user, timeline_event=event)
        self.assertEqual(notifications.count(), 1)
        notif = notifications.first()
        self.assertFalse(notif.read)

        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.subject, "Welcome Test Company!")
        self.assertIn("Test Company", email.body)
        self.assertEqual(email.to, ["test@example.com"])


class DealEmailTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.company = Company.objects.create(
            name="TestCo",
            email="company@example.com",
            created_by=self.user
        )
        mail.outbox = []

    def test_deal_creation_creates_timeline_notification_and_sends_email(self):
        """Creating a deal should:
           - return 201
           - create a TimelineEvent with event_type 'deal_created'
           - create a Notification for the user referencing that event
           - send exactly one email to the company if company.email exists
        """
        data = {"title": "Big Deal", "amount": 5000, "stage": "lead", "company": self.company.id}

        response = self.client.post("/api/deals/", data, format='json')
        self.assertEqual(response.status_code, 201)

        events = TimelineEvent.objects.filter(
            event_type="deal_created",
            related_deal__title="Big Deal"
        )
        self.assertEqual(events.count(), 1)
        event = events.first()
        self.assertIn("Created deal", event.description)
        self.assertEqual(event.user, self.user)

        notifications = Notification.objects.filter(user=self.user, timeline_event=event)
        self.assertEqual(notifications.count(), 1)
        notif = notifications.first()
        self.assertFalse(notif.read)

        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.subject, "New Deal Created: Big Deal")
        self.assertIn("Big Deal", email.body)
        self.assertEqual(email.to, ["company@example.com"])


class NotificationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        mail.outbox = []

    def test_notification_created_on_company_creation(self):
        data = {"name": "NotifyCo", "email": "notify@example.com"}
        resp = self.client.post("/api/companies/", data, format='json')
        self.assertEqual(resp.status_code, 201)

        notifications = Notification.objects.filter(user=self.user)
        self.assertEqual(notifications.count(), 1)

        event = notifications.first().timeline_event
        self.assertIsNotNone(event)
        self.assertEqual(event.event_type, "company_created")
        self.assertIn("NotifyCo", event.description)

    def test_notification_created_on_deal_creation(self):
        company = Company.objects.create(
            name="DealCo",
            email="deal@example.com",
            created_by=self.user
        )
        data = {"title": "Mega Deal", "amount": 10000, "stage": "lead", "company": company.id}

        resp = self.client.post("/api/deals/", data, format='json')
        self.assertEqual(resp.status_code, 201)

        notifications = Notification.objects.filter(user=self.user)
        self.assertEqual(notifications.count(), 1)

        event = notifications.first().timeline_event
        self.assertIsNotNone(event)
        self.assertEqual(event.event_type, "deal_created")
        self.assertIn("Mega Deal", event.description)
