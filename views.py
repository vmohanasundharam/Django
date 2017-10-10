# -*- coding: utf-8 -*-

from random import randint
import smtplib
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import json
from .models import city,SiteUsers
from .models import otp as otpdb
# Create your views here.

def index(request):
    return render(request, 'worldsearch/index.html', {})

def search(request):
    if 'email' not in request.session:
        return render(request, 'worldsearch/index.html', {})
    if request.is_ajax():
        uquery = request.GET.get('term', '')
        places = city.objects.filter(Name__startswith=uquery)
        results = []
        for pl in places:
            place_json = {}
            place_json = pl.Name
            results.append(place_json)
            place_json = pl.District
            results.append(place_json)
        data = json.dumps(results)
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)

    elif request.method == "GET":
         return render(request, 'worldsearch/search.html', {})

    elif request.method == "POST":
        uquery = request.POST.get('data')
        places = city.objects.filter(Name__startswith=uquery)
        c_results = []
        for pl in places:
            place_json = {}
            place_json = pl.Name
            c_results.append(place_json)

        places = city.objects.filter(District__startswith=uquery)
        d_results = []
        for pl in places:
            place_json = {}
            place_json = pl.District
            d_results.append(place_json)

        places = city.objects.filter(CountryCode__startswith=uquery)
        l_results = []
        for pl in places:
            place_json = {}
            place_json = pl.CountryCode
            l_results.append(place_json)
        return render(request, 'worldsearch/resultpage.html', {'countrys':c_results,'districts':d_results,'languages':l_results})
    else:
        data = 'fail'
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)

def display(request):
    if 'email' not in request.session:
        return render(request, 'worldsearch/index.html', {})
    if request.method == "GET":
        return render(request, 'worldsearch/resultpage.html', {})

def country_details(request):
    
    if'email' not in request.session:
        return render(request, 'worldsearch/index.html', {})

    if request.method == "GET":
        
        uquery = request.GET.get('data')
        places =  city.objects.get(Name=uquery)
        results = []
        place_json = {}
        place_json = places.Name
        results.append(place_json)
        place_json =  places.CountryCode
        results.append(place_json)
        place_json = places.District
        results.append(place_json)
        place_json =  places.Population
        results.append(place_json)
        return render(request, 'worldsearch/country.html', {'country':places.Name,'code':places.CountryCode,'district':places.District,'Population':places.Population})

def register(request):
    
    if 'email' in request.session:
        return HttpResponseRedirect(reverse('search'));

    if request.method == "GET":
        return render(request, 'worldsearch/register.html', {})
    if request.method == "POST":
        fname =  request.POST.get('fname')
        lname =  request.POST.get('lname')
        email =  request.POST.get('email')
        mobile =  request.POST.get('mno')
        gender = request.POST.get('gender')
        required_field = 'yes'
        try:
            res = SiteUsers.objects.get(email=email)
            return render(request, 'worldsearch/register.html', {'required':'yes'})
        except:
             s = SiteUsers(email=email,firstname=fname,lastname=lname,gender=gender,mobileno=mobile)
             s.save()
             request.session['login']='yes'
             return HttpResponseRedirect(reverse('search'));


def login(request):
    

    if request.method == "GET":
        return render(request, 'worldsearch/login.html', {})

    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            res = SiteUsers.objects.get(email=email)
            try:
                ss = otpdb.objects.get(email=email)
                return HttpResponseRedirect(reverse('otp'));
            except:
                TEXT = sendotp(email)
                print TEXT
                ss = otpdb(email=email,otpnumber=TEXT)
                ss.save()
                return HttpResponseRedirect(reverse('otp'));
        except:
             return render(request, 'worldsearch/login.html', {'required':'yes'});

def otp(request):

    if request.method == 'GET':
        return render(request, 'worldsearch/otp.html', {})

    if request.method == 'POST':

        uotp = request.POST.get('otp')
        try:
            res = otpdb.objects.get(otpnumber=uotp)
            otpdb.objects.filter(otpnumber=uotp).delete()
            request.session['email']='yes'
            return HttpResponseRedirect(reverse('search'));
        except:

            return render(request, 'worldsearch/otp.html', {'required':'yes'});

def sendotp(memail):

    try:
        mreciever = memail
        msender = "vmohanasundharam@gmail.com"
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("vmohanasundharam@gmail.com", "")
        SUBJECT = "OTP"
        TEXT =  randint(100000, 999999)

        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
        s.sendmail(msender,mreciever, message)

        s.quit()
        return TEXT
    except:
        return 0
def logout(request):
    del request.session['email']
    return render(request, 'worldsearch/', {});
