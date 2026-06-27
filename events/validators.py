import os
from django.core.exceptions import ValidationError
import re
from django.core.exceptions import ValidationError


def validate_student_id(student_id):
    """
    Format:
    1 digit
    2 letters
    2 digits
    2 letters
    2 digits

    Example:
    1AB23CD45
    """

    pattern = r'^[0-9][A-Za-z]{2}[0-9]{2}[A-Za-z]{2}[0-9]{2}$'

    if not re.match(pattern, student_id):
        raise ValidationError(
            "Student ID must follow the format: 1AB23CD45"
        )


ALLOWED_EXTENSIONS = ['.pdf', '.png', '.jpg', '.jpeg']
MAX_FILE_SIZE_MB = 2
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


def validate_receipt_file(value):
    """
    Validates that the uploaded receipt:
    - Is a PDF, PNG, or JPG/JPEG
    - Does not exceed 2MB
    """
    # Check extension
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            f"Unsupported file type '{ext}'. "
            f"Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Check file size
    if hasattr(value, 'size') and value.size > MAX_FILE_SIZE_BYTES:
        size_mb = value.size / (1024 * 1024)
        raise ValidationError(
            f"File size ({size_mb:.1f} MB) exceeds the maximum allowed size of {MAX_FILE_SIZE_MB} MB."
        )
