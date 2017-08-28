# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import User, Travel
from django.shortcuts import render, redirect
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def register(request):
    result = User.objects.validate_registration(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Successfully registered!")
    return redirect('/travels')

def login(request):
    result = User.objects.validate_login(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Successfully logged in!")
    return redirect('/travels')

def travels(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'destinations': Travel.objects.filter(user=user),
        'other_destinations': Travel.objects.exclude(user=user)
    }

    return render(request, 'main/home.html', context)

def show(request, dest_id):
    context = {
        'travel': Travel.objects.get(id=dest_id),
        'travel_group': Travel.objects.filter(id=dest_id)
    }
    return render(request, 'main/show.html', context)


def add(request):
    #display add page
    return render(request, 'main/add.html')

def create(request):
    errors = Travel.objects.validate_travel(request.POST)
    if errors:
        for err in errors:
            messages.error(request, err)
        return redirect('/travels/add')
    else:
        Travel.objects.add_travel(request.POST, request.session['user_id'])

    return redirect('/travels')


def join(request, dest_id):
    Travel.objects.join_group(request, dest_id)
    return redirect('/travels/destination/'+ dest_id)

def logout(request):
    request.session.clear()
    return redirect('/')
