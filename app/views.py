# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from system.system import system_main
from django.http import JsonResponse, HttpResponse
from django.views.decorators.gzip import gzip_page
from system.picar_v.commands_by_request import commands_to_picar


def home(request):
    return render(request, 'home.html')


def autonomous_car(request):
    return render(request, 'autonomous_car.html')


@gzip_page
def images(request):
    response = JsonResponse(system_main())
    return response


def commands_by_request(request):
    commands_to_picar(request)
    return HttpResponse('OK')
