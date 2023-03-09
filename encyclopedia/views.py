from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponseRedirect
import re
from random import randint
from markdown2 import markdown

from . import util

class NewEntryForm(forms.Form):
    entry_title = forms.CharField(label="Title")
    entry_text = forms.CharField(label="Description")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_title):
    entry_text = str(util.get_entry(entry_title.strip()))
    entry_text = markdown(entry_text)
    entry_list = util.list_entries()
    if entry_title in entry_list:
        return render(request, "encyclopedia/entry.html", {
            "entry_title": entry_title, "entry_text": entry_text
        })
    else:
        entry_text = "Error: Entry does not exist"
        return render(request, "encyclopedia/entry.html", {
            "entry_title": entry_title, "entry_text": entry_text
        })
    
def search_view(request):
    query_dict = request.GET #this is a dictionary
    query = query_dict.get("q") 
    search_results = []
    for entry in util.list_entries():
        if query.casefold() == entry.casefold():
            return HttpResponseRedirect(str(entry))
        
        if query.casefold() in entry.casefold():
            search_results.append(entry)
    
    return render(request, "encyclopedia/search.html", {
        "search_results":search_results, "query":query
    })
    
def add(request):
    if request.method == "POST":
        entry_title = request.POST.get("entry_title").strip()
        entry_text = request.POST.get("entry_text").strip()
        
        if entry_title == "" or entry_text == "":
            return render(request, "encyclopedia/add.html", {"message": "Please fill in all fields", "entry_title":entry_title, "entry_text":entry_text})
        
        if entry_title in util.list_entries():
            return render(request, "encyclopedia/add.html", {"message": "Error. Entry already exists.", "entry_title":entry_title, "entry_text":entry_text})
        
        entry_text = "<h1>"+str(entry_title)+"</h1>"+entry_text
        util.save_entry(entry_title, entry_text)
        return redirect("encyclopedia:entry", entry_title)
    
    return render(request, "encyclopedia/add.html")

def edit(request, entry_title):
    entry_text = util.get_entry(entry_title.strip())
    if entry_text == None:
        return render(request, "encyclopedia/edit.html", {'error':"404 Not Found"})
    if request.method == "POST":
        entry_text = request.POST.get("entry_text").strip()
        if entry_text == "":
            return render(request, "encyclopedia/edit.html", {"message": "Empty description", "entry_title":entry_title, "entry_text":entry_text})
        util.save_entry(entry_title, entry_text)
        return redirect("encyclopedia:entry", entry_title = entry_title)    
    return render(request, "encyclopedia/edit.html", {"entry_title": entry_title, "entry_text": entry_text})        
           
def random(request):
     entry_list = util.list_entries()
     random_entry = entry_list[randint(0, len(entry_list)-1)]
     return redirect("encyclopedia:entry", entry_title=random_entry)
            

    
    


    
    
            

            

    