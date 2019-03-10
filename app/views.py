# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from system.system import system_main
from django.http import JsonResponse
from django.views.decorators.gzip import gzip_page


def home(request):
    return render(request, 'home.html')


def autonomous_car(request):
    return render(request, 'autonomous_car.html')


@gzip_page
def images(request):
    response = JsonResponse(system_main())
    return response
