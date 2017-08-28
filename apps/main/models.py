# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import bcrypt
from django.db import models
from datetime import datetime, date
from dateutil.parser import parse as parse_date

class UserManager(models.Manager):
    def validate_login(self, post_data):
        errors = []
        # check DB for post_data['username']
        if len(self.filter(username=post_data['username'])) > 0:
            # check this user's password
            user = self.filter(username=post_data['username'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('email/password incorrect')
        else:
            errors.append('email/password incorrect')

        if errors:
            return errors
        return user

    def validate_registration(self, post_data):
        errors = []

        if len(post_data['name']) < 3 or len(post_data['username']) < 2:
            errors.append("name fields must be at least 3 characters")

        if len(post_data['password']) < 8:
            errors.append("password must be at least 8 characters")

        # check if username exists in db
        if User.objects.filter(username=post_data['username']):
            errors.append("username already in use")

        if post_data['password'] != post_data['pw_confirm']:
            errors.append("passwords do not match")

        if not errors:
            hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

            new_user = self.create(
                name=post_data['name'],
                username=post_data['username'],
                password=hashed
            )
            return new_user
        return errors


class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    objects = UserManager()
    def __str__(self):
        return self.email

class TravelManager(models.Manager):
    def validate_travel(self, post_data):
        errors = []

        if len(post_data['destination'])<1:
            errors.append('enter a valid destination place')

        #check if dates are valid
        from_date = post_data['from_date']
        to_date = post_data['to_date']

        if from_date:
            from_date = parse_date(from_date).date()
            if from_date < date.today():
                errors.append('enter a future date for your trip')
        else:
            errors.append('enter a from date')

        if to_date:
            to_date = parse_date(to_date).date()
            if to_date < date.today():
                errors.append('enter a future date for your trip')

        if from_date and to_date:
            if from_date > to_date:
                errors.append('travel date has be before end of travel date')

        if errors:
             return errors

    def add_travel(self, clean_data, user_id):
        self.create(
            destination = clean_data['destination'],
            description = clean_data['description'],
            from_date = clean_data['from_date'],
            to_date = clean_data['to_date'],
            user = User.objects.get(id=user_id)
        )
        
    def join_group(self, request, dest_id):
        destination = Travel.objects.get(id=dest_id)
        user = User.objects.get(id=request.session['user_id'])
        destination.group.add(user)


class Travel(models.Model):
    destination = models.CharField(max_length=100)
    description = models.CharField(max_length = 250)
    from_date = models.DateField()
    to_date = models.DateField()
    created_at = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='travels')
    group = models.ManyToManyField(User, related_name='destinations')
    objects = TravelManager()

    def __str__(self):
        return self.destination
