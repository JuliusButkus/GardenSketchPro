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