from django import forms
from django.utils.translation import gettext_lazy as _
from . import models

class GardenProjectForm(forms.ModelForm):
    class Meta:
        model = models.GardenProject
        fields = ['project_name', 'public', ]
        lables = {
            'project_name': _('project name'),
            'public': _('public'),
        }

class ZoneForm(forms.ModelForm):
    class Meta:
        model = models.Zone
        fields = ['name', 'lenght', 'width', 'public']


class SelectedPlantForm(forms.ModelForm):
    class Meta:
        model = models.SelectedPlant
        fields = ['plant', 'color', 'blooming_period', 'qty', 'price']

class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ['image', 'season']

