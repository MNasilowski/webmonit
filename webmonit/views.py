from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from .models import Page, PageLog
from django.db.models import Q
from .forms import CreatePageForm


def index(request):
    observed_pages = Page.objects.all()
    context = {
        'Pages': observed_pages,
    }
    return render(request, 'webmonit/index.html', context)


def detail(request, page_id):
    page = get_object_or_404(Page, pk=page_id)
    return render(request, 'webmonit/detail.html', {'page': page})


def page_log(request, page_id):
    page_logs = PageLog.objects.filter(page__pk=page_id)
    context = {
        'Logs': page_logs
    }
    return render(request, 'webmonit/logs.html', context)

def pages_with_problem(request):
    pages = Page.objects.filter(~Q(status=200))
    context = {
        'Pages': pages
    }
    return render(request, 'webmonit/problems.html', context)

def create(request):
    if request.method == 'POST':
        form = CreatePageForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/webmonit/")
    else:
        form = CreatePageForm()

    context = {'form' : form }
    return render(request, 'webmonit/create.html', context)

def edit(request, page_id):
    page = get_object_or_404(Page, pk=page_id)
    if request.method == 'POST':
        form = CreatePageForm(request.POST, instance=page)
        if form.is_valid():
            post = form.save()
            post.save()
            return HttpResponseRedirect("/webmonit/")
    else:
        form = CreatePageForm(instance=page)

    context = {'form' : form}
    return render(request, 'webmonit/edit.html', context)


def delete(request, page_id):
    context = {}
    page = get_object_or_404(Page, pk=page_id)
    if request.method == 'POST':
        page.delete()
        return HttpResponseRedirect("/webmonit/")
    return render(request, 'webmonit/delete.html', context)