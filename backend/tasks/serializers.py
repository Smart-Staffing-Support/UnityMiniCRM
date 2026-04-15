from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Company, Contact, Deal, Task, Interaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class CompanySerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
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
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    interactions_count = serializers.SerializerMethodField()
    last_interaction_date = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'phone',
                  'position', 'company', 'company_name', 'notes', 'created_at',
                  'updated_at', 'created_by', 'created_by_name',
                  'interactions_count', 'last_interaction_date']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by', 'full_name',
                            'interactions_count', 'last_interaction_date']

    def get_interactions_count(self, obj):
        return obj.interactions.count()

    def get_last_interaction_date(self, obj):
        latest = obj.interactions.order_by('-interaction_date').first()
        return latest.interaction_date if latest else None


class DealSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    contact_name = serializers.CharField(source='contact.full_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Deal
        fields = ['id', 'title', 'amount', 'stage', 'probability', 'expected_close_date',
                  'company', 'company_name', 'contact', 'contact_name', 'notes',
                  'created_at', 'updated_at', 'created_by', 'created_by_name']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']


class TaskSerializer(serializers.ModelSerializer):
    contact_name = serializers.CharField(source='contact.full_name', read_only=True)
    deal_title = serializers.CharField(source='deal.title', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'due_date',
                  'contact', 'contact_name', 'deal', 'deal_title', 'assigned_to',
                  'assigned_to_name', 'created_at', 'updated_at', 'created_by',
                  'created_by_name']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']


class InteractionSerializer(serializers.ModelSerializer):
    contact_name = serializers.CharField(source='contact.full_name', read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    deal_title = serializers.CharField(source='deal.title', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    is_follow_up_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Interaction
        fields = [
            'id',
            'contact', 'contact_name',
            'company', 'company_name',
            'deal', 'deal_title',
            'interaction_type',
            'subject',
            'notes',
            'interaction_date',
            'follow_up_date',
            'is_follow_up_overdue',
            'created_at',
            'updated_at',
            'created_by',
            'created_by_name',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by', 'is_follow_up_overdue']

    def validate(self, attrs):
        interaction_date = attrs.get('interaction_date', getattr(self.instance, 'interaction_date', None))
        follow_up_date = attrs.get('follow_up_date', getattr(self.instance, 'follow_up_date', None))
        contact = attrs.get('contact', getattr(self.instance, 'contact', None))
        company = attrs.get('company', getattr(self.instance, 'company', None))
        deal = attrs.get('deal', getattr(self.instance, 'deal', None))

        if not contact:
            raise serializers.ValidationError({'contact': 'A contact is required for every interaction.'})

        if follow_up_date and interaction_date and follow_up_date < interaction_date:
            raise serializers.ValidationError({
                'follow_up_date': 'Follow-up date cannot be earlier than the interaction date.'
            })

        if company and contact.company and company != contact.company:
            raise serializers.ValidationError({
                'company': 'Selected company must match the contact company.'
            })

        if deal:
            if company and deal.company != company:
                raise serializers.ValidationError({
                    'deal': 'Selected deal must belong to the selected company.'
                })
            if contact and deal.contact and deal.contact != contact:
                raise serializers.ValidationError({
                    'deal': 'Selected deal must belong to the selected contact.'
                })

        return attrs

    def get_is_follow_up_overdue(self, obj):
        return bool(obj.follow_up_date and obj.follow_up_date < timezone.now())