from django.urls import path

from . import views 

app_name = 'mediaapp'

urlpatterns = [
    path('', views.file_list, name='file_list'),
    path('upload/', views.upload_file, name='upload'),
    path('delete/<int:pk>/', views.file_delete, name='file_delete'),
]
