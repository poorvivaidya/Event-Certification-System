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
        'student',
        'event',
        'transaction_verified',
        'attendance',
        'feedback_submitted',
        'certificate_generated',
        'registered_at'
    ]

    list_filter = [
        'event',
        'attendance',
        'transaction_verified',
        'feedback_submitted'
    ]

    search_fields = [
        'student__student_id',
        'student__user__username',
        'student__user__email'
    ]

    readonly_fields = [
        'certificate_id',
        'registered_at'
    ]

    list_editable = [
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