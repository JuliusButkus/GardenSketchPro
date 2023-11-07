from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField
from django.urls import reverse


User = get_user_model()

class Type(models.Model):
    name_en = models.CharField(_('name in English language'), max_length=100)
    name_lt = models.CharField(_('name in Lithuanian language'),max_length=100)
    description_en = models.TextField(_('description in English language'), max_length=1000)
    description_lt = models.TextField(_('description in English language'), max_length=1000)
    
    class Meta:
        verbose_name = _("type")
        verbose_name_plural = _("types")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("type_detail", kwargs={"pk": self.pk})


class PlantTime(models.Model):
    month_en = models.CharField(
        choices=[
            (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'),
            (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'),
            (11, 'November'), (12, 'December'),
        ],
        max_length=15
    )
    month_lt = models.CharField(
        choices=[
            (1, 'Sausis'), (2, 'Vasaris'), (3, 'Kovas'), (4, 'Balandis'), (5, 'Gegužė'),
            (6, 'Birželis'), (7, 'Liepa'), (8, 'Rugpjūtis'), (9, 'Rugsėjis'), (10, 'Spalis'),
            (11, 'Lapkritis'), (12, 'Gruodis'),
        ],
        max_length=15
    )
    first_day = models.IntegerField(
        choices=[
            (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'),
            (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'),
            (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'),
            (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24'), (25, '25'),
            (26, '26'), (27, '27'), (28, '28'), (29, '29'), (30, '30'), (31, '31'),
        ])
    last_day = models.IntegerField(
        choices=[
            (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'),
            (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'),
            (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'),
            (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24'), (25, '25'),
            (26, '26'), (27, '27'), (28, '28'), (29, '29'), (30, '30'), (31, '31'),
        ])
    
    class Meta:
        verbose_name = _("plantTime")
        verbose_name_plural = _("plantTimes")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plantingday_detail", kwargs={"pk": self.pk})


class Color(models.Model):
    name_en = models.CharField(_("name in English language"),max_length=100)
    name_lt = models.CharField(_("name in Lithuanian language"),max_length=100)
    description_en = models.TextField(_("description in English language"), max_length=1000)
    description_lt = models.TextField(_("description in Lithuanian language"), max_length=1000)
    
    class Meta:
        verbose_name = _("color")
        verbose_name_plural = _("colors")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("color_detail", kwargs={"pk": self.pk})

class Plant(models.Model):
    name_en = models.CharField(max_length=100, unique=True)
    name_lt = models.CharField(max_length=100, unique=True)
    description_en = models.TextField(max_length=1000, blank=True)
    description_lt = models.TextField(max_length=1000, blank=True)
    type = models.ForeignKey(
        Type,
        verbose_name=_("type"),
        on_delete=models.CASCADE, 
        related_name=_("plant"),)
    color = models.ManyToManyField(
        Color,
        verbose_name=_("color"), 
        related_name=_("plant"),
        )
    planting_time = models.ForeignKey(
        PlantTime, 
        verbose_name=_("planting time"),
        on_delete=models.CASCADE,
        related_name=_("plant"))
    
    class Meta:
        verbose_name = _("plant")
        verbose_name_plural = _("plants")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plant_detail", kwargs={"pk": self.pk})
    
#zemiau modelio dalis kuria manipuliuoja vartotojas virsuje
# modelio dalis kiri tvarkoma administratoriaus.

class GardenProject(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name=_("garden_project"),
    )
    project_name = models.CharField(_("project name"), max_length=100)
    public = models.BooleanField(_("public"), default=False)

    class Meta:
        verbose_name = _("garden project")
        verbose_name_plural = _("garden projects")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("gardenproject_detail", kwargs={"pk": self.pk})
    

class Zone(models.Model):
    name_en = models.CharField(_("name in English language"), max_length=50, blank=True)
    name_lt = models.CharField(_("name in Lithuanian language"), max_length=50, blank=True)
    lenght = models.FloatField(_("enter lenght"))
    width = models.FloatField(_("enter width"))
    garden_project = models.ForeignKey(
        GardenProject,
        verbose_name=_("garden project"),
        on_delete=models.CASCADE,
        related_name=_("zone"),
    )
    
    class Meta:
        verbose_name = _("zone")
        verbose_name_plural = _("zones")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("zone_detail", kwargs={"pk": self.pk})


class ZoneCoposition(models.Model):
    zone = models.ForeignKey(
        Zone,
        verbose_name=_("zone"),
        on_delete=models.CASCADE,
        related_name=_("zone_coposition"),
    )
    public = models.BooleanField(_("public"), default=False)
    
    

    class Meta:
        verbose_name = _("zone coposition")
        verbose_name_plural = _("zone copositions")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("zonecoposition_detail", kwargs={"pk": self.pk})
  

class SelectedPlant(models.Model):
    plant = models.ForeignKey(
        Plant, 
        verbose_name=_("plant"),
        on_delete=models.CASCADE,
        related_name=_("selected_plant"))
    color = models.ForeignKey(
        Color,
        verbose_name=_("color"), 
        on_delete=models.CASCADE,
        related_name=_("selected_plant"))
    blooming_period = models.CharField(_("enter blooming period"), max_length=100)
    qty = models.IntegerField(_('enter quantity'))
    price = models.FloatField(_('enter plants price of unit'),)
    zone_composition = models.ForeignKey(
        ZoneCoposition,
        verbose_name=_("zone composition"),
        on_delete=models.CASCADE,
        related_name=_("selected_plant")
        )

    class Meta:
        verbose_name = _("selected plant")
        verbose_name_plural = _("selected plants")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("selectedplant_detail", kwargs={"pk": self.pk}) 


class Photo(models.Model):
    image = models.ImageField(_("add image"), upload_to="photos")
    season = models.CharField(
        _("select season"), 
        max_length=100, 
        choices=[
            ("SPRING", "SPRING"), 
            ("SUMMER", "SUMMER"), 
            ("AUTUMN", "AUTUMN"), 
            ("WINTER", "WINTER"),
        ])
    composition = models.ForeignKey(
        ZoneCoposition,
        verbose_name=_("zone composition"),
        on_delete=models.CASCADE,
        related_name=_("photo")
        )
        

    class Meta:
        verbose_name = _("photo")
        verbose_name_plural = _("photos")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("photo_detail", kwargs={"pk": self.pk})

    


     






