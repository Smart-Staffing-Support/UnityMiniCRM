from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    name = models.CharField()

    industry = models.CharField(blank=True)
    website = models.URLField(blank=True)
    phone = models.CharField(blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )

    class Meta:
        ordering = ["-created_at"]


class Contact(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()
    email = models.EmailField(unique=True)

    phone = models.CharField(blank=True)
    position = models.CharField(blank=True)
    notes = models.TextField(blank=True)

    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="contacts",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )

    class Meta:
        ordering = ["-created_at"]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Deal(models.Model):
    class Stage(models.TextChoices):
        LEAD = "lead"
        QUALIFIED = "qualified"
        PROPOSAL = "proposal"
        NEGOTIATION = "negotiation"
        WON = "won"
        LOST = "lost"

    title = models.CharField()
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    stage = models.CharField(choices=Stage, default=Stage.LEAD)
    probability = models.IntegerField(default=0)
    expected_close_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="deals"
    )
    contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="deals",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="+"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Task(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending"
        IN_PROGRESS = "in_progress"
        COMPLETED = "completed"

    class Priority(models.TextChoices):
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"

    title = models.CharField()

    description = models.TextField(blank=True)
    status = models.CharField(choices=Status, default=Status.PENDING)
    priority = models.CharField(choices=Priority, default=Priority.MEDIUM)
    due_date = models.DateTimeField(blank=True, null=True)

    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name="tasks"
    )
    deal = models.ForeignKey(
        Deal, on_delete=models.CASCADE, related_name="tasks"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )

    class Meta:
        ordering = ["-created_at"]
