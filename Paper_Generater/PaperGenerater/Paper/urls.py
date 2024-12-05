# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.select_grade, name='select_grade'),
    path('select-subject/', views.select_subject, name='select_subject'),
    path('select-chapter/', views.select_chapter, name='select_chapter'),
    path('generate-paper/', views.generate_paper, name='generate_paper'),
]
