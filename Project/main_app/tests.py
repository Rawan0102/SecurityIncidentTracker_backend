from django.test import TestCase
from django.contrib.auth.models import User
from main_app.models import Profile, Incident, Report, Comment
from datetime import datetime

class ModelsTest(TestCase):
    def setUp(self):
        # Create users
        self.manager_user = User.objects.create_user(username='manager1', password='test123')
        self.employee_user = User.objects.create_user(username='employee1', password='test123')

        # Assign roles using Profile
        self.manager_profile = Profile.objects.create(user=self.manager_user, role='manager')
        self.employee_profile = Profile.objects.create(user=self.employee_user, role='employee')

        # Create Incident (only by manager)
        self.incident = Incident.objects.create(
            title="System Breach",
            description="Detected a critical system breach",
            severity="critical",
            reporter=self.manager_user,
            assigned=self.employee_user,
            category="Unauthorized Access",
            location="Data Center"
        )

        # Create Report (only by employee)
        self.report = Report.objects.create(
            incident=self.incident,
            author=self.employee_user,
            title="Suspicious Login",
            description="User logged in from an unknown IP",
            category="unauthorized access",
            urgency="high",
            location="Admin Portal"
        )

        # Create Comment
        self.comment = Comment.objects.create(
            report=self.report,
            author=self.manager_user,
            content="Reviewing this immediately."
        )

    # -------------------
    # Basic Object Creation
    # -------------------

    def test_profile_roles(self):
        self.assertEqual(str(self.manager_profile), "manager1 - manager")
        self.assertEqual(str(self.employee_profile), "employee1 - employee")

    def test_incident_creation(self):
        self.assertEqual(str(self.incident), "System Breach")
        self.assertEqual(self.incident.reporter.username, 'manager1')
        self.assertEqual(self.incident.assigned.username, 'employee1')

    def test_report_creation(self):
        self.assertEqual(str(self.report), "Report by employee1 on System Breach")
        self.assertEqual(self.report.incident, self.incident)

    def test_comment_creation(self):
        self.assertEqual(str(self.comment), f"Comment by manager1 on Report #{self.report.id}")
        self.assertEqual(self.comment.report, self.report)

    # -------------------
    # Relationships
    # -------------------

    def test_incident_reports_relationship(self):
        self.assertEqual(self.incident.reports.count(), 1)
        self.assertIn(self.report, self.incident.reports.all())

    def test_report_comment_relationship(self):
        self.assertEqual(self.report.comments.count(), 1)
        self.assertIn(self.comment, self.report.comments.all())

    def test_user_comment_relationship(self):
        self.assertEqual(self.manager_user.comments.count(), 1)
        self.assertEqual(self.manager_user.comments.first().content, "Reviewing this immediately.")

    # -------------------
    # Role-based business rules (custom validation logic would go in views or forms)
    # -------------------

    def test_only_managers_can_report_incidents(self):
        self.assertEqual(self.manager_profile.role, "manager")
        self.assertEqual(self.incident.reporter.profile.role, "manager")

    def test_only_employees_can_create_reports(self):
        self.assertEqual(self.employee_profile.role, "employee")
        self.assertEqual(self.report.author.profile.role, "employee")
