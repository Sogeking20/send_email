from django.shortcuts import render
from django.http import JsonResponse
from .models import EmailMessage

def index(request):
    return render(request, 'emails/index.html')

def get_messages(request):
    messages = list(EmailMessage.objects.values())
    return JsonResponse({'messages': messages})