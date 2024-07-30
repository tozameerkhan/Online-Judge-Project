from django.shortcuts import render



def welcomeapp(request):
    return render(request, 'welcomepages.html')

