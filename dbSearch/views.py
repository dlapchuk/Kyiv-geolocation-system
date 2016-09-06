
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
import Database
from django import forms
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import CheckboxFieldRenderer
from django.core.paginator import Paginator
from django import forms

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import os

def main(request):
    return render_to_response('start.html', context_instance=RequestContext(request))

def sendMessage(request):
    if(request.method=="POST"):
        user = auth.get_user(request).username
        number = request.POST.get('send')
        message= request.POST['message']

    Database.sendMessage(user, number, message)
    table = Database.getShow(number, user)
    nearest = Database.getNearest(number)
    comments = Database.getComments(number)
    return render_to_response('showFact.html',{'table': table, 'nearest': nearest, 'comments': comments},context_instance=RequestContext(request))


def deleteMessage(request):
    number = request.POST.get('delete')
    print number
    user = auth.get_user(request).username
    pl_number = Database.getPlaceID(number)

    Database.deleteMessage(number)
    table = Database.getShow(pl_number, user)
    nearest = Database.getNearest(pl_number)
    comments = Database.getComments(pl_number)
    return render_to_response('showFact.html',{'table': table, 'nearest': nearest, 'comments': comments},context_instance=RequestContext(request))


def makeDump(request):
    Database.makeDump()
    return redirect('/dbSearch/outFacts/')

def makeRestore(request):
    Database.makeRestore()
    return redirect('/dbSearch/outFacts/')

def favorite(request):
    user = auth.get_user(request).username
    table = Database.findFavorite(user)
    print user
    return render_to_response('favorite.html',{'table': table},context_instance=RequestContext(request))

def login(request):
    if(request.method == "POST"):
        login = request.POST['login']
        password = request.POST['password']
        user = auth.authenticate(username=login,password=password)
        if user is not None:
            print user
            auth.login(request,user)
            return redirect('/dbSearch/')
        else:
            message="User not found"
            return render_to_response('login.html',{'error_message': message},context_instance=RequestContext(request))
    else:
        return render_to_response('login.html',context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)
    return redirect('/dbSearch/')

def signin(request):
    form = UserCreationForm()
    message = ""
    if(request.method == "POST"):
            form = UserCreationForm(request.POST)
            if(form.is_valid()):
                username =form.cleaned_data['username']
                password = form.cleaned_data['password2']
                #email = form.cleaned_data['email']
                User.objects.create_user(username,password)
                user = auth.authenticate(username = username,password = password)
                #group = Group.objects.get(name='users')
                #group.user_set.add(user)
                #auth.login(request,user)
                return redirect("/dbSearch/")
            else:
                return render_to_response("register.html",{'form':form},context_instance=RequestContext(request))
    else:
        return render_to_response("register.html",{'form':form},context_instance=RequestContext(request))


def showFact(request):
    user = auth.get_user(request).username
    number = request.POST.get('show')
    table = Database.getShow(number, user)
    nearest = Database.getNearest(number)
    comments = Database.getComments(number)
    return render_to_response('showFact.html',{'table': table, 'nearest': nearest, 'comments': comments},context_instance=RequestContext(request))


def outFacts(request, page_number=1):
    district = str("All")
    type = str("All")
    sort = request.POST.get('sort')
    table = Database.findPlaces(sort, district, type)
    Database.getCustStat()
    current_page = Paginator(table, 15)
    type = Database.getTypes()
    distr = Database.getDistricts()
    user = auth.get_user(request).username
    return render_to_response('outFacts.html',{'table': current_page.page(page_number),
                                               'sort': sort, 'types': type,'districts': distr},context_instance=RequestContext(request))

def finder(request):
    sort = request.POST.get('sort')
    if(request.method == "POST"):
        district= request.POST['district']
        type = request.POST['type']
    table = Database.findPlaces(sort, district, type)
    Database.getCustStat()
    typ = Database.getTypes()
    distr = Database.getDistricts()
    user = auth.get_user(request).username

    return render_to_response('outFacts.html',{'table': table, 'sort': sort, 'types': typ,'districts': distr},context_instance=RequestContext(request))

def addPlace(request):
    type = Database.getTypes()
    distr = Database.getDistricts()
    return render_to_response('add.html',{'types': type,'districts': distr},
                              context_instance=RequestContext(request))


def addFactConfirm(request):
    if(request.method == "POST"):
        distr= request.POST['distr']
        type = request.POST['type']
        name = request.POST['name']
        image = request.POST['image']
        longitude = float(request.POST['longitude'])
        latitude = float(request.POST['latitude'])
        description = request.POST['description']

        Database.addPlace(distr, type, name, image, longitude, latitude, description)

    return HttpResponseRedirect('/dbSearch/outFacts/')

def deleteFact(request):
    number = request.POST.get('delete')
    Database.deletePlace(number)
    return HttpResponseRedirect('/dbSearch/outFacts/')

def editFact(request):
    number = request.POST.get('edit')
    type = Database.getTypes()
    distr = Database.getDistricts()
    table = Database.getPlace(number)

    return render_to_response('edit.html',{'table': table,'number': number,'types': type,'districts': distr},
                              context_instance=RequestContext(request))

def addFavorite(request):
    user = auth.get_user(request).username
    number = request.POST.get('giveMark')
    mark = int(request.POST['mark'])
    Database.addFavorite(number, user, mark)
    table = Database.getShow(number, user)
    nearest = Database.getNearest(number)
    comments = Database.getComments(number)
    return render_to_response('showFact.html',{'table': table, 'nearest': nearest, 'comments': comments},context_instance=RequestContext(request))


def deleteFavorite(request):
    user = auth.get_user(request).username
    number = request.POST.get('giveMark')
    table = Database.getShow(number, user)
    nearest = Database.getNearest(number)
    comments = Database.getComments(number)
    Database.deleteFavorite(number, user)
    return render_to_response('showFact.html',{'table': table, 'nearest': nearest, 'comments': comments},context_instance=RequestContext(request))


def editFactConfirm(request):
    if(request.method == "POST"):
        number = request.POST.get('edit')
        distr= request.POST['distr']
        type = request.POST['type']
        name = request.POST['name']
        #name = string.split(name)
        image = request.POST['image']
        #image = string.split(image)
        longitude = float(request.POST['longitude'])
        #longitude = double(longitude)
        latitude = float(request.POST['latitude'])
        #latitude = double(latitude)
        description = request.POST['description']
        #description = string.split(description)
        Database.updatePlace(number,distr,type,name, image, longitude, latitude, description)
    return HttpResponseRedirect('/dbSearch/outFacts/')

def custStat(request):
    table = Database.getCustStat()
    return render_to_response('markStat.html',{'table': table}, context_instance=RequestContext(request))





















# Create your views here.
