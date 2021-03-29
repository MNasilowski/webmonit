from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from .models import Page, PageLog
from django.db.models import Q
from .forms import CreatePageForm
from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PageSerializer

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
    monit_instance = page.monit_instance
    monit_content = page.monit_content
    if request.method == 'POST':
        form = CreatePageForm(request.POST, instance=page)
        if form.is_valid():
            post = form.instance
            post.monit_instance = monit_instance
            post.monit_content = monit_content
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


@api_view(['GET'])
def pageOverview(request):
	webmonit_urls = {
		'List':'/page-list/',
		'Detail View':'/page-detail/<str:pk>/',
		'Create':'/page-create/',
		'Update':'/page-update/<str:pk>/',
		'Delete':'/page-delete/<str:pk>/',
		}
	return Response(webmonit_urls)


@api_view(['GET'])
def pageList(request):
	pages = Page.objects.all().order_by('-id')
	serializer = PageSerializer(pages, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def pageDetail(request, pk):
	pages = Page.objects.get(id=pk)
	serializer = PageSerializer(pages, many=False)
	return Response(serializer.data)


@api_view(['POST'])
def pageCreate(request):
	serializer = PageSerializer(data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

@api_view(['POST'])
def pageUpdate(request, pk):
	page = Page.objects.get(id=pk)
	serializer = PageSerializer(instance=page, data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)


@api_view(['DELETE'])
def pageDelete(request, pk):
	page = Page.objects.get(id=pk)
	page.delete()

	return Response('Item succsesfully delete!')