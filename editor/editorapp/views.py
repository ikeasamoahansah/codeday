from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from django.urls import reverse
from .models import Note, Snippet
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login as auth_login
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import pdfkit
config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")

from .forms import *

# Create your views here.


def get_and_del(request):
    if request.method == "POST":
        note_id = request.POST.get("note-id")
        note = Note.objects.filter(id=note_id).first()
        if note and note.owner == request.user:
            note.delete()


def get_and_del_snip(request):
    if request.method == "POST":
        snip_id = request.POST.get("snip-id")
        snip = Snippet.objects.filter(id=snip_id).first()
        if snip and snip.context.owner == request.user:
            snip.delete()


def home(request):

    notes = Note.objects.all()
    snippets = Snippet.objects.all()
    get_and_del(request)

    context = {
        "notes": notes,
        "snippets": snippets,
        "form": NoteForm()
    }


    return render(request, 'home.html', context)


def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'signup.html', {"form":form})


def logout_view(request):
    logout(request)
    return redirect('login')


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/home')
        else:
            return render(request, "login.html", {
                "msg": "Invalid login credentials"
            })
    else:
        return HttpResponse('<h1>Failed attempt to login</h1>')



@login_required(login_url='/login')
def post_content(request):
    if request.method == "POST":
        note_form = NoteForm(request.POST)
        if note_form.is_valid():
            note = note_form.save(commit=False)
            note.owner = request.user
            note.save()
            return redirect("/home")
        

    else:
        note_form = NoteForm()
    return render(request, 'post.html', {"form":note_form})


@login_required(login_url='/login')
def post_snip(request):

    if request.method == "POST":
        snippet_form = SnippetForm(request.POST)
        if snippet_form.is_valid():
                snippet_form.save()
                return redirect("/home")
    else:
        snippet_form = SnippetForm()
    return render(request, 'post.html', {"form":snippet_form})

def post_view(request, pk):

    if request.method == 'POST':
        get_and_del_snip(request)
        pdf = pdfkit.from_url(request.build_absolute_uri(), False, configuration=config)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Dispositon'] = 'attatchment; filename="filename.pdf"'
        return response
    

    note = Note.objects.get(id=pk)
    snippets = note.snippet_set.all()
    context = {
        "note": note,
        "snippets": snippets,
        "form": SnippetForm()
    }

    return render(request, 'view_post.html', context)


def edit_note(request, pk):
    current_note = Note.objects.get(id=pk)

    if request.method == "POST":
        form = NoteForm(request.POST or None, instance=current_note)
        if form.is_valid():
            form.save()
            return redirect(f'/note/{pk}')
    else:
        form = NoteForm(initial={
            'title': current_note.title,
            'text': current_note.text,
        })
    
    return render(request, 'update_note.html', {
        "form": form
    })


def edit_snippet(request, pk):

    current_snip = Snippet.objects.get(id=pk)

    if request.method == "POST":
        form = SnippetForm(request.POST or None, instance=current_snip)
        if form.is_valid():
            form.save()
            return redirect(f'/home')
    else:
        form = SnippetForm(initial={
            'title': current_snip.title,
            'code': current_snip.code,
            'language': current_snip.language,
            'style': current_snip.style,
            'context': current_snip.context,
        })
    
    return render(request, 'update_note.html', {
        "form": form
    })
