from django.shortcuts import render, redirect
from django.views.generic import TemplateView
import subprocess
from web.forms import BamForm
import time
from django.http import HttpResponseRedirect, HttpResponseBadRequest
import logging

import json
import yaml

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
        registered_datasets[user]=[]
        for dataset in list_datasets:
            if dataset not in registered_datasets[user]:
                registered_datasets[user].append(dataset)
    with open("../beacon/permissions/registered_datasets.yml", 'w') as pfile:
        yaml.dump(registered_datasets, pfile)
    pfile.close

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

def load_registered_datasets():
    with open("../beacon/permissions/public_datasets.yml", 'r') as pfile:
        registered_datasets = yaml.safe_load(pfile)
    pfile.close()

    return registered_datasets


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
    bash_out=load_public_datasets()
    context={'bash_out': bash_out}
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
    bash_out=load_controlled_datasets()
    context={'bash_out': bash_out}
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
    registered_datasets=load_registered_datasets()
    context={'bash_out': bash_out, 'registered_datasets': registered_datasets['public_datasets']}
    if request.method == 'POST':
        answer = request.POST.getlist('list', False)
        datasets_list = request.POST.getlist('list_datasets', False)
        add_registered_datasets(answer, datasets_list)
        context = {
                'answer': answer, 'datasets_list': datasets_list
            }
        return redirect("bash:index")
    return render(request, template, context)