from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from . import util
from django.core.files.base import ContentFile
from django.core.files.base import File
from django.urls import reverse
import random
from markdown2 import Markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, name):
    entryList = util.list_entries()
    if name in entryList:
        page = util.get_entry(name)
        markdowner = Markdown()
        convertedpage = markdowner.convert(page)
        if "h1" in convertedpage:
            return render(request, "encyclopedia/title.html", {
                "wikititle": name,
                "wikidetail": convertedpage
            })
        else:
            return render(request, "encyclopedia/title.html", {
                "wikititle": name,
                "wikidetail": convertedpage,
                "val": "1"
            })
    else:
        return render(request, "encyclopedia/title.html", {
            "wikititle": "404",
            "wikidetail": "Entry does not exist"
        })

def search(request):
    query = request.GET.get('q')
    print(query)

    entryList = util.list_entries()
    allSubstring = [s for s in entryList if query in s]

    if query in entryList:
        page = util.get_entry(query)
        return redirect(f'/wiki/{ query }')
    elif len(allSubstring) > 0:
        allSubstring = [s for s in entryList if query in s]
        return render(request, "encyclopedia/result.html", {
            "subList": allSubstring,
            "val": "2"
        })
    else:
        return render(request, "encyclopedia/result.html", {
            "noEnt": "0 results...",
            "val": "3"
        })

def create(request):
    entryList = util.list_entries()

    title = request.POST.get('title', '')
    content = request.POST.get('content', '')
    if title in entryList:
        if len(title) >= 1:
            return render(request, "encyclopedia/create.html", {
                "errMsg": "ERROR: entry already exists!",
                "val": "1"
            })
        else:
            return render(request, "encyclopedia/create.html", {
                "errMsg": "Enter a title",
                "val": "1"
            })
    elif title == "":
        return render(request, "encyclopedia/create.html")
    else:
        util.save_entry(title, content)
        return redirect(f'wiki/{ title }')

def edit(request, name):
    wikientry = util.get_entry(name)
    entryList = util.list_entries()

    newtitle = request.POST.get('title', '')
    newcontent = request.POST.get('content', '')
    print(newtitle)
    if newtitle == "":
        return render(request, "encyclopedia/edit.html", {
        "orgtitle": name,
        "orgcontent": wikientry,
        "newtitle": newtitle
    })
    else:
        util.save_entry(newtitle, newcontent)
        return HttpResponseRedirect(reverse('encyclopedia:title', args=(name,)))

def randompg(request):
    entryList = util.list_entries()
    totalEntries = 0
    
    for i in entryList:
        totalEntries += 1
    
    entryArr = [totalEntries]

    for i in entryList:
        entryArr.append(i)

    randomNum = random.randint(1, totalEntries)
    chosenPage = entryArr[randomNum]        
    print(chosenPage)
    print(totalEntries)
    print(randomNum)
    if chosenPage!="":
        return redirect(f'wiki/{ chosenPage }')
    else:
        randomNum = random.randint(1, totalEntries)
        chosenPage = entryArr[randomNum]        
        print(chosenPage)
        print(totalEntries)
        print(randomNum)
        return redirect(f'wiki/{ chosenPage }')
