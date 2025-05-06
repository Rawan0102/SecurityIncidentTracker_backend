from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    

class Incident(models.Model):
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    severity = models.CharField(
    max_length=10,
    choices=SEVERITY_CHOICES,
    default='low'
)

    title = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved = models.BooleanField(default=False)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_incidents')
    assigned = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_incidents')
    category = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
   

    def __str__(self):
        return self.title
    
class Report(models.Model):
    CATEGORY_CHOICES = [
        ('phishing', 'Phishing'),
        ('malware', 'Malware'),
        ('unauthorized access', 'Unauthorized Access'),
        ('data leak', 'Data Leak'),
        ('other', 'Other') 
    ]
    URGENCY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='reports')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='other')
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=200)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='low')


    def __str__(self):
        return f"Report by {self.author.username} on {self.incident.title}"

class Comment(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on Report #{self.report.id}"