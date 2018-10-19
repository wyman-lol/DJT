from django.shortcuts import render

# Create your views here.
def search(request):
    return render(request, 'doc/search.html')

def docDownload(request):
    return render(request, 'doc/docDownload.html')