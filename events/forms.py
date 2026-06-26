
from django import forms
from django.contrib.auth.models import User
from .models import (
    Participant,
    Feedback,
    Event,
    StudentProfile
)
from .validators import validate_receipt_file


# ==========================================
# STUDENT REGISTRATION
# ==========================================

class StudentRegistrationForm(forms.ModelForm):
    student_id = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1JB23CS001'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'email'
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Email already exists."
            )

        return email

    def clean_student_id(self):
        student_id = self.cleaned_data['student_id']

        if StudentProfile.objects.filter(
            student_id=student_id
        ).exists():
            raise forms.ValidationError(
                "Student ID already exists."
            )

        return student_id

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match."
            )

        return cleaned_data


# ==========================================
# EVENT REGISTRATION
# ==========================================

class ParticipantRegistrationForm(forms.ModelForm):

    class Meta:
        model = Participant

        fields = [
            'event',
            'transaction_id',
            'receipt'
        ]

        widgets = {
            'event': forms.Select(attrs={
                'class': 'form-select'
            }),

            'transaction_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Transaction ID'
            }),

            'receipt': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.png,.jpg,.jpeg'
            }),
        }

    def clean_receipt(self):
        receipt = self.cleaned_data.get('receipt')

        if not receipt:
            raise forms.ValidationError(
                "Payment receipt is required."
            )

        validate_receipt_file(receipt)

        return receipt

    def clean_transaction_id(self):
        transaction_id = self.cleaned_data.get(
            'transaction_id'
        )

        if Participant.objects.filter(
            transaction_id=transaction_id
        ).exists():
            raise forms.ValidationError(
                "Transaction ID already exists."
            )

        return transaction_id


# ==========================================
# FEEDBACK
# ==========================================

class FeedbackForm(forms.ModelForm):

    rating = forms.ChoiceField(
        choices=[(i, '⭐' * i) for i in range(1, 6)],
        widget=forms.RadioSelect(
            attrs={'class': 'form-check-input'}
        )
    )

    class Meta:
        model = Feedback

        fields = [
            'rating',
            'comments'
        ]

        widgets = {
            'comments': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder':
                'Share your experience...'
            })
        }

    def clean_rating(self):
        rating = int(self.cleaned_data['rating'])

        if not (1 <= rating <= 5):
            raise forms.ValidationError(
                "Rating must be between 1 and 5."
            )

        return rating


# ==========================================
# ADMIN EVENT FORM
# ==========================================

class EventForm(forms.ModelForm):

    class Meta:
        model = Event

        fields = [
            'name',
            'date',
            'location'
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }


# ==========================================
# BULK CSV UPLOAD
# ==========================================

class BulkUploadForm(forms.Form):

    csv_file = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
                'accept': '.csv'
            }
        )
    )
