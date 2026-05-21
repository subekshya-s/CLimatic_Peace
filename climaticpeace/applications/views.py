from django.shortcuts import render, redirect
from .forms import ApplicationForm
from .models import Application
import requests
import os
import logging

logger = logging.getLogger(__name__)


def sync_to_sheetdb(application):
    try:
        api_url = os.environ.get('SHEETDB_API_URL')

        if not api_url:
            logger.warning("SHEETDB_API_URL not set — skipping sync.")
            return False

        row = {
            "Full Name":          application.full_name,
            "Email":              application.email,
            "Phone":              application.phone,
            "Age":                application.age,
            "Country":            application.country,
            "Faith Background":   application.get_faith_background_display() or "Prefer not to say",
            "Education":          application.get_education_level_display(),
            "Preferred Location": application.get_preferred_location_display() or "Not specified",
            "NGO Experience":     application.ngo_experience,
            "Why Join Essay":     application.why_join_essay,
            "CV Filename":        application.cv.name if application.cv else "",
            "Submitted At":       application.submitted_at.strftime("%Y-%m-%d %H:%M:%S UTC"),
        }

        response = requests.post(
            api_url,
            json={"data": row},
            timeout=10
        )

        if response.status_code == 201:
            Application.objects.filter(pk=application.pk).update(synced_to_sheets=True)
            logger.info(f"Synced {application.email} to SheetDB.")
            return True
        else:
            logger.error(f"SheetDB returned {response.status_code}: {response.text}")
            return False

    except Exception as e:
        logger.error(f"SheetDB sync failed: {e}")
        return False


def index(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save()
            sync_to_sheetdb(application)
            return redirect('success')
        else:
            return render(request, 'index.html', {'form': form})
    else:
        form = ApplicationForm()
        return render(request, 'index.html', {'form': form})


def success(request):
    return render(request, 'success.html')