from datetime import timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Company, Contact, Deal, Interaction


class InteractionAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='testpass123')

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.company = Company.objects.create(
            name='Acme Inc',
            created_by=self.user
        )

        self.contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            company=self.company,
            created_by=self.user
        )

        self.deal = Deal.objects.create(
            title='Enterprise Plan',
            amount=15000,
            stage='lead',
            probability=25,
            company=self.company,
            contact=self.contact,
            created_by=self.user
        )

        self.list_url = '/api/interactions/'

    def get_payload(self):
        return {
            'contact': self.contact.id,
            'company': self.company.id,
            'deal': self.deal.id,
            'interaction_type': 'call',
            'subject': 'Initial qualification call',
            'notes': 'Customer asked for pricing details.',
            'interaction_date': timezone.now().isoformat(),
            'follow_up_date': (timezone.now() + timedelta(days=2)).isoformat(),
        }

    def test_create_interaction_successfully(self):
        response = self.client.post(self.list_url, self.get_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Interaction.objects.count(), 1)
        self.assertEqual(Interaction.objects.first().subject, 'Initial qualification call')

    def test_create_interaction_requires_subject(self):
        payload = self.get_payload()
        payload['subject'] = ''
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('subject', response.data)

    def test_follow_up_date_cannot_be_before_interaction_date(self):
        now = timezone.now()
        payload = self.get_payload()
        payload['interaction_date'] = now.isoformat()
        payload['follow_up_date'] = (now - timedelta(days=1)).isoformat()

        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('follow_up_date', response.data)

    def test_list_interactions(self):
        Interaction.objects.create(
            contact=self.contact,
            company=self.company,
            deal=self.deal,
            interaction_type='email',
            subject='Follow-up email',
            notes='Sent proposal document.',
            interaction_date=timezone.now(),
            created_by=self.user
        )

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_interaction(self):
        interaction = Interaction.objects.create(
            contact=self.contact,
            company=self.company,
            deal=self.deal,
            interaction_type='meeting',
            subject='Discovery meeting',
            notes='Met with stakeholders.',
            interaction_date=timezone.now(),
            created_by=self.user
        )

        payload = {
            'contact': self.contact.id,
            'company': self.company.id,
            'deal': self.deal.id,
            'interaction_type': 'meeting',
            'subject': 'Updated discovery meeting',
            'notes': 'Meeting notes updated.',
            'interaction_date': timezone.now().isoformat(),
            'follow_up_date': (timezone.now() + timedelta(days=3)).isoformat(),
        }

        response = self.client.put(f'/api/interactions/{interaction.id}/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        interaction.refresh_from_db()
        self.assertEqual(interaction.subject, 'Updated discovery meeting')

    def test_delete_interaction(self):
        interaction = Interaction.objects.create(
            contact=self.contact,
            company=self.company,
            deal=self.deal,
            interaction_type='note',
            subject='Internal note',
            notes='Do not forget to follow up.',
            interaction_date=timezone.now(),
            created_by=self.user
        )

        response = self.client.delete(f'/api/interactions/{interaction.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Interaction.objects.count(), 0)

    def test_interaction_requires_contact(self):
        payload = self.get_payload()
        payload['contact'] = None

        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('contact', response.data)