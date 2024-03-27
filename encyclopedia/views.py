from django.shortcuts import render

from . import util
from markdown2 import Markdown


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
