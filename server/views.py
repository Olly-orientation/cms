from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"server/serverIndex.html")

def menu(request):
    return render(request,"server/menu.html")