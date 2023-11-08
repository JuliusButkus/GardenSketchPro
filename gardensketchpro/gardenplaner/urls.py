from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('plant_types/', views.PlantTypeListView.as_view(), name='plant_types'),
    path('plant_list/', views.PlantListView.as_view(), name='plant_list'),
]