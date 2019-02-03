# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from system.system import system_main


def home(request):
    return render(request, 'home.html', {"img": "lena_color.png"})


def camera(request):
    data = system_main()
    return render(request, 'camera.html', data)


