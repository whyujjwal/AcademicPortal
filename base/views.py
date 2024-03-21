from django.shortcuts import render
from django.http import HttpResponse


def Home(response):
    return HttpResponse('Homepage')

def Rooms(response):
    return HttpResponse('Homepage')