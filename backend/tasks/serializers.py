from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Company, Contact, Deal, Task, TimelineEvent, Notification

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class CompanySerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(
        source='created_by.username', read_only=True)
    contacts_count = serializers.SerializerMethodField()
    deals_count = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'industry', 'website', 'phone', 'email', 'address',
                  'notes', 'created_at', 'updated_at', 'created_by', 'created_by_name',
                  'contacts_count', 'deals_count']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']

    def get_contacts_count(self, obj):
        return obj.contacts.count()

    def get_deals_count(self, obj):
        return obj.deals.count()


class ContactSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    company_name = serializers.CharField(source='company.name', read_only=True)
    created_by_name = serializers.CharField(
        source='created_by.username', read_only=True)

    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'phone',
                  'position', 'company', 'company_name', 'notes', 'created_at',
                  'updated_at', 'created_by', 'created_by_name']
        read_only_fields = ['id', 'created_at',
                            'updated_at', 'created_by', 'full_name']


class DealSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    contact_name = serializers.CharField(
        source='contact.full_name', read_only=True)
    created_by_name = serializers.CharField(
        source='created_by.username', read_only=True)

    class Meta:
        model = Deal
        fields = ['id', 'title', 'amount', 'stage', 'probability', 'expected_close_date',
                  'company', 'company_name', 'contact', 'contact_name', 'notes',
                  'created_at', 'updated_at', 'created_by', 'created_by_name']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']

class TaskSerializer(serializers.ModelSerializer):
    contact_name = serializers.CharField(
        source='contact.full_name', read_only=True)
    deal_title = serializers.CharField(source='deal.title', read_only=True)
    assigned_to_name = serializers.SerializerMethodField()
    created_by_name = serializers.CharField(
        source='created_by.username', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority', 'due_date',
            'contact', 'contact_name', 'deal', 'deal_title',
            'assigned_to', 'assigned_to_name',
            'created_at', 'updated_at', 'created_by', 'created_by_name'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']

    def get_assigned_to_name(self, obj):
        if obj.assigned_to:
            return f"{obj.assigned_to.first_name} {obj.assigned_to.last_name} ({obj.assigned_to.email})"
        return None

    def validate(self, data):
        assigned_to = data.get('assigned_to')

        if assigned_to:
            try:
                contact = Contact.objects.get(id=assigned_to.id)
                data['assigned_to'] = contact.created_by
            except Contact.DoesNotExist:
                pass

        return data
class TimelineEventSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    company_name = serializers.CharField(
        source='related_company.name', read_only=True)
    contact_name = serializers.SerializerMethodField()
    deal_name = serializers.CharField(
        source='related_deal.title', read_only=True)
    task_title = serializers.CharField(
        source='related_task.title', read_only=True)

    class Meta:
        model = TimelineEvent
        fields = [
            "id",
            "event_type",
            "description",
            "user",
            "company_name",
            "contact_name",
            "deal_name",
            "task_title",
            "created_at",
        ]

    def get_contact_name(self, obj):
        if obj.related_contact:
            c = obj.related_contact
            return f"{c.first_name} {c.last_name} ({c.email})"

        task = getattr(obj, 'related_task', None)
        if task and task.assigned_to:
            u = task.assigned_to
            return f"{u.first_name} {u.last_name} ({u.email})"

        return None

class NotificationSerializer(serializers.ModelSerializer):
    timeline_event = TimelineEventSerializer(read_only=True)
    target_type = serializers.SerializerMethodField()
    target_id = serializers.SerializerMethodField()
    class Meta:
        model = Notification
        fields = [
            'id',
            'timeline_event',
            'read',
            'created_at',
            'target_type',
            'target_id',
        ]

    def get_target_type(self, obj):
        e = obj.timeline_event
        if not e:
            return None
        if e.related_company:
            return "company"
        if e.related_contact:
            return "contact"
        if e.related_deal:
            return "deal"
        if e.related_task:
            return "task"
        return None

    def get_target_id(self, obj):
        e = obj.timeline_event
        if not e:
            return None
        if e.related_company:
            return e.related_company.id
        if e.related_contact:
            return e.related_contact.id
        if e.related_deal:
            return e.related_deal.id
        if e.related_task:
            return e.related_task.id
        return None
