# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class SiteUsers(models.Model):
    email = models.CharField(max_length=100,primary_key=True)
    firstname = models.CharField(max_length=100,blank=True)
    lastname = models.CharField(max_length=100,blank=True)
    gender = models.CharField(max_length=7,blank=True)
    mobileno = models.IntegerField()

class city(models.Model):
    Name = models.CharField(max_length=50,blank=True)
    CountryCode = models.CharField(max_length=50,blank=True)
    District = models.CharField(max_length=50,blank=True)
    Population = models.IntegerField()

class otp(models.Model):
    email = models.CharField(max_length=100,primary_key=True)
    otpnumber = models.IntegerField()
