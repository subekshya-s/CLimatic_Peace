from django import forms
from .models import Application, EDUCATION_CHOICES, FAITH_CHOICES


class ApplicationForm(forms.ModelForm):
    """
    ModelForm automatically creates form fields
    from the Application model.
    We just customize how they look and validate.
    """

    class Meta:
        model  = Application
        fields = [
            # The order here = order on the page
            'full_name',
            'email',
            'phone',
            'age',
            'country',
            'faith_background',
            'education_level',
            'preferred_location',
            'ngo_experience',
            'why_join_essay',
            'cv',
        ]

        # widgets = how each field LOOKS in HTML
        widgets = {
            'full_name': forms.TextInput(attrs={
                'placeholder': 'Enter your full name',
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'your@email.com',
                'class': 'form-control',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '+1 234 567 8900',
                'class': 'form-control',
            }),
            'age': forms.NumberInput(attrs={
                'placeholder': 'Must be between 18 and 30',
                'class': 'form-control',
                'min': 18,
                'max': 30,
            }),
            'country': forms.TextInput(attrs={
                'placeholder': 'Your country of residence',
                'class': 'form-control',
            }),
            'faith_background': forms.Select(attrs={
                'class': 'form-control',
            }),
            'education_level': forms.Select(attrs={
                'class': 'form-control',
            }),
            'preferred_location': forms.Select(attrs={
                'class': 'form-control',
            }),
            'ngo_experience': forms.Textarea(attrs={
                'placeholder': 'Tell us about your NGO or volunteer experience...',
                'class': 'form-control',
                'rows': 4,
            }),
            'why_join_essay': forms.Textarea(attrs={
                'placeholder': 'Why do you want to join Youth Are Green Faith Builders 2? (~200 words)',
                'class': 'form-control',
                'rows': 7,
                'id': 'essay-field',  # used by JS word counter
            }),
            'cv': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx',
            }),
        }

        # labels = the text shown above each field
        labels = {
            'full_name':           'Full Name',
            'email':               'Email Address',
            'phone':               'Phone Number',
            'age':                 'Age',
            'country':             'Country of Residence',
            'faith_background':    'Faith Background (Optional)',
            'education_level':     'Education Level',
            'preferred_location':  'Preferred Camp Location',
            'ngo_experience':      'NGO / Volunteer Experience',
            'why_join_essay':      'Why do you want to join?',
            'cv':                  'Upload Your CV',
        }

    # ── CUSTOM VALIDATION ───────────────────────────────────────
    # These are called automatically when form.is_valid() runs
    # Method name must be: clean_<fieldname>

    def clean_age(self):
        age = self.cleaned_data.get('age')
        # cleaned_data = data AFTER Django's basic validation

        if age is None:
            raise forms.ValidationError("Please enter your age.")

        if age < 18 or age > 30:
            raise forms.ValidationError(
                f"You must be between 18 and 30 to apply. You entered {age}."
            )
        return age  # always return the value at the end

    def clean_why_join_essay(self):
        essay = self.cleaned_data.get('why_join_essay', '')
        word_count = len(essay.split())

        if word_count < 50:
            raise forms.ValidationError(
                f"Your essay is too short ({word_count} words). "
                f"Please write at least 50 words."
            )
        if word_count > 300:
            raise forms.ValidationError(
                f"Your essay is too long ({word_count} words). "
                f"Please keep it under 300 words."
            )
        return essay

    def clean_cv(self):
        cv = self.cleaned_data.get('cv')

        if not cv:
            raise forms.ValidationError("Please upload your CV.")

        # Check file extension
        allowed_extensions = ['.pdf', '.doc', '.docx']
        file_ext = '.' + cv.name.split('.')[-1].lower()

        if file_ext not in allowed_extensions:
            raise forms.ValidationError(
                f"File type '{file_ext}' is not allowed. "
                f"Please upload a PDF or Word document."
            )

        # Check file size (5MB limit)
        if cv.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                "File is too large. Please keep your CV under 5MB."
            )

        return cv

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower()
        # force lowercase so Gmail and GMAIL are treated the same
        return email

  