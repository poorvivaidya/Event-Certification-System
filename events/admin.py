from django.contrib import admin
from .models import Event, Participant, Feedback, StudentProfile


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'date']
    search_fields = ['name']

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):

    list_display = [
        "student_id",
        "user"
    ]

    search_fields = [
        "student_id",
        "user__username",
        "user__email"
    ]

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):

    list_display = [
        "student",
        "event",
        "transaction_verified",
        "attendance",
        "certificate_type",
    ]

    list_filter = [
        "event",
        "transaction_verified",
        "attendance",
        "certificate_type",
    ]

    search_fields = [
        "student__student_id",
        "student__user__first_name",
        "student__user__last_name",
        "event__name",
    ]

    readonly_fields = [
        'certificate_id',
        'registered_at'
    ]

    list_editable = [
        'certificate_type',
        'transaction_verified',
        'attendance'
    ]



@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):

    list_display = [
        'participant',
        'rating',
        'submitted_at'
    ]

    list_filter = [
        'rating'
    ]

    search_fields = [
        'participant__student__student_id',
        'participant__student__user__username'
    ]