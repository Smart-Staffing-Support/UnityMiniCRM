from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Company, Contact, Deal, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]
        read_only_fields = ["username"]


class CompanySerializer(serializers.ModelSerializer):
    created_by = UserSerializer()

    contacts_count = serializers.SerializerMethodField()
    deals_count = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "industry",
            "website",
            "phone",
            "email",
            "address",
            "notes",
            "created_at",
            "updated_at",
            "created_by",
            "contacts_count",
            "deals_count",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "created_by"]

    def get_contacts_count(self, obj):
        return obj.contacts.count()

    def get_deals_count(self, obj):
        return obj.deals.count()


class ContactSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()

    full_name = serializers.ReadOnlyField()
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = Contact
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "phone",
            "position",
            "company",
            "company_name",
            "notes",
            "created_at",
            "updated_at",
            "created_by",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "created_by",
            "full_name",
        ]


class DealSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()

    company_name = serializers.CharField(source="company.name", read_only=True)
    contact_name = serializers.CharField(
        source="contact.full_name", read_only=True
    )

    class Meta:
        model = Deal
        fields = [
            "id",
            "title",
            "amount",
            "stage",
            "probability",
            "expected_close_date",
            "company",
            "company_name",
            "contact",
            "contact_name",
            "notes",
            "created_at",
            "updated_at",
            "created_by",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "created_by"]


class TaskSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()

    contact_name = serializers.CharField(
        source="contact.full_name", read_only=True
    )
    deal_title = serializers.CharField(source="deal.title", read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "due_date",
            "contact",
            "contact_name",
            "deal",
            "deal_title",
            "assigned_to",
            "assigned_to_name",
            "created_at",
            "updated_at",
            "created_by",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "created_by"]
