from django.shortcuts import render, redirect

from . import util
from markdown2 import Markdown
import random


def convert_md_to_html(entry):
    markdowner = Markdown()
    if entry:
        return markdowner.convert(entry)
    else:
        return None


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    entry = util.get_entry(title)
    html_content = convert_md_to_html(entry)
    if html_content:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })


def search(request):
    if request.method == "POST":
        query = request.POST["q"]
        html_content = convert_md_to_html(util.get_entry(query))
        if html_content:
            return redirect("entry", title=query)
        else:
            entries = util.list_entries()
            results = []
            for entry in entries:
                if query.lower() in entry.lower():
                    results.append(entry)
            return render(request, "encyclopedia/search.html", {
                "results": results
            })


def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    elif request.method == "POST":
        title = request.POST["title"]
        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {
                "message": "The entry already exists."
            })
        else:
            content = request.POST["content"]
            util.save_entry(title, content)
            return redirect("entry", title=title)


def edit(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    elif request.method == "POST":
        content = request.POST["content"]
        util.save_entry(title, content)
        return redirect("entry", title=title)


def random_entry(request):
    entries = util.list_entries()
    return redirect("entry", title=random.choice(entries))
