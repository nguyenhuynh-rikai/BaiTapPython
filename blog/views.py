import datetime

from django.shortcuts import render
from django.http import HttpResponse

def hello_world(request):
    now = datetime.datetime.now()
    html = f"<html><body><h1>Bây giờ là: {now}</h1></body></html>"
    return HttpResponse(html)
# Create your views here.
