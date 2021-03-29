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

    path('page-list/', views.pageList, name="task-list"),
    path('page-detail/<str:pk>/', views.pageDetail, name="task-detail"),
    path('page-create/', views.pageCreate, name="task-create"),
    path('page-update/<str:pk>/', views.pageUpdate, name="task-update"),
    path('page-delete/<str:pk>/', views.pageDelete, name="task-delete"),
]
