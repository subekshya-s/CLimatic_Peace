from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator



EDUCATION_CHOICES = [
    ('high_school',  'High School Diploma'),
    ('bachelor',     "Bachelor's Degree"),
    ('master',       "Master's Degree"),
    ('phd',          'PhD / Doctorate'),
    ('other',        'Other'),
]

FAITH_CHOICES = [
    ('',             'Prefer not to say'),
    ('islam',        'Islam'),
    ('christianity', 'Christianity'),
    ('judaism',      'Judaism'),
    ('hinduism',     'Hinduism'),
    ('buddhism',     'Buddhism'),
    ('other',        'Other'),
]

COUNTRY_CHOICES = [
    ('lebanon',   'Lebanon'),
    ('jordan',    'Jordan'),
    ('tunisia',   'Tunisia'),
    ('albania',   'Albania'),
    ('indonesia', 'Indonesia'),
    ('other',     'Other'),
]


class Application(models.Model):

    # ── PERSONAL INFO ──────────────────────────
    full_name   = models.CharField(max_length=200)
    email       = models.EmailField(unique=True)
    phone       = models.CharField(max_length=30)
    age         = models.IntegerField(
                    validators=[
                        MinValueValidator(18),  # minimum age
                        MaxValueValidator(30),  # maximum age
                    ]
                  )
    country     = models.CharField(max_length=100)

    # ── BACKGROUND ─────────────────────────────
    faith_background = models.CharField(
                         max_length=100,
                         blank=True,       
                         choices=FAITH_CHOICES,
                         default=''
                       )
    education_level  = models.CharField(
                         max_length=50,
                         choices=EDUCATION_CHOICES
                       )
    ngo_experience   = models.TextField(
                         help_text="Describe any NGO or volunteer experience"
                       )
    # ── ESSAY ──────────────────────────────────
    why_join_essay = models.TextField(
                       help_text="Why do you want to join? (~200 words)"
                     )

    # ── PREFERRED CAMP LOCATION ────────────────
    preferred_location = models.CharField(
                           max_length=50,
                           choices=COUNTRY_CHOICES,
                           blank=True
                         )

    # ── CV UPLOAD ──────────────────────────────
    cv = models.FileField(
           upload_to='cvs/',
           # files saved to: media/cvs/filename.pdf
           help_text="PDF or Word document, max 5MB"
         )

    # ── META (automatic) ───────────────────────
    submitted_at     = models.DateTimeField(auto_now_add=True)

    synced_to_sheets = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']
        

    def __str__(self):
        return f"{self.full_name} ({self.email})"