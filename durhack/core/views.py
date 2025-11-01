from django.shortcuts import render

# Create your views here.
def homePage(request):
    return render(request,'core/index.html')