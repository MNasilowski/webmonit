from django.urls import path

from . import views

app_name = 'webmonit'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:page_id>/details/', views.detail, name='detail'),
    path('<int:page_id>/logs/', views.page_log, name='page_log'),
    path('problems/', views.pages_with_problem, name='problems'),
    path('create/', views.create, name='create'),
    path('<int:page_id>/edit/', views.edit, name='edit'),
    path('<int:page_id>/delete/', views.delete, name='delete'),
]
