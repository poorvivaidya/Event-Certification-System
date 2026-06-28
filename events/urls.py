from django.urls import path
from . import views

urlpatterns = [
    path("csrf-test/", views.csrf_test),
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
    path(
        "verify/<uuid:certificate_id>/",
        views.verify_certificate,
        name="verify_certificate"
    ),
]
