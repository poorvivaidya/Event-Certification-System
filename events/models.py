import uuid
from django.db import models
from django.contrib.auth.models import User
from .validators import validate_receipt_file


class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    location = models.CharField(
        max_length=200,
        default="SJB Institute of Technology"
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    student_id = models.CharField(
        max_length=20,
        unique=True
    )

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"


class Participant(models.Model):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='participants'
    )

    transaction_id = models.CharField(
        max_length=100,
        unique=True
    )

    receipt = models.FileField(
        upload_to='receipts/',
        validators=[validate_receipt_file]
    )

    # Admin Approval
    transaction_verified = models.BooleanField(
        default=False
    )

    # Admin Attendance
    attendance = models.BooleanField(
        default=False
    )

    # Student Feedback
    feedback_submitted = models.BooleanField(
        default=False
    )

    # Certificate Tracking
    certificate_generated = models.BooleanField(
        default=False
    )

    certificate_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    registered_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-registered_at']

    def __str__(self):
        return (
            f"{self.student.user.get_full_name()} - "
            f"{self.event.name}"
        )

    @property
    def can_get_certificate(self):
        return (
            self.attendance
            and self.transaction_verified
            and self.feedback_submitted
        )


class Feedback(models.Model):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ]

    participant = models.OneToOneField(
        Participant,
        on_delete=models.CASCADE,
        related_name='feedback'
    )

    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES
    )

    comments = models.TextField(
        blank=True
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.participant.student.user.get_full_name()} "
            f"({self.rating}/5)"
        )