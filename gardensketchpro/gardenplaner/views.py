from typing import Any
from datetime import date, timedelta
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models.query import QuerySet, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.forms.models import inlineformset_factory
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from . import models, forms


def index(request: HttpRequest):
    """
    Renders the 'index.html' template with the given request and context.
    Parameters:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The rendered 'index.html' template with the given context.
    """
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_visits': num_visits,
    }
    return render(request, 'gardenplaner/index.html', context)

class PlantTypeListView(generic.ListView):
    model = models.Type
    template_name = "gardenplaner/plant_types.html"
    context_object_name = "type_list"
    paginate_by = 10

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search"] = True
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("query")
        if query:
            queryset = queryset.filter(
                Q(name_en__icontains=query) | 
                Q(name_lt__icontains=query)  
            )
        return queryset
    

class PlantListView(generic.ListView):
    model = models.Plant
    template_name = "gardenplaner/plant_list.html"
    context_object_name = "plant_list"
    paginate_by = 10

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search"] = True
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("query")
        if query:
            queryset = queryset.filter(
                Q(name_en__icontains=query) | 
                Q(name_lt__icontains=query)  
            )
        return queryset   


class GardenProjectListView(generic.ListView):
    model = models.GardenProject
    template_name = "gardenplaner/my_projects.html"
    context_object_name = "gardenproject_list"
    paginate_by = 10

class CreateGardenProjectView(generic.View):
    template_name = 'gardenplaner/create_project.html'

    def get(self, request, *args, **kwargs):
        form = forms.GardenProjectForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.GardenProjectForm(request.POST)
        if form.is_valid():
            garden_project = form.save(commit=False)
            garden_project.user = request.user  # Assuming the user is authenticated
            garden_project.save()
            return redirect('gardenproject_detail', pk=garden_project.pk)
        return render(request, self.template_name, {'form': form})
    

class GardenProjectDetailView(generic.DetailView):
    model = models.GardenProject
    template_name = "gardenplaner/gardenproject_detail.html"
    context_object_name = "garden_project"

def delete_project_view(request, pk):
    garden_project = get_object_or_404(models.GardenProject, pk=pk)
    if request.method == 'POST':
        garden_project.delete()
        return redirect('my_projects')
    return render(request, 'gardenplaner/gardenproject_confirm_delete.html', {'garden_project': garden_project})


def confirm_delete_project_view(request, pk):
    garden_project = get_object_or_404(models.GardenProject, pk=pk)
    return render(request, 'gardenplaner/confirm_delete_project.html', {'garden_project': garden_project}) 


class ZoneDetailView(generic.DetailView):
    model = models.Zone
    template_name = 'gardenplaner/zone_detail.html'
    context_object_name = 'zone'


class CreateZoneView(generic.View):
    template_name = 'gardenplaner/create_zone.html'

    def get(self, request, project_id):
        garden_project = get_object_or_404(models.GardenProject, pk=project_id)
        zone_form = forms.ZoneForm()
        return render(request, self.template_name, {
            'zone_form': zone_form,
            'garden_project': garden_project
        })

    def post(self, request, project_id):
        garden_project = get_object_or_404(models.GardenProject, pk=project_id)
        zone_form = forms.ZoneForm(request.POST)

        if zone_form.is_valid():
            zone = zone_form.save(commit=False)
            zone.garden_project = garden_project
            zone.save()

            # Redirect to the zone_detail view
            return redirect('zone_detail', project_id=project_id, pk=zone.pk)

        return render(request, self.template_name, {
            'zone_form': zone_form,
            'garden_project': garden_project
        })


class SelectPlantView(generic.View):
    template_name = "gardenplaner/selecting_plants.html"

    def get(self, request, zone_id):
        zone = get_object_or_404(models.Zone, pk=zone_id)
        selected_plants = models.SelectedPlant.objects.filter(zone=zone)

        form = forms.SelectedPlantForm()

        context = {
            'zone': zone,
            'selected_plants': selected_plants,
            'form': form,
        }

        return render(request, self.template_name, context)

    def post(self, request, zone_id):
        zone = get_object_or_404(models.Zone, pk=zone_id)

        form = forms.SelectedPlantForm(request.POST)
        if form.is_valid():
            selected_plant = form.save(commit=False)
            selected_plant.zone = zone
            selected_plant.save()

        return redirect('selecting_plants', zone_id=zone_id)