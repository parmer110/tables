from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms

def index(request):
    return render (request, "common/index.html")
