import json
import os
from urllib import request, response
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.http import require_POST, require_GET
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from events.validators import validate_student_id
from .forms import ParticipantRegistrationForm
from .models import Event, Participant, Feedback
from .forms import ParticipantRegistrationForm, FeedbackForm, BulkUploadForm

from .utils import (
    generate_certificate,
    send_registration_email,
    process_bulk_csv,
)

from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import StudentProfile

def signup(request):

    if request.method == "POST":

        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        student_id = request.POST.get("student_id")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        try:
            validate_student_id(student_id)
        except ValidationError as e:
            messages.error(request, e.message)
            return redirect("signup")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("signup")

        if StudentProfile.objects.filter(student_id=student_id).exists():
            messages.error(request, "Student ID already exists.")
            return redirect("signup")

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        StudentProfile.objects.create(
            user=user,
            student_id=student_id
        )

        messages.success(
            request,
            "Account created successfully. Please login."
        )

        return redirect("login")

    return render(request, "events/signup.html")

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect


def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)
            if not request.POST.get("remember_me"):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(60 * 60 * 24 * 30)   # 30 days

            # Admin Login
            if user.is_staff:
                return redirect("admin_dashboard")

            # Student Login
            return redirect("student_dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "events/login.html"
    )


def user_logout(request):

    logout(request)

    return redirect("index")
# ─────────────────────────────────────────────────────────────────────────────
# HOME / INDEX
# ─────────────────────────────────────────────────────────────────────────────

def index(request):
    """Landing page with links to registration and dashboard."""
    events = Event.objects.all()
    total_participants = Participant.objects.count()
    return render(request, 'events/index.html', {
        'events': events,
        'total_participants': total_participants,
    })

@login_required
def student_dashboard(request):

    participant = Participant.objects.filter(
        student__user=request.user
    ).first()
    participants = Participant.objects.filter(
    student=request.user.studentprofile
).select_related("event")

    context = {
        "participant": participant,
        "participants": participants
    }

    return render(
    request,
    "events/student_dashboard.html",
    {
        "participants": participants
    }
)


from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Participant

@require_POST
def toggle_transaction(request, pk):
    participant = Participant.objects.get(pk=pk)

    # Toggle True/False
    participant.transaction_verified = not participant.transaction_verified
    participant.save()

    return JsonResponse({
        "transaction_verified": participant.transaction_verified
    })

from django.contrib.auth.decorators import login_required
from .forms import ParticipantRegistrationForm
from .models import Participant
from .utils import send_registration_email

@login_required
def register_event(request):

    # Get event from URL (if user clicked Register on an event card)
    event_id = request.GET.get("event")

    selected_event = None

    if event_id:
        selected_event = get_object_or_404(
            Event,
            pk=event_id
        )

    form = ParticipantRegistrationForm(
        request.POST or None,
        request.FILES or None,
        initial={"event": selected_event} if selected_event else None
    )

    # If an event is already selected, remove the dropdown
    if selected_event:
        form.fields.pop("event")

    if request.method == "POST":

        if form.is_valid():

            participant = form.save(commit=False)

            # Logged-in student
            participant.student = request.user.studentprofile

            # If user came from an event card, fix the event
            if selected_event:
                participant.event = selected_event
            if Participant.objects.filter(
                student=request.user.studentprofile,
                event=participant.event
            ).exists():

                messages.error(
                    request,
                    "You have already registered for this event."
            )

                return redirect("student_dashboard")
            participant.student = request.user.studentprofile
            participant.save()

            send_registration_email(participant)

            messages.success(
                request,
                "Event registration submitted successfully. Please wait for admin approval."
            )

            return redirect("student_dashboard")

    return render(
        request,
        "events/register_event.html",
        {
            "form": form,
            "selected_event": selected_event,
        }
    )
# ─────────────────────────────────────────────────────────────────────────────
# ADMIN DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from .models import Event, Participant, StudentProfile

@staff_member_required
def admin_dashboard(request):

    event_id = request.GET.get("event")

    events = Event.objects.all()

    students = StudentProfile.objects.select_related("user").all()

    participants = Participant.objects.select_related(
        "student",
        "student__user",
        "event"
    )

    if event_id:
        participants = participants.filter(event_id=event_id)

    total_students = students.count()

    total_events = events.count()

    total_participants = participants.count()

    pending_payments = participants.filter(
        transaction_verified=False
    ).count()

    approved_payments = participants.filter(
        transaction_verified=True
    ).count()

    attended = participants.filter(
        attendance=True
    ).count()

    certificates = participants.filter(
        attendance=True,
        feedback_submitted=True,
        transaction_verified=True
    ).count()

    bulk_form = BulkUploadForm()

    context = {

        "students": students,

        "participants": participants,

        "events": events,

        "selected_event": event_id,

        "total_students": total_students,

        "total_events": total_events,

        "total_participants": total_participants,

        "pending_payments": pending_payments,

        "approved_payments": approved_payments,

        "attended": attended,

        "certificates": certificates,

        "bulk_form": bulk_form,

    }

    return render(
        request,
        "events/admin_dashboard.html",
        context
    )


# ─────────────────────────────────────────────────────────────────────────────
# AJAX: ATTENDANCE TOGGLE
# ─────────────────────────────────────────────────────────────────────────────

