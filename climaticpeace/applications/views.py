from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ApplicationForm
from .models import Application

def index(request):

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('success')   
            

        else:
            return render(request, 'index.html', {'form': form})
            

    else:
        form = ApplicationForm()
        return render(request, 'index.html', {'form': form})

def success(request):         
    return render(request, 'success.html')