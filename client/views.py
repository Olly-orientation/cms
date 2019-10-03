from django.shortcuts import render

# Create your views here.
def index(request):
  return render(request,"client/clientIndex.html")

def detail(request):
  return render(request,"client/articleDetail.html")

def type(request):
  return render(request,"client/articleType.html")