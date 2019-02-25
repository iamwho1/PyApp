from django.shortcuts import render

# Create your views here.

import textwrap
import os, psutil
import json
from stackapi import StackAPI


from django.http import HttpResponse
from django.views.generic.base import View

class HomePageView(View):

    def dispatch(request, *args, **kwargs):
        global listOfProcessNames; listOfProcessNames = list()
        global processName; processName = list()
        global output

        for proc in psutil.process_iter():    
                listDict = proc.as_dict(attrs=['pid', 'name', 'cpu_percent'])
                listOfProcessNames.append(listDict)
                processName.append(proc.name())
            
        output="\n".join(str(v) for v in listOfProcessNames)

        with open('./config.json', '+w') as configfile:
            json.dump(processName, configfile)

        with open('./config.json') as f:
            data=json.load(f)

        return HttpResponse(output, content_type="text/plain")

class StackPageView(View):
    
    def dispatch(request, *args, **kwargs):

        # Fetching the StackAPI with tag of grafana 
        SITE = StackAPI('stackoverflow')
        search = SITE.fetch('search', intitle='grafana', order='asc', pagesize=10)

        #Writing the fetched data to a json name: config.json
        with open('./search.json', 'w') as f:
            json.dump(search, f, indent=4)

        # Storing the data view_count:link to dictionary 
        with open('./search.json') as f:
            data = json.loads(f.read())

        views = dict()
        for item in data['items']:
            viewcount = item['view_count']
            links = item['link']
            views[viewcount] = links

        # Sorting the number of total views from highest to lowest
        sorted_views = sorted(views.items(), key=lambda kv: kv[0], reverse=True)

        # Printing the Top 10 highest view count 
        output = []
        b = 0
        while b < 10:
            sorted_views[b]
            output.append(sorted_views[b])
            b += 1
        output="\n".join(str(v) for v in output)
            
        return HttpResponse(output, content_type="text/plain")