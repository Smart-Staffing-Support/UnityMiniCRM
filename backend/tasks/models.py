from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='companies')

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    position = models.CharField(max_length=100, blank=True)
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='contacts')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='contacts')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Deal(models.Model):
    STAGE_CHOICES = [
        ('lead', 'Lead'),
        ('qualified', 'Qualified'),
        ('proposal', 'Proposal'),
        ('negotiation', 'Negotiation'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]

    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    stage = models.CharField(
        max_length=20, choices=STAGE_CHOICES, default='lead')
    probability = models.IntegerField(
        default=0, help_text='Win probability (0-100%)')
    expected_close_date = models.DateField(null=True, blank=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='deals')
    contact = models.ForeignKey(
        Contact, on_delete=models.SET_NULL, null=True, blank=True, related_name='deals')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='deals')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateTimeField(null=True, blank=True)
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    deal = models.ForeignKey(
        Deal, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='created_tasks')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class TimelineEvent(models.Model):
    EVENT_TYPES = [
        ("company_created", "Company Created"),
        ("company_updated", "Company Updated"),
        ("contact_created", "Contact Created"),
        ("contact_updated", "Contact Updated"),
        ("deal_created", "Deal Created"),
        ("deal_stage_changed", "Deal Stage Changed"),
        ("task_created", "Task Created"),
        ("task_completed", "Task Completed"),
    ]

    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    related_company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True)
    related_contact = models.ForeignKey(
        Contact, on_delete=models.SET_NULL, null=True, blank=True)
    related_deal = models.ForeignKey(
        Deal, on_delete=models.SET_NULL, null=True, blank=True)
    related_task = models.ForeignKey(
        Task, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.event_type} - {self.created_at}"
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    timeline_event = models.ForeignKey(
        'TimelineEvent', on_delete=models.CASCADE, related_name="notifications"
    )
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.username} - {self.timeline_event.event_type}"
