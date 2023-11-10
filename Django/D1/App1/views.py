from django.shortcuts import render
from django.http import HttpResponse

def test_case1(request):
    return HttpResponse("<h1><hr>This is First Django Project<hr></h1>")

def test_case2(request):
    return HttpResponse("<table border=1> <tr><td> Second Service</td></tr></table>")

# Create your views here.
