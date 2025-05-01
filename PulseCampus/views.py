from django.shortcuts import HttpResponse

def homepage(request):
    return HttpResponse("Hello World!")