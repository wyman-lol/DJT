from django.shortcuts import render

# Create your views here.

def index_view(request):
    return render(request, 'course/index.html')

def course(request):
    return render(request, 'course/course.html')