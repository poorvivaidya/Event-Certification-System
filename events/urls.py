from django.urls import path
from . import views

urlpatterns = [

    # Home
    path("", views.index, name="index"),

    # Authentication
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

    # Student
    path(
        "student-dashboard/",
        views.student_dashboard,
        name="student_dashboard"
    ),

    path(
        "register-event/",
        views.register_event,
        name="register_event"
    ),

    path(
        "feedback/<int:pk>/",
        views.feedback,
        name="feedback"
    ),

    path(
        "certificate/<int:participant_id>/",
        views.download_certificate,
        name="download_certificate"
    ),

    # Admin
    path(
        "dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    path(
        "toggle-attendance/<int:participant_id>/",
        views.toggle_attendance,
        name="toggle_attendance"
    ),

    path(
        "toggle-transaction/<int:pk>/",
        views.toggle_transaction,
        name="toggle_transaction"
    ),

    path(
        "bulk-upload/",
        views.bulk_upload,
        name="bulk_upload"
    ),

    path(
        "participant/<int:participant_id>/",
        views.participant_detail,
        name="participant_detail"
    ),

    path(
        "verify/<uuid:certificate_id>/",
        views.verify_certificate,
        name="verify_certificate"
    ),

    path(
        "api/stats/",
        views.api_stats,
        name="api_stats"
    ),

]