@require_POST
def toggle_attendance(request, participant_id):
    """AJAX endpoint to toggle attendance. Returns JSON."""
    try:
        participant = get_object_or_404(
    Participant,
    pk=participant_id
)
        participant.attendance = not participant.attendance
        participant.save(update_fields=['attendance'])

        return JsonResponse({
            'success': True,
            'attendance': participant.attendance,
            'participant_id': participant_id,
            'message': (
                f"Attendance marked for {participant.student.user.get_full_name()}"
                if participant.attendance
                else f"Attendance removed for {participant.student.user.get_full_name()}"
            ),
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)



# ─────────────────────────────────────────────────────────────────────────────
# CERTIFICATE DOWNLOAD
# ─────────────────────────────────────────────────────────────────────────────
@login_required
def download_certificate(request, participant_id):
  
    participant = get_object_or_404(
    Participant,
    pk=participant_id
)

    if not participant.can_get_certificate:
        missing = []
        if not participant.attendance:
            missing.append("Attendance not marked")
        if not participant.feedback_submitted:
            missing.append("Feedback not submitted")
        if not participant.transaction_verified:
            missing.append("Transaction not verified")

        return render(
            request,
            'events/certificate_denied.html',
            {'participant': participant, 'missing': missing},
            status=403,
        )

    # Build the verification URL
    verify_url = request.build_absolute_uri(
        f'/verify/{participant.certificate_id}/'
    )

    import os

    file_path = generate_certificate(participant)

    if not os.path.exists(file_path):
        raise Http404("Certificate not found")

    with open(file_path, 'rb') as f:
       response = HttpResponse(f.read(), content_type='application/pdf')

    response['Content-Disposition'] = (
    f'attachment; filename="certificate_{participant.student.student_id}.pdf"'
)

    return response


# ─────────────────────────────────────────────────────────────────────────────
# CERTIFICATE VERIFICATION PAGE
# ─────────────────────────────────────────────────────────────────────────────
@login_required
def verify_certificate(request, certificate_id):
    """Public verification page for a certificate."""
    try:
        participant = get_object_or_404(Participant, certificate_id=certificate_id)
        verified = participant.can_get_certificate
    except Exception:
        participant = None
        verified = False

    return render(request, 'events/verify.html', {
        'participant': participant,
        'verified': verified,
        'certificate_id': certificate_id,
    })


# ─────────────────────────────────────────────────────────────────────────────
# API: REAL-TIME STATS (AJAX POLLING)
# ─────────────────────────────────────────────────────────────────────────────

@require_GET
def api_stats(request):
    """JSON endpoint for real-time dashboard statistics."""
    event_id = request.GET.get('event')

    qs = Participant.objects.all()
    if event_id:
        qs = qs.filter(event_id=event_id)

    total = qs.count()
    attended = qs.filter(attendance=True).count()
    feedback_done = qs.filter(feedback_submitted=True).count()
    verified = qs.filter(transaction_verified=True).count()

    # Certified = all three conditions True
    certified = qs.filter(
        attendance=True,
        feedback_submitted=True,
        transaction_verified=True
    ).count()

    return JsonResponse({
        'total': total,
        'attended': attended,
        'feedback_done': feedback_done,
        'verified': verified,
        'certified': certified,
    })


# ─────────────────────────────────────────────────────────────────────────────
# BULK CSV UPLOAD
# ─────────────────────────────────────────────────────────────────────────────

@require_POST
def bulk_upload(request):
    """Admin feature: bulk-create participants from a CSV file."""
    form = BulkUploadForm(request.POST, request.FILES)

    if form.is_valid():
        csv_file = request.FILES['csv_file']
        created_count, errors = process_bulk_csv(csv_file)

        if created_count > 0:
            messages.success(
                request,
                f"✅ Successfully imported {created_count} participant(s)."
            )
        if errors:
            for err in errors:
                messages.warning(request, err)
        if created_count == 0 and not errors:
            messages.info(request, "No new participants were imported.")
    else:
        messages.error(request, "Please upload a valid CSV file.")

    return redirect('admin_dashboard')


# ─────────────────────────────────────────────────────────────────────────────
# PARTICIPANT DETAIL (helper for feedback link from dashboard)
# ─────────────────────────────────────────────────────────────────────────────

def participant_detail(request, participant_id):
    """Simple detail page for a participant."""
    participant = get_object_or_404(Participant, pk=participant_id)
    return render(request, 'events/participant_detail.html', {
        'participant': participant,
    })
from django.shortcuts import render, get_object_or_404, redirect
from .models import Participant
from .forms import FeedbackForm
@login_required
def feedback(request, pk):
    participant = get_object_or_404(Participant, pk=pk)

    # Prevent duplicate feedback
    if participant.feedback_submitted:
        return render(request, "events/feedback.html", {
            "participant": participant,
            "already_submitted": True
        })

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():

            feedback = form.save(commit=False)
            feedback.participant = participant
            feedback.save()

            participant.feedback_submitted = True
            participant.save()

            messages.success(
    request,
    "Feedback submitted successfully."
            )

            return redirect("student_dashboard")
            

    else:
        form = FeedbackForm()

    return render(request, "events/feedback.html", {
        "form": form,
        "participant": participant
    })
