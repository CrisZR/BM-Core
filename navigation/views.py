from django.shortcuts import render


# Create your views here.
def navMobile(request):
    return render(request, "navigation/nav_mobile.html")
