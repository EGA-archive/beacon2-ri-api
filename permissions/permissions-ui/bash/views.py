from django.shortcuts import render, redirect
from django.views.generic import TemplateView
import subprocess
from web.forms import BamForm
import time
from django.http import HttpResponseRedirect, HttpResponseBadRequest
import logging
import json
import yaml
from pymongo.mongo_client import MongoClient
import imp
from django.urls import resolve

# load a source module from a file
file, pathname, description = imp.find_module('beacon', [''])
my_module = imp.load_module('beacon', file, pathname, description)

from beacon import conf

client = MongoClient(
        "mongodb://{}:{}@{}:{}/{}?authSource={}".format(
            conf.database_user,
            conf.database_password,
            conf.database_host,
            conf.database_port,
            conf.database_name,
            conf.database_auth_source,
        )
    )




LOG = logging.getLogger(__name__)

def add_public_datasets(list_datasets):
    with open("../beacon/permissions/public_datasets.yml", 'r') as pfile:
        public_datasets = yaml.safe_load(pfile)
    pfile.close
    public_datasets['public_datasets']=list_datasets
    with open("../beacon/permissions/public_datasets.yml", 'w') as pfile:
        yaml.dump(public_datasets, pfile)
    pfile.close

def add_controlled_datasets(list_datasets):
    with open("../beacon/permissions/controlled_datasets.yml", 'r') as pfile:
        controlled_datasets = yaml.safe_load(pfile)
    pfile.close
    controlled_datasets['controlled_datasets']=list_datasets
    with open("../beacon/permissions/controlled_datasets.yml", 'w') as pfile:
        yaml.dump(controlled_datasets, pfile)
    pfile.close
    
def add_registered_datasets(list_users, list_datasets):
    with open("../beacon/permissions/registered_datasets.yml", 'r') as pfile:
        registered_datasets = yaml.safe_load(pfile)
    pfile.close
    for user in list_users:
        print(user)
        registered_datasets[user]=[]
        for dataset in list_datasets:
            if dataset not in registered_datasets[user]:
                registered_datasets[user].append(dataset)
    with open("../beacon/permissions/registered_datasets.yml", 'w') as pfile:
        yaml.dump(registered_datasets, pfile)
    pfile.close

def load_datasets():
    results = client.beacon.get_collection('datasets').find({}, {"id": 1})
    results = list(results)
    list_of_datasets=[]
    for object in results:
        for k,v in object.items():
            if k == 'id':
                list_of_datasets.append(v)
    return list_of_datasets

def load_public_datasets():
    with open("../beacon/permissions/public_datasets.yml", 'r') as pfile:
        public_datasets = yaml.safe_load(pfile)
    pfile.close()

    list_of_public_datasets = public_datasets['public_datasets']

    return list_of_public_datasets

def load_controlled_datasets():
    with open("../beacon/permissions/controlled_datasets.yml", 'r') as pfile:
        controlled_datasets = yaml.safe_load(pfile)
    pfile.close()

    list_of_controlled_datasets = controlled_datasets['controlled_datasets']

    return list_of_controlled_datasets

def load_users():
    with open("../beacon/permissions/registered_datasets.yml", 'r') as pfile:
        registered_datasets = yaml.safe_load(pfile)
    pfile.close()

    list_users=[]

    for k, v in registered_datasets.items():
        list_users.append(k)

    return list_users

def load_registered_datasets(user):
    with open("../beacon/permissions/registered_datasets.yml", 'r') as pfile:
        registered_datasets = yaml.safe_load(pfile)
    pfile.close()

    list_registered_datasets=[]

    for k, v in registered_datasets.items():
        if k == user:
            list_registered_datasets = v

    return list_registered_datasets



def bash_view(request):
    template = "home.html"
    form =BamForm()
    context = {'form': form}
    if request.method == 'POST':
        form = BamForm(request.POST)
        if form.is_valid():
            reference = form.cleaned_data['Datasets']
            if reference == 'PUBLIC':
                return redirect("bash:public")
            elif reference == 'CONTROLLED':
                return redirect("bash:controlled")
            elif reference == 'REGISTERED':
                return redirect("bash:registered")
    return render(request, template, context)

def public_view(request):
    template = "public.html"
    datasets=load_datasets()
    bash_out=load_public_datasets()
    context={'bash_out': bash_out, 'datasets': datasets}
    if request.method == 'POST':
        answer = request.POST.getlist('list', False)
        print(answer)
        add_public_datasets(answer)
        context = {
                'answer': answer,
            }
        return redirect("bash:index")
    return render(request, template, context)

def controlled_view(request):
    template = "controlled.html"
    datasets=load_datasets()
    bash_out=load_controlled_datasets()
    context={'bash_out': bash_out, 'datasets': datasets}
    if request.method == 'POST':
        answer = request.POST.getlist('list', False)
        print(answer) 
        add_controlled_datasets(answer)
        context = {
                'answer': answer,
            }
        return redirect("bash:index")
    return render(request, template, context)

def registered_view(request):
    template = "registered.html"
    bash_out=load_users()
    datasets=load_datasets()
    context={}
    if request.method == 'GET':
        users = request.GET.getlist('userslist', False)
        if users != False:
            registered_datasets = load_registered_datasets(users[0])
            context={'bash_out': bash_out, 'datasets': datasets, 'users': users, 'registered_datasets': registered_datasets}
        else:
            context={'bash_out': bash_out, 'datasets': datasets, 'users': users}

        return render(request, template, context)


    if request.method == 'POST':
        user = request.POST.getlist('users', False)
        datasets_list = request.POST.getlist('list', False)
        add_registered_datasets(user, datasets_list)
        context = {
                'answer': user, 'datasets_list': datasets_list
            }
        return redirect("bash:index")
    return render(request, template, context)